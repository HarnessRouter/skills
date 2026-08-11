# HarnessRouter built-in skills

The skills baked into the HarnessRouter image. Every Harness can use them, and every Harness can
switch any of them off.

A skill is a folder with a `SKILL.md` in it — instructions an agent loads when the task calls for
them, plus any scripts and reference material those instructions point at. This repository is the
source of the built-in set; the image build pulls it in.

## What is here

| Skill | What it does | Origin |
|---|---|---|
| [`pdf`](./pdf) | Create PDFs from HTML with real page control; extract text and tables; merge, split, rotate, stamp; list and fill form fields; render pages to PNG for visual checking | HarnessRouter, Apache-2.0 |
| [`officecli`](./officecli) | Create, read and edit `.docx`, `.xlsx`, `.pptx` — styles, tables, formulas, pivot tables, charts, tracked changes | [iOfficeAI/OfficeCLI](https://github.com/iOfficeAI/OfficeCLI) v1.0.143, Apache-2.0 — see [NOTICE](./officecli/NOTICE.md) |

## `skills.json`

The manifest at the root decides what ships and what starts on:

```json
{ "name": "pdf", "include": true, "default_enabled": true }
```

- **`include`** — copy this folder into the image at build time. `false` keeps the skill in the
  repository for anyone who wants it, and out of the shipped image.
- **`default_enabled`** — a newly created Harness starts with this skill on. It is never a promise
  that it stays on: a Harness can switch any built-in off, and that choice always wins.

The folder name is the skill name and must match `name`.

## Adding a skill

1. Create a folder named for the skill, containing `SKILL.md` with `name` and `description` in its
   frontmatter. The description is what decides whether the skill gets loaded at all — write it as
   a list of the situations that should trigger it, and the ones that should not.
2. Declare what it needs. The build honours all three for every included skill:
   - `requirements.txt` — Python packages
   - `apt-packages.txt` — system packages, one per line
   - `install.sh` — anything else. Runs as root with network access, **at build time only**
3. Add an entry to `skills.json`.
4. Make sure it works without a network. A task has no internet access, so a skill that downloads a
   template or installs a package at run time fails in a way that looks like a broken tool.

## Licensing

The skills here are Apache-2.0, either written for this repository or vendored from an Apache-2.0
upstream with attribution preserved in a `NOTICE.md` recording what was changed.

Anthropic's `docx`, `pdf`, `pptx` and `xlsx` skills are deliberately **not** here. They are
source-available rather than open source, and their licence forbids copying them, distributing
them, and creating derivative works — which is exactly what bundling them into a distributed image
would be. Be careful with third-party skill collections: at least one popular Apache-2.0-labelled
repository ships those files verbatim, frontmatter still reading `license: Proprietary`. The label
on the repository does not change the licence on the file.
