# Workspace and Harness configuration

## Contents

- Select the Workspace
- Reuse, create, or update Harnesses
- Configure instructions
- Configure Tools and MCP
- Configure Skills
- Preserve API conventions

## Select the Workspace

Use one Workspace as the product/project and environment boundary. Reuse the Workspace that
represents the intended product and environment; otherwise create one through a documented API or
the HarnessRouter Dashboard. Do not invent a Workspace endpoint.

Separate products, customers, and environments when their data, credentials, permissions, or
operations require isolation. Use a Workspace-scoped API key.

## Reuse, create, or update Harnesses

1. Call `GET /v1/harnesses`.
2. Compare purpose, instructions, data, Tools/MCP, Skills, permissions, model policy, limits, and
   output contract with the Harness plan.
3. Reuse only a genuine match.
4. Update the canonical Harness only when the change remains compatible with callers.
5. Otherwise create with `POST /v1/harnesses`.
6. Persist the returned `harness_id` in server-side product configuration.

Use `GET /v1/models` and `GET /v1/harnesses/{id}/models`; do not permanently hardcode a model name.
Use `GET | PUT | DELETE /v1/harnesses/{id}` only according to the deployed schema.

## Configure instructions

Define:

1. One runtime job and its allowed inputs.
2. Out-of-scope work that returns `role_mismatch`, including building the host product.
3. Allowed data, Tools, external services, and side effects.
4. Prohibited actions and approval gates.
5. Exact output and Artifact contract: primary file, supporting files, entry point, relationships,
   media types, and verification result.
6. A requirement to save deliverables as real working-directory files.
7. Completed, incomplete, and failure behavior the product can handle.
8. A prohibition on secrets and user-facing `localhost` links.

## Configure Tools and MCP

- Enable only the Tools required by the Harness purpose.
- Prefer read-only and least-privilege access.
- Store fixed external credentials with `PUT /v1/mcp-secrets/{short-name}`; never embed them.
- Put consequential writes behind product approval or a separate Harness.
- Use `additional_headers[]` to declare supported per-request identity header names. Send values only
  from the authenticated product server and reference them with the deployed `$headers.<Name>`
  syntax. Never store the values in Harness configuration.
- Prove Tool discovery and one narrow call. Verify visible handling of missing permission, missing
  secret, timeout, and downstream failure.

## Configure Skills

Skills are folder bundles:

```json
{
  "name": "contract-review",
  "files": [
    {"path": "SKILL.md", "content": "---\nname: contract-review\ndescription: ...\n---\n..."},
    {"path": "references/rubric.md", "content": "..."}
  ]
}
```

Preserve relative paths and use `content_b64` for binary files. The root `SKILL.md` requires YAML
`name` and `description`. Install only purpose-required Skills.

Large bundles can round-trip as opaque `{name, enabled, blob}` entries. Preserve these unchanged
when updating unrelated configuration. Read actual files with
`GET /v1/harnesses/{id}/skills/{name}/files` before editing or verification. Inspect capability
metadata before duplicating built-in DOCX, PDF, PPTX, or XLSX Skills. Verify behavior with a
representative task, not file presence alone.

## Preserve API conventions

- Requests use snake_case such as `default_model`, `mcp_servers`, and `max_step`.
- Stored Harness responses use camelCase such as `defaultModel`, `mcpServers`, and `maxStep`.
- Do not copy response objects directly into update requests.
- Retrieve and preserve every field not intentionally changed. A partial UI model must not erase
  Tools, Skills, headers, secret references, limits, or model policy.
- Null `maxStep` or `timeoutSeconds` uses runtime defaults. Confirm the current values from deployed
  capability metadata before enforcing them as product policy.
- Treat the deployed schema as exact truth; treat this reference as workflow guidance.
