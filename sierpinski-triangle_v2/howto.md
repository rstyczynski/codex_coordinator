# Sierpiński triangle GUI implementation plan

Authoring role: Astra — planner, stage 1 of the coordinated workflow. This document is a plan, not implementation or verification evidence.

## Observed inputs and scope

Read `../coordinated_method.md`, `goal.md`, and the original project's Python implementation, tests, and README. The v2 folder contains only `goal.md` at planning time. No applicable `AGENTS.md` was found in the target/reference directories or their ancestor directories. Node and Python 3 executables are available locally; browser execution and downloads have not yet been tested.

The reference computes an equilateral triangle in a square image, uses midpoint subdivision retaining three corner triangles, and exports one polygon per terminal triangle. Reuse that geometry concept without modifying any reference files. All implementation, documentation, and retained evidence belong inside this v2 folder. Do not edit the goal, method, or this plan during implementation. Do not publish, deploy, commit, push, or create additional chats/subagents.

## Technology and intended behavior

Use plain HTML, CSS, and JavaScript with inline SVG. No framework, package installation, network resource, build step, or application backend is needed. SVG provides sharp previews and a direct export of the displayed geometry. Use classic scripts rather than browser ES modules so opening `index.html` directly works without module/file-origin restrictions. Keep geometry and validation independent of the DOM, exposing the same functions to browser code and Node's built-in test runner through a small conditional export.

Primary launch: open `index.html` in a modern browser. For repeatable local browser testing, serve this directory with Python's standard-library static server bound to `127.0.0.1`; this serves files only and is not an application backend. The browser tool can then visit the localhost URL. If the browser cannot access localhost or capture downloads, report the actual limitation and resolve it before claiming the corresponding acceptance check passed.

Show a compact control panel beside or above a centered preview, with visible labels, keyboard-accessible actions, focus indicators, and an accessible status/error region. Render immediately on load. Use these defaults and limits:

| Control | Default | Accepted value |
| --- | --- | --- |
| Recursion depth | 6 | Integer 0–8 |
| Drawing size (square, pixels) | 800 | Integer 100–4000 |
| Triangle color | `#1f2937` | Six-digit hexadecimal color |
| Background color | `#ffffff` | Six-digit hexadecimal color |

Provide editable numeric controls and visible hex color fields, optionally accompanied by synchronized native color pickers. Hex text fields make exact values, invalid-input feedback, and automation straightforward. Label limits beside controls. Actions: **Redraw**, **Restore defaults**, and **Download SVG**. Enter in the form should redraw. Reset restores all controls, clears errors, and immediately renders defaults.

Drawing size means both SVG width and height. Display at the requested CSS size when space permits, scaling down to fit the preview on smaller screens; show the current rendered pixel dimensions so large sizes remain unambiguous. A size change from 800 to 300 must visibly reduce the preview on an ordinary desktop viewport. Keep the triangle centered within its square image, not stretched by CSS.

Treat edits as pending until Redraw succeeds. Validate all values before building SVG: reject empty inputs, fractions, nonfinite values, out-of-range values, and malformed hex colors. Do not use permissive `parseInt` truncation. Normalize valid colors. Identify the offending field in visible feedback and retain the last valid drawing on failure. After correction, Redraw clears errors and works normally. Explain that export saves the last rendered drawing; pending or invalid inputs must never silently become an export. Identical foreground/background colors may be allowed with a visible warning that the triangle will be invisible.

## Geometry and export contract

For square size `s`, side length is `0.9*s`, triangle height is `sqrt(3)*side/2`, and top is `(s-height)/2`. Vertices are `(s/2, top)`, `(0.05*s, top+height)`, and `(0.95*s, top+height)`. Thus the triangle's bounding box is centered horizontally and vertically. At each level retain the three corner triangles formed by edge midpoints, omitting the central triangle. Depth 0 is one solid triangle; depth `d` has `3**d` terminal polygons, bounded at 6,561.

Produce a standalone SVG with namespace, explicit width/height, matching square viewBox, title, background rectangle, and filled polygons without strokes. Preserve sufficient coordinate precision to avoid visible seams. Use validated numbers/colors only when composing markup. Export the exact last successfully rendered SVG, including its background, via a Blob, object URL, and an anchor with a deterministic `.svg` download filename. Revoke object URLs after the browser has had time to consume them. Report download initiation honestly; do not claim filesystem completion merely because a click occurred.

## Files and ordered implementation steps

