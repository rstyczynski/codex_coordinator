# Goal: Sierpiński triangle with a graphical interface

Execute this goal using [coordinated_method.md](coordinated_method.md). Follow its Astra planning → Sol implementation → Astra verification sequence.

## Problem

Design and build a program that draws a Sierpiński triangle through a graphical interface. The original command-line code is acceptable as a geometry reference, but this version must let a user set parameters and see the drawing through graphical controls rather than terminal prompts.

## Target and reference

- Resolve the following paths relative to the repository root.
- Target: `sierpinski-triangle_v2/`.
- Create the target directory when execution starts if it does not exist. It is a disposable product and working directory; inspect existing contents before reusing it.
- Optional reference: `sierpinski-triangle_v1/`, if a previous v1 run exists. Keep it intact; the GUI must also be buildable without it.
- All new deliverables belong in the v2 folder.
- Keep both workflow chats in the current Codex project, using the same local checkout of this repository.

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

- `sierpinski-triangle_v2_goal.md`: durable problem and acceptance criteria in the repository root, maintained by the coordinator. Preserve it when cleaning the disposable target directory.
- howto.md: plan written by Astra.
- Project files and result.md: implementation and actual validation report written by Sol.
- verification.md: independent acceptance verification written by Astra after Sol finishes.

The user requests the coordinated workflow with Astra, Sol, and follow-up verification. Keep execution details out of coordinated_method.md. Do not publish, deploy, commit, or push.
