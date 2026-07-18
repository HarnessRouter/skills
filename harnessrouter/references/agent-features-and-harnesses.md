# Agent features and Harness boundaries

## Contents

- Classify the request
- Inventory agent-powered features
- Decide Harness boundaries
- Plan multi-Harness handoffs

## Classify the request

Separate three jobs before making an API call:

- **Host-product work:** build or modify the product, UI, server, auth, data flow, integration,
  renderer, and tests in the user's project.
- **Harness administration:** inspect, create, update, or verify Workspace/Harness configuration.
- **Runtime task:** execute one bounded end-user job through an already integrated product feature.

Write two statements:

```text
Host-product goal: <the product and user workflow to build>
Runtime agent jobs: <the bounded jobs Harnesses perform for end users>
```

Never send the host-product goal as a runtime task.

## Inventory agent-powered features

Use HarnessRouter when a capability needs multi-step reasoning, Tools, code execution, files,
browsing, long-running work, iteration, or autonomous decisions. A truly single-shot text
transformation with no Tools, files, persistence, or multi-step work may remain on an existing raw
model path.

Create an inventory before creating Harnesses:

| Feature key | User action | Agent job | Inputs | Outputs | Data/Tools | Risk |
|---|---|---|---|---|---|---|
| `contract_intake` | Upload contract | Extract and normalize | PDF/DOCX | JSON + summary | File read | Low |
| `contract_review` | Review | Find risks and propose edits | Contract + policy | Findings + redline | Files + policy | Medium |
| `review_qa` | Verify | Check coverage and claims | Review files | QA report | Read-only files | Low |

Count runtime responsibilities, not buttons or screens.

## Decide Harness boundaries

A Harness is one reusable runtime configuration with a coherent purpose and permission boundary.
Create separate Harnesses when any of these differ materially:

- purpose or definition of success;
- instructions or domain workflow;
- allowed product data or tenant scope;
- Tools, MCP servers, Skills, or credentials;
- read-only versus write/publish permissions;
- model, cost, latency, step, or timeout policy;
- output and Artifact contract;
- risk, approval, or compliance boundary.

Reuse one Harness when all important boundaries match. Do not create a Harness per button and do not
put unrelated features into one all-powerful Harness.

Plan each Harness before changing configuration:

```text
Name:
Feature keys:
Purpose:
Allowed inputs/data:
Required outputs and Artifact entry point:
Instructions:
Tools/MCP/Skills:
Permissions and approval gates:
Model/limits:
Failure and incomplete behavior:
```

## Plan multi-Harness handoffs

Pass only the minimum verified Artifact or structured output required by the next Harness. Persist
the relationship in the host product. Do not grant a downstream Harness the upstream Harness's
Tools or permissions merely because they participate in the same workflow. Make the product server,
not agent prose, decide which Harness runs next.
