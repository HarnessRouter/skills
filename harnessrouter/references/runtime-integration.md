# Runtime integration

## Contents

- Build the server-side route
- Start a Response
- Upload files
- Stream and persist state
- Continue, cancel, and recover
- Handle errors and startup

## Build the server-side route

Create an authenticated product server route for every agent-powered feature. Never call
HarnessRouter from browser code.

```text
Product UI
  → authenticate user and tenant
  → authorize feature and files
  → map feature_key to approved harness_id
  → call HarnessRouter server-side
  → stream sanitized state
  → persist ownership and identifiers
  → return an authorized product contract
```

The browser may send `feature_key`, user input, and authorized product file references. The server
must resolve `harness_id`; reject arbitrary client-provided Harness IDs.

## Start a Response

Use the Harness ID as the first path segment:

```http
POST /{harness_id}/v1/responses
Idempotency-Key: <unique key for this new task>
```

```json
{
  "input": "Perform one bounded end-user job.",
  "stream": true
}
```

Generate a fresh idempotency key for every new task. Reuse it only when retrying that exact request.

## Upload files

1. Authorize the user and product file.
2. Upload server-side with `POST /v1/files`.
3. Reference the returned `file_id` in the schema-supported `input_file` content block.
4. Persist user/tenant, product file, Workspace, Harness, Session, and Response relationships.
5. Reject cross-user and cross-tenant file references.

Send only required context. Do not paste entire product databases, secrets, or hidden state into the
runtime input.

## Stream and persist state

Handle at least:

| Event | Product behavior |
|---|---|
| `response.created` | Immediately save Response ID, Session ID, user/tenant, feature, and Harness |
| `response.output_text.delta` | Append visible answer text |
| `response.reasoning_summary_text.delta` | Optionally show a safe progress summary |
| `response.output_item.added` | Show sanitized activity status |
| `response.output_text.annotation.added` | Record returned file metadata |
| `response.completed` | Finalize success and refresh Files |
| `response.incomplete` | Preserve partial work and offer Continue |
| `response.failed` | Show a sanitized classified failure |

Return a product-owned task/session identifier, not unrestricted HarnessRouter account objects.

## Continue, cancel, and recover

Continue the same goal using the existing Session and prior Response:

```json
{
  "input": "Apply the requested changes and update the artifacts.",
  "previous_response_id": "<response id>",
  "metadata": {"session_id": "<session id>"}
}
```

Cancel with `POST /v1/sessions/{session_id}/cancel` after product-level authorization.

After a stream disconnects following `response.created`:

1. Poll `GET /v1/sessions/{session_id}` until terminal.
2. Recover turns from `GET /v1/sessions/{session_id}/turns`.
3. Recover changed files from `GET /v1/sessions/{session_id}/files?changed=true`.
4. Do not submit a duplicate runtime task.

Use `GET /v1/sessions?harness={id}&limit=20` only server-side and never expose account-wide listings
as end-user history.

## Handle errors and startup

A new Session may use a warm sandbox or wait for fresh capacity. Treat lack of an initial event as
startup until the documented timeout or explicit error; do not duplicate the task.

API errors use a JSON `detail` field with standard HTTP status codes. Handle the documented invalid
request, unauthorized key, and missing/inaccessible resource cases. Add other status handling only
when declared by the deployed schema or response. Sanitize all upstream details returned to users.
