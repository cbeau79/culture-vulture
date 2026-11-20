#!/usr/bin/env bash
# Set an issue's Status on the "culture vulture" GitHub project board.
#
# Usage: scripts/set-project-status.sh <issue-number> "<status>"
# Status is one of: Backlog, Ready, In progress, In review, Done
#
# Needs PROJECT_TOKEN: a classic personal access token with the "project" scope.
# The Claude workflow passes it in from the repo secret of the same name.
# The issue must already be on the board. If it isn't, this prints a note and exits.
set -euo pipefail

number="${1:?issue number}"
status="${2:?status name}"
repo="${GITHUB_REPOSITORY:-cbeau79/culture-vulture}"

if [ -z "${PROJECT_TOKEN:-}" ]; then
  echo "PROJECT_TOKEN is not set, so the project status was not changed."
  exit 0
fi
export GH_TOKEN="$PROJECT_TOKEN"

data=$(gh api graphql \
  -f owner="${repo%/*}" -f name="${repo#*/}" -F number="$number" \
  -f query='
    query($owner: String!, $name: String!, $number: Int!) {
      repository(owner: $owner, name: $name) {
        issue(number: $number) {
          projectItems(first: 10) {
            nodes {
              id
              project {
                id
                title
                field(name: "Status") {
                  ... on ProjectV2SingleSelectField { id options { id name } }
                }
              }
            }
          }
        }
      }
    }')

rows=$(echo "$data" | jq -r --arg s "$status" '
  .data.repository.issue.projectItems.nodes[]
  | . as $item
  | ($item.project.field.options // [])[]
  | select((.name | ascii_downcase) == ($s | ascii_downcase))
  | [$item.id, $item.project.id, $item.project.field.id, .id, $item.project.title] | @tsv')

if [ -z "$rows" ]; then
  echo "Issue #$number is not on a project board with a \"$status\" status. Nothing changed."
  exit 0
fi

while IFS=$'\t' read -r item project field option title; do
  gh api graphql \
    -f project="$project" -f item="$item" -f field="$field" -f option="$option" \
    -f query='
      mutation($project: ID!, $item: ID!, $field: ID!, $option: String!) {
        updateProjectV2ItemFieldValue(input: {
          projectId: $project, itemId: $item, fieldId: $field,
          value: { singleSelectOptionId: $option }
        }) { projectV2Item { id } }
      }' > /dev/null
  echo "Issue #$number set to \"$status\" on \"$title\"."
done <<< "$rows"
