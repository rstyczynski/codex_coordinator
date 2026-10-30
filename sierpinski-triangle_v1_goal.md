# Goal: Sierpiński triangle with a graphical interface

Execute this goal using [onesession_method.md](onesession_method.md). Follow its Astra planning → Sol implementation → coordinator review sequence within the current chat session. For this goal, the role names describe stage responsibilities performed by the current assistant; do not create separate chats, spawn subagents, or switch models. This single-session requirement overrides the method's separate-chat dispatch instructions.

## Problem

Design and build a program that draws a Sierpiński triangle through a graphical interface. Let a user set parameters and see the drawing through graphical controls rather than terminal prompts.

## Target and constraints

- Resolve paths relative to the repository root.
- Target: `sierpinski-triangle_v1/`.
- Create the target directory when execution starts if it does not exist. It is a disposable product and working directory; inspect existing contents before reusing it.
- Keep all new deliverables inside the target folder.
- Keep all stages in the current chat, current Codex project, and same local checkout.
- Build the product independently using only this goal, its method, and files inside the target folder.
- Preserve reusable method documents.
- Do not publish, deploy, commit, or push as part of this goal.

## Acceptance criteria

1. A runnable graphical interface displays a recognizable, centered Sierpiński triangle with repeated central triangular gaps.
2. Clearly labeled graphical controls set recursion depth, drawing size, triangle color, and background color. Supply useful defaults and show an initial drawing without requiring parameter entry.
3. Provide actions to redraw with edited values and restore defaults. Custom values visibly affect the result. Depth zero produces a solid triangle.
4. Show clear in-interface feedback for invalid or impractical values and remain usable afterward. Bound recursion depth to keep rendering responsive.
5. Allow saving or downloading the drawing as SVG through the graphical interface.
6. Use a simple, portable implementation with minimal dependencies. Astra chooses and explains the technology. A locally running browser interface without a backend is acceptable; a desktop GUI is also acceptable if launch and verification are supported here.
7. Include a README with exact launch/use instructions, defaults and limits, export instructions, test commands, and limitations.
8. Perform appropriate geometry and parameter checks. Exercise the real graphical interface: default drawing, custom values, invalid-input recovery, reset, and export. Report evidence and limitations honestly.

## Required artifacts and ownership

- `sierpinski-triangle_v1_goal.md`: durable problem and acceptance criteria in the repository root, maintained by the coordinator. Preserve it when cleaning the disposable target directory.
- `howto.md`: plan written by Astra.
- Project files, README, and `result.md`: implementation and actual validation report written by Sol.

The requested workflow uses planning, implementation, and coordinator review within one chat. Reports must identify the stage and actual authoring model honestly. Keep execution identifiers, progress, and run history out of the reusable method.
