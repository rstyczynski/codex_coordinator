# Sierpiński triangle implementation plan

## Scope and inspected state

Build an interactive, documented program that draws a recognizable Sierpiński triangle. Every drawing prompt must display a useful default and accept it when the user presses Enter. Custom values must affect the generated drawing, and invalid input must receive clear feedback.

Shared target folder: `/Users/rstyczynski/Documents/ChatGPT/Codex/sierpinski-triangle`.

The planner read `/Users/rstyczynski/Documents/ChatGPT/Codex/master.md`. The target folder was empty on inspection. No `AGENTS.md` was found in the target or its ancestor directories. Recheck instructions and existing files before implementation and preserve any subsequently added content. This plan is the only planner deliverable; no implementation or sample has yet been created.

## Decisions and assumptions

- Use Python 3.9+ and only its standard library. Do not install packages or require a GUI framework.
- Write an SVG file, which can be opened in a browser and scales cleanly. Do not automatically launch a browser.
- Use deterministic recursive subdivision of an equilateral triangle: compute its three edge midpoints and recurse into the three corner triangles, omitting the central triangle. At depth zero emit one filled polygon. Depth `d` therefore produces exactly `3**d` polygons.
- Use a square SVG canvas, matching its width and height, with an explicit viewBox. Set a margin of 5% of the canvas width. The outer triangle's side is 90% of the width; its height is `sqrt(3) / 2 * side`. Center it horizontally and vertically, with its apex up. Use no polygon strokes.
- Prompt in English. Whitespace-only input selects the default. Reprompt after invalid input rather than terminating with a traceback.
- Avoid adding unrelated features, randomness, animation, image-library dependencies, or an elaborate command-line interface.

### Interactive parameters

| Prompt | Default | Accepted values |
| --- | --- | --- |
| Recursion depth | `6` | Integer from `0` through `8` inclusive |
| Image width in pixels | `800` | Integer from `100` through `4000` inclusive |
| Triangle color | `#1f2937` | Exactly six hexadecimal digits prefixed with `#` |
| Background color | `#ffffff` | Exactly six hexadecimal digits prefixed with `#` |
| Output SVG path | `sierpinski.svg` | A nonempty filename ending in `.svg`, case-insensitive; relative paths resolve against the process working directory |

Depth 8 caps output at 6,561 triangles. Explain that at high depth on a small canvas, details may only become visible when zooming. Accept uppercase hex colors, optionally normalizing their case. Escape the displayed default convention consistently, e.g. `Recursion depth [6]: `.

Expand `~` in user-entered paths. Require the parent directory to exist and report directories, missing parents, and unsupported suffixes clearly. Do not create directories implicitly. If a destination already exists, explicitly offer overwrite with a default of No; declining returns to the output-path prompt. Catch write failures and allow choosing another path. Catch EOF or Ctrl-C at the entry point and exit with a short cancellation message and a nonzero status, without a traceback. Never treat an empty input stream as an unlimited sequence of defaults.

## Files to create

All paths below are relative to the shared target folder:

- `sierpinski.py`: executable entry point plus separately callable geometry, SVG generation, validation, and prompt helpers. Protect the entry point with `if __name__ == '__main__'` so importing does not prompt.
- `test_sierpinski.py`: focused standard-library `unittest` checks using temporary directories and mocked input/output where appropriate.
- `README.md`: requirements, exact commands, prompt/default table, output-path semantics, overwrite behavior, limitations, and how to view the sample.
- `sample.svg`: generated example using depth 6, width 800, and the default colors.
- `result.md`: implementation report required by the master workflow, including actual validation outcomes and any deviations or remaining blockers.

Preserve `howto.md`. No dependency manifest is needed for a standard-library program.

## Ordered implementation steps

