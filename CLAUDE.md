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

When working an issue, keep its status label current. An issue carries one status label at a time. Use `gh issue edit <number> --add-label "<new>" --remove-label "<old>"`.

- **Starting work:** add `in progress`. Remove `needs info` and `ready for review` if present.
- **Blocked on a question:** ask it in a comment, then swap `in progress` for `needs info`. Stop there. Chris replies with an `@claude` mention to restart the work.
- **Branch pushed:** swap `in progress` for `ready for review`. Put `Closes #<number>` in the pull request body, so merging closes the issue.
- **Nothing to change** (already done, or not a code change): say so in a comment and remove `in progress`.

Leave the `claude` label alone. Never close an issue yourself: merging the pull request does that.
