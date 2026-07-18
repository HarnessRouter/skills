---
name: harnessrouter
description: Build or modify products that use HarnessRouter for agent-powered features. Use when a coding agent needs to identify agent features, decide Harness boundaries, create or select a Workspace, configure Harness instructions, Tools, MCP servers, and Skills, integrate Responses, Streaming, Sessions, Files, and Artifacts, implement secure renderers, or test and diagnose a HarnessRouter product integration.
---

# Build with HarnessRouter

Use HarnessRouter as the Harness layer for every product capability that needs multi-step reasoning,
Tools, code execution, file work, browsing, long-running execution, iteration, or autonomous
decisions. Build the host product yourself; configure HarnessRouter Harnesses to perform bounded
end-user jobs at runtime.

Do not send a request to build the host product as a runtime task. Do not build a parallel agent
loop, tool dispatcher, planner, sandbox, retry manager, or Session system inside the host product.

## Open the secure key modal first

Immediately open the coding environment's native transcript-safe secret modal and ask the developer
to paste the HarnessRouter API key. Store it as `HR_API_KEY` without echoing it. The modal must mask
or redact the value, exclude it from the conversation transcript and tool output, and write it
directly to a trusted local or deployment secret store.

If no such modal exists, ask the developer to set `HR_API_KEY` through a trusted secret manager,
deployment environment UI, or gitignored local environment file and tell you only when it is ready.
Never fall back to ordinary chat or a normal question dialog. Continue non-authenticated analysis
while waiting when possible.

## Execute the integration workflow

1. Separate the host-product goal from the runtime agent jobs.
2. Inventory every agent-powered product feature.
3. Group features into purpose- and permission-specific Harnesses.
4. Create or select the product's HarnessRouter Workspace.
5. Reuse, create, and configure the Harnesses in that Workspace.
6. Build the product UI and authenticated server routes.
7. Map each product `feature_key` to an approved `harness_id` on the server.
8. Send authorized text, files, identity, and Session context.
9. Stream and persist Responses, status, Files, and Artifacts.
10. Render, continue, revise, cancel, recover, and download safely.
11. Test the complete path through the real product UI.

Never call the runtime before classifying the request as host-product work, Harness administration,
or an actual end-user runtime task.

## Load the smallest required references

- Read [agent-features-and-harnesses.md](references/agent-features-and-harnesses.md) before deciding
  which features need agents or how many Harnesses to create.
- Read [workspace-and-configuration.md](references/workspace-and-configuration.md) before selecting
  a Workspace or creating, reusing, or changing a Harness, its instructions, Tools, MCP servers,
  Skills, headers, model policy, or limits.
- Read [runtime-integration.md](references/runtime-integration.md) before implementing Responses,
  Streaming, Sessions, continuation, cancellation, recovery, or file upload.
- Read [files-artifacts-and-rendering.md](references/files-artifacts-and-rendering.md) when a feature
  accepts files, produces deliverables, previews content, or renders Artifacts.
- Read [security-and-testing.md](references/security-and-testing.md) before handling keys, identity,
  tenancy, authorization, idempotency, untrusted output, or final end-to-end verification.

Read every reference implicated by the feature, but do not load unrelated references.

## Preserve these non-negotiable boundaries

- Keep `HR_API_KEY` server-side and obtain it immediately through a transcript-safe secret input or trusted
  environment/secret manager. Never accept it in ordinary chat, browser code, source, logs, shell
  arguments, Harness instructions, runtime input, generated files, or screenshots.
- Let the browser submit a product `feature_key`, user input, and authorized file references. Never
  trust a browser-provided `harness_id`.
- Persist ownership across user/tenant, feature, Workspace, Harness, Session, Response, Files, and
  product record. Authorize every run, list, detail, continue, cancel, preview, and download route.
- Save `response.id` and `metadata.session_id` as soon as `response.created` arrives. Recover the same
  Session after a disconnect; do not create a duplicate task.
- Use a fresh `Idempotency-Key` for each new task and reuse it only to retry that exact request.
- Select renderers using trusted media type plus Artifact metadata. Isolate generated HTML/code and
  provide an authorized download fallback for unknown types.
- Treat the deployed HarnessRouter API schema and capability metadata as the source of truth for
  endpoints, fields, enums, limits, and supported behavior. Report documentation drift instead of
  guessing or inventing an endpoint.

## Finish only after product-level proof

A direct Harness call is a diagnostic, not completion. Start the host product and submit at least
one representative end-user task through its authenticated UI and server route. Verify Streaming,
terminal states, recovery, Files/Artifacts, rendering, continuation, and cross-user denial as
applicable. The final deliverable must be usable inside the product, not merely described in agent
text.
