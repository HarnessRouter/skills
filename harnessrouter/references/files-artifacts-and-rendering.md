# Files, Artifacts, and rendering

## Contents

- Retrieve files securely
- Define the Artifact contract
- Select renderers
- Isolate active content

## Retrieve files securely

- List with `GET /v1/sessions/{session_id}/files`.
- Use `?changed=true` for files changed by the latest turn.
- Retrieve with `GET /v1/containers/{session_id}/files/{file_id}/content` according to the deployed
  schema.
- Proxy previews and downloads through authenticated product server routes after checking ownership.
- Treat returned `download_url` values as attachment downloads, not inline-display URLs.
- Fetch bytes server-side and return an authorized blob or safe text representation for preview.
- Where supported, request the server-converted PDF preview for DOCX, PPTX, and XLSX by replacing
  `/content` with `/pdf` on the same authorized content route. Retain the original download.

## Define the Artifact contract

Configure the Harness to return enough metadata for deterministic product behavior:

```text
artifact type
primary file
supporting files
entry point
trusted/verified media types
directory and dependency relationships
verification status
available product actions
```

Do not infer the entry point or file relationships solely from filenames or agent prose when the
Harness can return explicit metadata. Preserve directories for multi-file projects.

## Select renderers

Use trusted media type plus Artifact metadata to render:

- Markdown and plain text;
- structured JSON;
- source code;
- Diff/Patch;
- directory trees;
- generated HTML applications;
- images;
- PDF;
- DOCX/PPTX/XLSX previews plus original download;
- CSV/XLSX data;
- multi-file projects;
- unknown or unsafe types.

For unknown types, show sanitized metadata and an authorized download. Never execute them.

For a single-file HTML app, use the declared entry point, commonly `index.html`. For a multi-file
project, preserve directories, identify the entry point, and provide a complete archive download.

## Isolate active content

Render generated HTML in a sandboxed iframe without parent credentials, same-origin privileges, or
privileged browser APIs. Do not inject generated scripts into the product DOM. Treat source code as
text unless the product has an explicit isolated execution environment. Apply size limits and safe
fallbacks before loading large files into the browser.
