# Codex coordinator

Multi session workflow presenting coordination between Astra and Sol, with a Sierpiński triangle example.

<img src="assets/three-chat-slack.png" alt="Three-chat workflow: the coordinator manages Astra for planning and verification, and Sol for implementation." width="420">

## Run the v2 process

Three chats work together: a coordinator manages the process, Astra plans and
verifies, and Sol implements. They share one local checkout and pass work through files.

Open this repository as a Codex project with a local checkout. In a coordinator chat, send:

```text
@sierpinski-triangle_v2_goal.md.
```

The process runs in sequence: Astra writes `howto.md`, Sol implements the
graphical application and writes `result.md`, then Astra writes
`verification.md`. The coordinator reviews each stage and routes corrections
until acceptance passes or a blocker needs user input.

Use a Codex environment with separate-chat tools and both requested models
available. See [the v2 goal](sierpinski-triangle_v2_goal.md) for acceptance
criteria and [the coordinated method](coordinated_method.md) for the full process.

The project-local [`.codex/config.toml`](.codex/config.toml) uses `"approve"`
for Codex app MCP calls, including explicit overrides for chat creation and
follow-up messages, so v2 can coordinate without repeated approval prompts.
These settings require a trusted project; browser site permissions are separate.

## Run the v1 process

One chat handles planning, implementation, and review in sequence, using the
same assistant throughout. It builds the same graphical application with all stages kept in one conversation.

Open this repository as a Codex project with a local checkout. In one
coordinator chat, send:

```text
@sierpinski-triangle_v1_goal.md.
```

The assistant writes `howto.md`, builds and tests the graphical application,
then records actual validation in `result.md` and reviews the result.

All deliverables go into `sierpinski-triangle_v1/`. See [the v1 goal](sierpinski-triangle_v1_goal.md)
for acceptance criteria and [the one-session method](onesession_method.md) for
the full process.

Both goal files live in the repository root alongside the reusable methods.
Each run creates its corresponding `sierpinski-triangle_v1/` or
`sierpinski-triangle_v2/` directory for generated products, reports, and working
files. Those directories are disposable; preserve the root goal files, methods,
and this README when cleaning up a run.
