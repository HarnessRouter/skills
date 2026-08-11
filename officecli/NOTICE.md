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
   a freshly created document has no built-in styles, PDF export needs an uninstalled plugin so
   LibreOffice does that job, and there is no network at run time.

   It also covers the resident flush, which cost us a real deliverable. The default writes to disk
   seconds after the process goes idle, so a task that finishes right after writing a file loses
   its content while `validate` still passes. The image sets `OFFICECLI_RESIDENT_FLUSH=each` to
   remove the race rather than relying on the agent remembering to `close`; the note explains it
   so nobody reintroduces the race by changing that variable.

Nothing else was altered. Updating the vendored copy means re-pulling upstream `SKILL.md`, pinning
the new release in `install.sh` with its checksum, and re-applying these two changes.
