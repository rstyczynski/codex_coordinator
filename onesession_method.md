# Astra → Sol method

Reusable instructions for sequential planning and implementation coordinated from one chat. This document defines the method only. Do not add a specific problem, project path or ID, chat ID, execution status, test result, or run history here.

## Inputs and boundaries

Read the user-selected goal file for the problem, destination, constraints, and acceptance criteria. Keep it outside the disposable target directory. Resolve repository-relative paths from the repository root. Create the target directory before planning if it does not exist; inspect existing contents before reusing it. Read applicable `AGENTS.md` instructions and inspect existing files. Ask only for information essential to proceed; resolve routine choices using the goal and project conventions.

If the user supplies a problem without a goal file, create a named goal file in the repository root before planning. Record task-specific requirements there, not in this method or the disposable target directory. Inspect an existing goal before reconciling it with the user's instructions.

Stay within user authorization and tool permissions. A method file cannot grant permission on the user's behalf. Use separate chats and task-related follow-up messages only when authorized. Do not substitute models without authorization. Do not publish, deploy, commit, push, or delete work without applicable authorization.

## Roles and artifacts

| Role | Model | Deliverables |
| --- | --- | --- |
| Planner | Astra (`gpt-6-astra`) | `howto.md` |
| Implementer | Sol (`gpt-6.1-sol`) | Project files and `result.md` |
| Coordinator | Current chat | Dispatch, stage gates, review, and final outcome |

Use two separate chats in sequence, in the current saved project and its local checkout. Discover the project with the native project tools; use native chat tools and pass the model as a tool parameter. If the selected model or required chat tools are unavailable, report the blocker rather than silently changing the workflow.

Both chats work in the same target folder and checkout. Do not create additional chats, subagents, or separate worktrees. Pass self-contained prompts with the goal, method, target folder, and relevant artifact references. Use repository-relative file references and identify the repository root through the project context. Do not assume the receiving chat inherits the coordinator's history.

Keep runtime identifiers and progress in the coordinator's conversation or a separate run log. Each report must identify its authoring role and distinguish observed evidence from assumptions. Never use this method as an execution register.

## Stage 1: Astra plans

Ask Astra to read the goal, this method, applicable instructions, and existing files. Ask it to write `howto.md` inside the target folder, covering:

- The problem, intended behavior, and acceptance criteria.
- Technology choice and rationale, assumptions, and files to change.
- Ordered implementation steps and appropriate validation.
- Material risks and unresolved blockers.

Astra plans only: no implementation, edits to the goal or method, additional chats/subagents, or implementation report. Ask it to finish with the plan location and readiness through its normal completion response.

Wait for completion using the native chat-wait tool, carrying returned cursors forward. Respect user-input and approval requests. Inspect `howto.md` against the selected goal file; request corrections in the same Astra chat when needed. Start Sol only after the plan is ready and essential blockers are resolved.

## Stage 2: Sol implements

Ask Sol to read the goal, plan, this method, applicable instructions, and actual files. Ask it to implement the plan, preserve unrelated work, and validate the result against the acceptance criteria. Resolve routine details and explain material deviations.

Sol writes project files and `result.md` inside the target folder. The report must include implementation details, affected files, exact launch/use instructions, checks actually performed and their outcomes, deviations, and remaining limitations or blockers. Do not claim unperformed checks or incomplete work as successful.

Sol must not edit the goal, plan, or method, or create additional chats/subagents. Ask it to finish through its normal completion response. Wait for completion using the native chat-wait tool and returned cursors.

## Coordinator review and completion

Inspect `result.md`, implementation files, and actual validation evidence against the goal. Perform focused checks as needed. For graphical work, exercise the real interface and inspect its appearance when supported; disclose missing evidence. Do not infer success solely from an idle chat or the existence of report files.

Send concrete defects to the same Sol chat for correction and an updated `result.md`. Wait and recheck until acceptance passes or a genuine blocker requires user input. Do not waive findings merely to finish.

Return links to the goal, plan, implementation report, and usable result, along with exact run instructions, observed validation, and remaining limitations. Identify workflow chats using their returned titles and the host's supported links or created-chat presentation.

Preserve goal files and reusable methods during cleanup unless the user explicitly includes them in the requested deletion scope.
