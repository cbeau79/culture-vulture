@README.md

# Rules for code changes

These apply when working a GitHub issue or PR. The README above explains the project.

- Do only what the issue asks. Keep changes small and focused.
- Never edit `emails/` or `logs/run-log.md`. They are the weekly task's output and history.
- Change `config/` files only when the issue asks for it. They shape every future digest.
- Don't add dependencies beyond `markdown` and `pyyaml` without asking in the issue first.
- Before finishing, run `pip install markdown pyyaml` then `python3 site/build.py` and confirm it builds without errors.
- If the issue is unclear, ask in a comment rather than guessing.
- Write in British English. No em dashes.

# Issue status

Issues sit on the "culture vulture" project board. When working an issue, keep its Status field current with `scripts/set-project-status.sh <number> "<status>"`.

- **Starting work:** set `In progress`.
- **Blocked on a question:** ask it in a comment, then set `Backlog`. Stop there. Chris replies with an `@claude` mention to restart the work.
- **Branch pushed:** set `In review`. Put `Closes #<number>` in the pull request body, so merging closes the issue.
- **Nothing to change** (already done, or not a code change): say so in a comment and set `Backlog`.

Never set `Done` and never close an issue yourself. Merging the pull request closes the issue, and the board moves closed issues to `Done`. If the script says it changed nothing, mention that in your comment and carry on.
