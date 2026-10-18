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