1. Reinspect the target and applicable instructions. Confirm `python3` is available and record its version; if unavailable, report that validation blocker rather than claiming tests passed.
2. Implement pure geometry helpers for outer vertices, midpoints, and recursive subdivision. Keep computations in floating point and round only during SVG serialization, to at least six decimal places or comparable precision. Validate public drawing inputs so direct calls cannot bypass depth, size, and color bounds.
3. Implement SVG serialization with the SVG namespace, explicit width, height and viewBox, one full-canvas background rectangle, and one polygon per terminal triangle. Restrict colors to the validated hex format. Prefer an iterator for terminal triangles; collecting at most 6,561 polygons is also acceptable.
4. Implement reusable integer and color prompts with visible defaults, whitespace handling, bounds, and actionable error messages. Implement the output-path prompt and explicit overwrite handling. On success print the resolved absolute path and triangle count.
5. Add the focused tests described below. Use temporary locations so tests cannot overwrite user files. Ensure cancellation and write errors do not produce tracebacks in normal CLI use.
6. Run the automated checks and interactive smoke runs. Generate `sample.svg` through the implemented program using defaults for the four drawing parameters and `sample.svg` for the output path. Inspect its actual appearance using an available SVG-capable viewer; do not infer appearance solely from the test suite. If no viewer is available, disclose that limitation and retain structural validation results.
7. Write `README.md` and `result.md` with exact commands, observed outcomes, the generated sample, limitations, and material deviations. Do not create chats/subagents, publish, deploy, or push changes.

## Validation and acceptance evidence

### Geometry and SVG

- Depths 0, 1, 2, 6, and 8 yield respectively 1, 3, 9, 729, and 6,561 polygons.
- Outer triangle edges have equal length within a numerical tolerance. All vertices lie inside the canvas margins.
- At depth 1, verify the expected midpoint vertices for each of the three corner triangles and that no central polygon is emitted.
- Verify terminal triangle areas are positive and their summed area equals the initial area times `(3/4)**depth`, within a tolerance. This supplements counts with a geometric check.
- Parse generated SVG using `xml.etree.ElementTree`; assert namespace, dimensions, viewBox, background rectangle, polygon count, triangle fill, and finite polygon coordinates.
- Visually inspect the default sample for an upward equilateral triangle with repeated central triangular gaps, centered on its background. Depth zero must be solid.

### Inputs and filesystem behavior

- Enter/whitespace selects defaults and each prompt includes its default.
- Valid custom depth, width, and colors survive into SVG attributes/counts.
- Nonnumeric and fractional integers, out-of-range depths/widths, and malformed colors show an error and reprompt; boundary values are accepted.
- Validate missing parent directories, directory destinations, wrong suffixes, default/relative paths, and paths containing spaces.
- Existing output remains unchanged if overwrite is declined; affirmative overwrite succeeds. Exercise a write error through mocking if reproducing permissions is unreliable.
- EOF and Ctrl-C exit cleanly without generating a traceback or looping indefinitely.

### Exact commands to document and execute

Run from a terminal:

```sh
cd /Users/rstyczynski/Documents/ChatGPT/Codex/sierpinski-triangle
python3 sierpinski.py
```

Press Enter at each of the five prompts to use all defaults on a fresh run. If the default output already exists, the extra overwrite prompt defaults to No.

Run tests:

```sh
cd /Users/rstyczynski/Documents/ChatGPT/Codex/sierpinski-triangle
python3 -m unittest -v test_sierpinski.py
```

Generate the sample on a fresh destination:

```sh
cd /Users/rstyczynski/Documents/ChatGPT/Codex/sierpinski-triangle
printf '\n\n\n\nsample.svg\n' | python3 sierpinski.py
```

Exercise custom values on a fresh destination:

```sh
cd /Users/rstyczynski/Documents/ChatGPT/Codex/sierpinski-triangle
printf '3\n600\n#0055aa\n#fff4dd\ncustom.svg\n' | python3 sierpinski.py
```

Use a temporary directory for the custom smoke-run output, or remove only implementation-owned temporary artifacts afterward. Open `sample.svg` in a browser using its Open File command. On macOS the user can also run `open sample.svg` from the target folder; automated GUI opening must follow tool permissions.

## Risks and blockers

- Polygon growth is exponential; the depth cap bounds time and file size.
- Very small triangles may blend at normal display size; SVG zoom preserves detail.
- Python availability/version and successful visual inspection remain implementation-time checks.
- The target is outside this planning chat's writable roots. Writing this plan requires the host's permission mechanism; the implementer must likewise honor its own permissions for this target. User workflow authorization does not bypass tool permissions.
- No essential design question or user decision remains unresolved. The plan is ready for implementation once saved successfully.
