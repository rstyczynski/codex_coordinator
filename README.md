# Codex coordinator

A reusable planning, implementation, and verification workflow, with a Sierpiński triangle example.

## Run the v2 process

Open this repository as a Codex project with a local checkout. In a coordinator chat, send:

```text
Execute sierpinski-triangle_v2/goal.md.
```

The process runs in sequence: Astra writes `howto.md`, Sol implements the
graphical application and writes `result.md`, then Astra writes
`verification.md`. The coordinator reviews each stage and routes corrections
until acceptance passes or a blocker needs user input.

Use a Codex environment with separate-chat tools and both requested models
available. See [the v2 goal](sierpinski-triangle_v2/goal.md) for acceptance
criteria and [the coordinated method](coordinated_method.md) for the full process.
