# Attribution and changes

`SKILL.md` in this folder is derived from **OfficeCLI** by iOfficeAI, used under the Apache License
2.0. The full licence text is in `LICENSE.txt`.

- Upstream: https://github.com/iOfficeAI/OfficeCLI
- Vendored from: `v1.0.143` (release of 2026-07-28)
- Binary installed by `install.sh`, pinned to that release and verified by SHA-256

## Changes made to the upstream SKILL.md

1. **Replaced the "Install" section.** Upstream tells the agent to `curl | bash` from
   `d.officecli.ai`. Tasks here have no network, so the instruction could only ever fail, and its
   failure reads as a broken tool. The binary is baked into the image instead, and the section now
   says where it is.

2. **Appended "Notes for this environment".** Behaviour we verified by running it, that the
   upstream text does not cover: `--text` is silently ignored on `add` (properties need `--prop`),
   a freshly created document has no built-in styles, the resident process must be flushed with
   `close` before another program reads the file, PDF export needs an uninstalled plugin so
   LibreOffice does that job, and there is no network at run time.

Nothing else was altered. Updating the vendored copy means re-pulling upstream `SKILL.md`, pinning
the new release in `install.sh` with its checksum, and re-applying these two changes.
