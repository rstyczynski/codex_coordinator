# Sierpiński triangle

An interactive Python program that writes a Sierpiński triangle to an SVG image.
Requires Python 3.9 or newer; no packages to install.

Run in a terminal:

```sh
cd /Users/rstyczynski/Documents/ChatGPT/Codex/sierpinski-triangle
python3 sierpinski.py
```

Each prompt shows its default in brackets. Press Enter (or enter only spaces)
to accept it. Invalid values produce an explanation and repeat the prompt.

| Parameter | Default | Accepted values |
| --- | --- | --- |
| Recursion depth | `6` | Whole number, 0–8 |
| Image width | `800` | Whole number, 100–4000 pixels; height equals width |
| Triangle color | `#1f2937` | `#` followed by six hexadecimal digits |
| Background color | `#ffffff` | `#` followed by six hexadecimal digits |
| Output SVG path | `sierpinski.svg` | Filename ending in `.svg` (case-insensitive) |

Relative paths use the terminal's current directory. Paths can contain spaces;
enter them without surrounding quotes at the interactive prompt. `~` expands
to your home directory. The parent directory must already exist. The program
prints the absolute output path and triangle count when it succeeds.

An existing destination triggers `Overwrite? [y/N]`. Enter means No and returns
to the path prompt. Enter `y` or `yes` to replace the file. Write failures also
return to the path prompt. Files are written through a temporary file in the
destination directory; existing content is replaced only after a complete write.
A destination created concurrently is protected when overwrite was not approved.
Replacing a symbolic link replaces the link itself. New-file publication uses
hard links, so the destination filesystem must support them; otherwise choose
a path on a filesystem that does. Ctrl-C or EOF cancels with exit status 1 and
no traceback; successful generation exits with status 0.

The drawing starts with an equilateral triangle centered on a square background,
with its side 90% of the image width. Each subdivision keeps three corner
triangles and leaves the central triangle empty. Depth 0 is solid; depth `d`
contains `3**d` polygons. Depth 8 produces 6,561 polygons. At small image sizes
and high depths, zoom in to see the smallest details.

Open the included [sample.svg](sample.svg) using a browser's Open File command.
On macOS, you can also run `open sample.svg` from this directory.

Generate the included default drawing on a fresh destination:

```sh
cd /Users/rstyczynski/Documents/ChatGPT/Codex/sierpinski-triangle
printf '\n\n\n\nsample.svg\n' | python3 sierpinski.py
```

Because the sample is already included, rerunning this command asks for overwrite
confirmation and then reaches EOF. To deliberately regenerate the included file:

```sh
printf '\n\n\n\nsample.svg\nyes\n' | python3 sierpinski.py
```

Custom example (use a fresh destination, or run interactively to confirm overwrite):

```sh
cd /Users/rstyczynski/Documents/ChatGPT/Codex/sierpinski-triangle
printf '3\n600\n#0055aa\n#fff4dd\ncustom.svg\n' | python3 sierpinski.py
```

Run the focused geometry, SVG, input, and filesystem tests:

```sh
cd /Users/rstyczynski/Documents/ChatGPT/Codex/sierpinski-triangle
python3 -m unittest -v test_sierpinski.py
```
