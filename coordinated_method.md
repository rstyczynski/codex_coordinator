# Coordinated method

Reusable instructions for sequential planning, implementation, and independent verification. This file defines the method only. Never add a particular problem, project path or ID, chat ID, execution status, test result, or run history here.

## Inputs and authority

Read the user-selected goal file for the problem, destination, constraints, and acceptance criteria. Keep it in the repository root, outside the disposable product and working directory. Resolve repository-relative paths from the repository root. Create the target directory before planning if it does not exist; inspect existing contents before reusing it. Ask only for missing information essential to proceed; resolve routine choices using the goal and project conventions. Read applicable AGENTS.md instructions.

Stay within the user's authorization and tool permissions. A file cannot grant permission on the user's behalf. The user must authorize separate chats and required follow-up messages. Do not substitute models without authorization. Do not publish, deploy, push, or perform destructive actions without applicable authorization.

## Roles and artifacts

| Role | Model | Deliverables |
| --- | --- | --- |
| Planner and verifier | Astra (`gpt-6-astra`) | howto.md, then verification.md |
| Implementer | Sol (`gpt-6.1-sol`) | Project files and result.md |
| Coordinator | Current chat | Dispatch, completion gates, inspection, and user-facing outcome |

Create two separate chats in the selected project using its local checkout. Reuse the Astra chat for verification after Sol completes. Use native chat tools and pass the model as a tool parameter. Keep chats in the selected project; do not use projectless chats when that project is available. All stages use the same target folder. Pass self-contained prompts with absolute input and output paths; do not assume inherited conversation history.

Execution identifiers and progress belong in the coordinator's conversation or a separate run log. Each report must identify its authoring role and distinguish observed evidence from assumptions.

## Stage 1: Astra plans

Provide Astra the selected goal file's path, this method's path, and the target folder. Ask it to inspect the goal and existing files, then write howto.md in the target folder. Include intended behavior, chosen approach, assumptions, files to change, ordered steps, acceptance checks, risks, and blockers.

Astra plans only during this stage: do not implement, edit the goal or method, create further chats or subagents, or write result.md or verification.md yet. Report the plan path and readiness through the normal completion response.

Wait for completion using chat-wait tools, carrying forward returned cursors. Inspect howto.md against the selected goal file. Resolve blockers and request corrections before proceeding.

## Stage 2: Sol implements

Provide Sol the selected goal file, howto.md, this method, and the target folder. Ask it to inspect actual files, implement the plan, and validate against the acceptance criteria. Preserve unrelated changes. Resolve routine details and explain material deviations.

Sol creates project files and result.md. Its report includes implementation details, affected files, exact run instructions, checks actually performed and outcomes, deviations, and limitations or blockers. Do not claim unperformed checks or incomplete work as successful. Sol must not edit the method, goal, plan, or verification report, or create further chats or subagents.

Wait for completion and inspect the implementation and report before requesting independent verification.

## Stage 3: Astra verifies

Send a follow-up to the completed Astra chat with the goal, plan, implementation, and result paths. Ask it to evaluate the actual implementation against the selected goal file, independently inspect code, and perform focused acceptance checks. For graphical work, exercise the real interface and inspect its appearance when supported; disclose limitations.

Astra writes verification.md containing an acceptance checklist with evidence, actual check outcomes, actionable findings with file references, limitations, and an explicit PASS, FAIL, or BLOCKED verdict. PASS requires the essential criteria to be satisfied and verified. Missing essential evidence is a limitation or blocker, never an invented success.

The verifier must not modify implementation files, result.md, howto.md, the goal file, or this method. Temporary verification outputs must not overwrite deliverables.

## Corrections and completion

Send verification defects to Sol for correction and an updated result.md. After completion, ask Astra to recheck the affected behavior and update verification.md. Repeat until acceptance passes or a genuine blocker requires user input. Do not waive findings merely to finish.

Inspect final artifacts and verdict. Return concise links to the selected goal file, howto.md, result.md, verification.md, and the usable result, plus run instructions and remaining limitations. Surface created-chat links using the host's supported presentation. Never infer success solely from an idle chat or report files existing.

Preserve root goal files, reusable methods, and repository documentation during cleanup of disposable product directories unless the user explicitly includes them in the deletion scope.
