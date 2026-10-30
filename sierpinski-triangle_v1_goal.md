# Goal: Sierpiński triangle with interactive parameters

Execute this goal using [onesession_method.md](onesession_method.md). Follow its Astra planning → Sol implementation → coordinator review sequence.

## Problem

Design and build a program that draws a Sierpiński triangle. Ask for drawing parameters through terminal prompts, showing useful defaults that the user can accept by pressing Enter.

## Target and constraints

- Resolve paths relative to the repository root.
- Target: `sierpinski-triangle_v1/`.
- Create the target directory when execution starts if it does not exist. It is a disposable product and working directory; inspect existing contents before reusing it.
- Keep all new deliverables inside the target folder.
- Keep both workflow chats in the current Codex project using the same local checkout.
- Astra chooses the language, drawing format, and practical parameter set, explaining these choices in `howto.md`.
- Use a simple, portable implementation with minimal dependencies.
- Preserve the separate v2 goal and reusable method documents.
- Do not publish, deploy, commit, or push as part of this goal.

## Acceptance criteria

1. A runnable program produces a recognizable Sierpiński triangle with repeated central triangular gaps.
2. Interactive prompts show useful defaults. Pressing Enter accepts each default without requiring manual values.
3. Users can change recursion depth, drawing size, triangle color, background color, and output destination. Custom values affect the saved result.
4. Invalid values produce clear feedback and allow correction. Bound recursion depth to prevent impractical rendering. Depth zero produces a solid triangle.
5. Save a viewable drawing and include a generated example. Handle output errors clearly and avoid overwriting existing files without confirmation.
6. Include a README with exact launch/use instructions, defaults and limits, output instructions, test commands, and limitations.
7. Perform appropriate geometry and parameter checks. Exercise default and custom input, invalid-input recovery, and output handling. Inspect the generated drawing and report actual evidence honestly.

## Required artifacts and ownership

- `sierpinski-triangle_v1_goal.md`: durable problem and acceptance criteria in the repository root, maintained by the coordinator. Preserve it when cleaning the disposable target directory.
- `howto.md`: plan written by Astra.
- Project files, generated example, README, and `result.md`: implementation and actual validation report written by Sol.

The requested workflow uses Astra for planning and Sol for implementation, with coordinator review. Keep execution identifiers, progress, and run history out of the reusable method.
