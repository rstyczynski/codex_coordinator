# Sierpiński Studio

A small, dependency-free browser interface for drawing and downloading a Sierpiński triangle. Implementation author: Sol.

## Launch

From a terminal, run exactly:

```sh
cd /Users/rstyczynski/Documents/ChatGPT/Codex/sierpinski-triangle_v2
python3 -m http.server 8765 --bind 127.0.0.1
```

Open [the local app](http://127.0.0.1:8765/) in a modern browser. Keep the terminal running; Ctrl+C stops the server. If port 8765 is already occupied by this app, reuse it; otherwise choose another free port and use that port in the URL. The server only serves static files. No installation, build process, framework, remote resources, or application backend is required.

The classic scripts are also designed for opening `index.html` directly in a browser. This launch mode was **not verified**: the available browser automation permits only HTTP(S), and rejected the `file:` URL. Use the tested localhost launch above for repeatable results.

## Use

The initial drawing appears immediately. Edit the four labeled fields, then select **Redraw**, or press Enter within the form. Edits remain pending until a redraw succeeds.

| Parameter | Default | Limit |
| --- | --- | --- |
| Recursion depth | 6 | Whole number 0–8 |
| Drawing size | 800 px | Whole number 100–4000 px |
| Triangle color | `#1f2937` | `#` followed by six hexadecimal digits |
| Background color | `#ffffff` | `#` followed by six hexadecimal digits |

Depth zero produces one solid triangle. Each additional depth replaces every triangle with its three corners, leaving a central gap. Depth 8 contains 6,561 polygons. Invalid values show a field-specific error and preserve the last valid drawing. Correct the field and redraw, or select **Restore defaults** to reset all controls and redraw immediately. Matching triangle/background colors are permitted with a visible warning.

Size determines both dimensions of the exported square SVG. The preview uses that size when space permits and scales down proportionally to fit smaller screens. Its heading always reports the actual SVG dimensions. A 300 px drawing is visibly smaller than an 800 px drawing on a desktop. Controls stack above the preview on narrow screens; scroll vertically to reach the drawing.

## Export

Select **Download SVG**. The browser saves a standalone SVG with its background and a filename such as `sierpinski-depth-3-300px.svg`. Browser settings determine the download destination or whether a Save dialog appears.

The download always contains the **last successfully rendered drawing**, including when current fields contain pending or invalid edits. Select Redraw first to apply those edits. The status reports a download request; it cannot independently confirm the browser's filesystem save. Open the SVG in a browser or vector editor to view or zoom without losing resolution.

## Tests

Node 18 or newer is sufficient for the built-in test runner. No packages are needed:

```sh
cd /Users/rstyczynski/Documents/ChatGPT/Codex/sierpinski-triangle_v2
node --test test_geometry.cjs
```

The nine focused tests cover geometry, area, counts through depth 8, depth-one midpoint omission, size bounds, SVG metadata/colors, and rejection before recursion. Real GUI observations and screenshots are in [result.md](result.md) and `evidence/`; those are recorded manual automation observations, not a separate unattended browser test suite.

## Files and limitations

`geometry.js` contains deterministic geometry, validation, and SVG generation; `app.js` manages controls and exports; `index.html` and `styles.css` provide the interface. `test_geometry.cjs` uses Node's built-in assertions.

Tested in the Codex ChatGPT in-app browser on macOS, with Node v26.4.0 and Python 3.14.7. Other browsers and direct-file launch have not been exercised. Very fine triangles may blend when scaled down; zoom the exported SVG to inspect them. Rendering time varies by device. The cap limits work to 6,561 polygons. No persistence, undo history, PNG export, or native color-picker dialog is included.
