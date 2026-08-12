# Attribution and changes

`SKILL.md`, `scripts/image_gen.py`, `references/` and `assets/` in this folder come from the
`imagegen` skill in **openai/skills**, used under the Apache License 2.0. The full licence text is
in `LICENSE.txt`, exactly as it ships upstream.

- Upstream: https://github.com/openai/skills/tree/main/skills/.system/imagegen
- Vendored from commit `49f948f`
- Note: that repository is **deprecated**; OpenAI now points to https://github.com/openai/plugins.
  Updates should be taken from wherever this skill lives there.

## Changes

1. **Added `scripts/hr_image_gen.py`.** Upstream's CLI builds the client with `OpenAI()`, which
   reads `OPENAI_API_KEY` and `OPENAI_BASE_URL` from the environment. On a Codex harness those
   names already carry the chat connection — usually a different provider — and one env pair
   cannot hold two credentials. The wrapper takes `HR_IMAGE_BASE_URL` / `HR_IMAGE_KEY` and passes
   them to the SDK explicitly, so image generation works the same on Claude Code, Codex and
   Hermes rather than only where the chat provider happens to be OpenAI.

2. **Appended "Notes for this environment" to `SKILL.md`** — which of the upstream modes applies
   here, and that no API key is ever asked of the user because the credential is a per-turn
   broker token.

Upstream files are otherwise unmodified.