1. Create `geometry.js` with defaults, parameter validation, vertices/subdivision, and SVG generation. Keep functions deterministic and usable from Node without a DOM.
2. Create `test_geometry.cjs` using `node:test` and `node:assert/strict` for the focused checks below. No test dependency is needed.
3. Create `index.html` with labeled controls, the three actions, status/error feedback, and preview container. Create `styles.css` for readable responsive layout and visible focus/error states.
4. Create `app.js` for initial render, submission, reset, optional picker synchronization, rendered-state tracking, and SVG download. Validate before any expensive generation; update the preview atomically on success.
5. Run focused tests, then launch the actual interface and exercise every GUI check below. Capture useful screenshots and downloaded output under `evidence/` if supported. Avoid treating a generated SVG fixture as proof that the GUI download worked.
6. Write `README.md` with exact launch, use, export, and test instructions, defaults/limits, size behavior, last-rendered export semantics, and actual browser limitations. Write `result.md` identifying Sol as implementer and recording files, actual checks and outcomes, deviations, remaining limitations, and evidence paths. Do not write `verification.md`; Astra owns the later independent stage.

Suggested commands (README must reflect the final file names):

```sh
cd /Users/rstyczynski/Documents/ChatGPT/Codex/sierpinski-triangle_v2
node --test test_geometry.cjs
python3 -m http.server 8765 --bind 127.0.0.1
```

Visit `http://127.0.0.1:8765/` while the server runs. If the port is occupied, select another and record the actual URL. Also check direct file opening when supported. Stop the owned test server when finished unless it is deliberately left running for the user's preview and clearly reported.

## Acceptance checks and evidence

Geometry/parameter tests must establish equilateral outer geometry, centered bounds, finite coordinates, positive polygon areas, counts for depths 0, 1, 2, 6, and 8, and total filled area equal to outer area times `(3/4)**depth` within numerical tolerance. Check depth-one midpoint coordinates/central omission, size bounds 100 and 4000, custom colors and SVG dimensions/background. Reject depths -1, 9, 1.5, empty/nonnumeric values; sizes 99, 4001, fractions, empty/nonfinite values; and malformed colors. Verify validation occurs before recursion.

Exercise these through real browser controls, inspecting rendered appearance as well as DOM/SVG evidence where available:

| Goal criterion | Required observation |
| --- | --- |
| 1, 2: initial GUI | Fresh load shows default values and a centered recognizable triangle with repeated gaps, without interaction; 729 polygons and an 800-square SVG. Controls are clearly labeled and usable. |
| 3: custom values | Enter depth 3, size 300, triangle `#0055aa`, background `#fff4dd`; click Redraw. Observe changed geometry, smaller preview, colors, status/dimensions, and 27 polygons. |
| 3: depth zero | Set depth 0 and redraw; observe a solid equilateral triangle with one polygon. |
| 4: invalid recovery | Try depth 9, a fractional/empty depth, size 99/4001, and invalid hex text. Each rejected submission shows useful in-interface feedback and retains the previous valid drawing. Correct fields and redraw successfully without reloading. |
| 4: responsiveness | Render depth 8 and size 4000; verify 6,561 polygons, bounded behavior, and that controls/reset remain usable. Record observations/timing without inventing performance guarantees. |
| 3: reset | After custom values and an error, Restore defaults restores all four defaults, removes stale feedback, and redraws the default image. |
| 5: export | Render custom values; click Download SVG. Obtain the actual browser download, inspect valid standalone SVG dimensions/colors/polygon count, and open it to confirm appearance. Also verify pending edits do not change the exported rendered state. |
| 6: portability | Confirm local static launch with no fetched dependencies or build process; record browser and launch mode actually tested. Test direct-file launch if claiming it works. |
| 7: documentation | Follow README commands and compare documented defaults, limits, export semantics, and limitations to the implementation. |
| 8: evidence | Record focused test results plus the actual GUI interactions and screenshots/download evidence. Explicitly distinguish checks performed from checks merely planned. |

Also inspect a narrow viewport for clipped controls, distorted SVG, or unusable buttons. Keyboard focus and status feedback should remain legible. Independent verification later must inspect actual code and repeat essential GUI paths, rather than relying only on Sol's report.

## Assumptions, risks, and readiness

Assumptions: square SVG output and reference defaults suit the goal; a modern desktop browser is available; saving through the browser's standard download behavior is acceptable. These are routine choices and need no further user input.

Risks: depth-8 DOM generation can be slower on weaker devices; retain the cap and measure actual behavior. Native color dialogs can be awkward to automate, hence the visible editable hex fields. Responsive scaling can conceal size changes, hence natural-size previews and explicit dimensions. Browser tooling may handle file URLs or downloads differently; use localhost for controlled testing and disclose any missing evidence. Very fine triangles can blend at small preview sizes; SVG zoom preserves geometry.

Stage 1 readiness: ready for Sol implementation. No planning blocker found. Runtime/browser/export success remains to be established during implementation and independent verification.
