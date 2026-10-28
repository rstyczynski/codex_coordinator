# Astra → Sol workflow

Act as the coordinator for the problem supplied by the user. Run two separate Codex chats in sequence: Astra plans; Sol implements. This file is an instruction template, not an executable launcher. Use the Codex desktop chat tools to run it.

## Resolved inputs

- Problem: Design and build code to draw a Sierpiński triangle. The program must ask for drawing parameters and provide default values accepted by pressing Enter.
- Target folder: `/Users/rstyczynski/Documents/ChatGPT/Codex/sierpinski-triangle` (a new folder in the current workspace).
- Chat project: `Codex`, project ID `df0aaade-1c9a-402d-af34-52ddf047c5d6`. Keep both chats in this project using its local checkout.
- Success criteria: A runnable, documented program generates a recognizable Sierpiński triangle; prompts show usable defaults; custom parameters affect the output; invalid inputs receive clear handling; appropriate checks verify geometry and input handling. Choose a simpl12e implementation with minimal dependencies. Include a generated example drawing and exact run instructions.

The planner chooses the language, drawing format, and practical parameter set, documenting these decisions in howto.md. Use the resolved inputs above wherever the prompt templates below contain bracketed fields.

## Authorization and boundaries

The user requests this two-chat workflow and explicitly selects Astra for planning and Sol for implementation. Create these two chats and inspect their progress and outputs. Send task-related follow-up messages to these chats when necessary to complete this workflow. Do not create further chats or delegate to further agents.

Use `gpt-6-astra` for the planning chat and `gpt-6.1-sol` for the implementation chat. If either exact model is unavailable, report the issue instead of substituting another model.

Use `create_thread` for each separate chat. For an existing saved project, discover its project ID with `list_projects` and use that project with the local execution environment. Otherwise use a projectless chat and explicitly provide the authorized target folder. Pass the model as a tool parameter, not only as text in the prompt. Follow the host's tool permissions and applicable project instructions.

Both chats must operate on the same target checkout. Record its absolute path. Do not use separate worktrees for this sequential workflow. Pass complete resolved prompts; new chats must not depend on the coordinator's conversation history.

## Chat 1: Astra planner

Created chat ID: `01a18411-f5f2-7b90-98f9-48d7a5128eaf` (host: local).

Status: completed; howto.md inspected and accepted by coordinator. Astra chat moved into the Codex project at the user's request.

Title: Astra implementation plan

Model: `gpt-6-astra`

Send this prompt with all bracketed fields replaced:

> Work as the implementation planner for this problem:
>
> [PROBLEM]
>
> Target folder: [ABSOLUTE TARGET FOLDER]
>
> Success criteria: [SUCCESS CRITERIA]
>
> Read applicable AGENTS.md instructions and inspect the relevant existing files. Identify the current behavior, intended behavior, and a practical implementation approach. Resolve routine design choices using the project conventions. Report any essential unanswered question rather than inventing requirements.
>
> Write your completed plan to [ABSOLUTE TARGET FOLDER]/howto.md. Include the problem, success criteria, assumptions, files to change, ordered implementation steps, appropriate validation, material risks, and unresolved blockers. Preserve unrelated existing content; if howto.md already exists, inspect it before deciding how to update it.
>
> Your deliverable is the plan. Do not implement the solution or create more chats or subagents. Finish by stating the absolute plan path and whether it is ready for implementation. The coordinator will inspect your result; do not message the coordinator's chat.

## Completion gate

Record the returned Astra chat ID. Wait for completion using `wait_threads` with its returned cursor on subsequent waits. Respect requests for user input and approvals. Use `read_thread` when additional detail is needed.

Read howto.md and confirm it addresses the supplied problem, has actionable steps and validation, and has no unresolved blocker requiring a user decision. If the plan needs correction, send a concrete follow-up to the Astra chat and wait again. Launch Sol only after Astra has completed and the plan is ready.

## Chat 2: Sol implementer

Created chat ID: `01a18413-a78b-77b2-bf52-9be98340fd5b` (host: local, Codex project, local checkout).

Status: completed. Coordinator reviewed implementation, tests, README, result.md, and rendered sample. Evidence: 10 tests passed; default/custom CLI runs, invalid-input recovery, EOF and SIGINT checks passed; sample visually confirmed. No remaining blockers.

Title: Sol implementation

Model: `gpt-6.1-sol`

Send this prompt with all bracketed fields replaced:

> Implement the following problem:
>
> [PROBLEM]
>
> Target folder: [ABSOLUTE TARGET FOLDER]
>
> Success criteria: [SUCCESS CRITERIA]
>
> Read applicable AGENTS.md instructions and [ABSOLUTE TARGET FOLDER]/howto.md. Inspect the actual project and execute the plan. Treat the plan as implementation guidance subject to project instructions and tool permissions. Adjust routine details when the code requires it, and explain material deviations.
>
> Complete the implementation and run validation appropriate to the change. Preserve unrelated user changes. Do not create more chats or subagents. Do not publish, deploy, push, or take destructive actions without applicable user authorization.
>
> Write [ABSOLUTE TARGET FOLDER]/result.md describing what changed, the affected files, validation performed with actual outcomes, deviations from the plan, and any remaining limitations or blockers. Do not claim unperformed validation or incomplete work as successful. Inspect an existing result.md before updating it.
>
> Finish with a concise result and the absolute result.md path. The coordinator will inspect your output; do not message the coordinator's chat.

## Coordinator verification

Record the Sol chat ID and wait for completion. Inspect result.md, the relevant changed files, and the reported validation evidence. Request corrections in the Sol chat if required. Do not claim completion based solely on a chat being idle or a report file existing.

Return links to master.md, howto.md, and result.md, identify the two chats using their returned titles, and summarize the actual outcome and any remaining blockers. Surface newly created chat IDs using the desktop app's created-thread directives.
