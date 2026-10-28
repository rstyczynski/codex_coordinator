#!/usr/bin/env python3
"""Draw a Sierpiński triangle as SVG using only the Python standard library."""

import math
import os
from pathlib import Path
import re
import tempfile


DEFAULT_DEPTH = 6
DEFAULT_WIDTH = 800
DEFAULT_TRIANGLE = "#1f2937"
DEFAULT_BACKGROUND = "#ffffff"
DEFAULT_OUTPUT = "sierpinski.svg"


def validate_integer(value, minimum, maximum):
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError(f"Enter a whole number from {minimum} to {maximum}.")
    return value


def validate_color(value):
    if not isinstance(value, str) or not re.fullmatch(r"#[0-9a-fA-F]{6}", value):
        raise ValueError("Enter a color as # followed by six hexadecimal digits (e.g. #0055aa).")
    return value.lower()


def outer_vertices(width):
    validate_integer(width, 100, 4000)
    side = width * 0.9
    height = math.sqrt(3) * side / 2
    top = (width - height) / 2
    return ((width / 2, top), (width * 0.05, top + height),
            (width * 0.95, top + height))


def midpoint(a, b):
    return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)


def terminal_triangles(vertices, depth):
    validate_integer(depth, 0, 8)

    def subdivide(triangle, remaining):
        if remaining == 0:
            yield triangle
            return
        a, b, c = triangle
        ab, bc, ca = midpoint(a, b), midpoint(b, c), midpoint(c, a)
        for corner in ((a, ab, ca), (ab, b, bc), (ca, bc, c)):
            yield from subdivide(corner, remaining - 1)

    return subdivide(vertices, depth)


def generate_svg(depth=DEFAULT_DEPTH, width=DEFAULT_WIDTH,
                 triangle_color=DEFAULT_TRIANGLE, background_color=DEFAULT_BACKGROUND):
    validate_integer(depth, 0, 8)
    vertices = outer_vertices(width)
    triangle_color = validate_color(triangle_color)
    background_color = validate_color(background_color)
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{width}" viewBox="0 0 {width} {width}">',
             '  <title>Sierpiński triangle</title>',
             f'  <rect width="{width}" height="{width}" fill="{background_color}"/>']
    for triangle in terminal_triangles(vertices, depth):
        points = " ".join(f"{x:.9f},{y:.9f}" for x, y in triangle)
        lines.append(f'  <polygon points="{points}" fill="{triangle_color}"/>')
    lines.append('</svg>')
    return "\n".join(lines) + "\n"


def prompt_integer(label, default, minimum, maximum):
    while True:
        raw = input(f"{label} [{default}]: ").strip()
        try:
            value = default if not raw else int(raw)
            return validate_integer(value, minimum, maximum)
        except ValueError:
            print(f"Enter a whole number from {minimum} to {maximum}.")


def prompt_color(label, default):
    while True:
        raw = input(f"{label} [{default}]: ").strip()
        try:
            return validate_color(raw or default)
        except ValueError as error:
            print(error)


def validate_output_path(raw):
    if not raw.strip():
        raise ValueError("Enter a nonempty SVG filename.")
    path = Path(raw).expanduser().absolute()
    if path.is_dir():
        raise ValueError("The output path is a directory; enter an SVG filename.")
    if path.suffix.lower() != ".svg":
        raise ValueError("The output filename must end in .svg.")
    if not path.parent.is_dir():
        raise ValueError("The parent directory must already exist.")
    return path


def confirm_overwrite(path):
    while True:
        answer = input(f"{path} already exists. Overwrite? [y/N]: ").strip().lower()
        if answer in ("", "n", "no"):
            return False
        if answer in ("y", "yes"):
            return True
        print("Enter yes or no; Enter means no.")


def write_svg(path, content, overwrite=False):
    """Publish a complete file, preserving an existing file unless authorized."""
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n",
                                         dir=path.parent, delete=False) as output:
            temporary = Path(output.name)
            output.write(content)
        if overwrite:
            os.replace(temporary, path)
        else:
            # Linking fails if a file appeared after the overwrite check.
            os.link(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def prompt_and_write(content):
    while True:
        raw = input(f"Output SVG path [{DEFAULT_OUTPUT}]: ").strip()
        try:
            path = validate_output_path(raw or DEFAULT_OUTPUT)
        except (ValueError, OSError, RuntimeError) as error:
            print(f"Invalid output path: {error}")
            continue
        overwrite = False
        if path.exists() or path.is_symlink():
            overwrite = confirm_overwrite(path)
            if not overwrite:
                print("File kept. Choose another output path.")
                continue
        try:
            write_svg(path, content, overwrite)
            return path
        except (OSError, ValueError) as error:
            print(f"Could not write {path}: {error}. Choose another output path.")


def main():
    try:
        depth = prompt_integer("Recursion depth (0–8)", DEFAULT_DEPTH, 0, 8)
        width = prompt_integer("Image width in pixels (100–4000)", DEFAULT_WIDTH, 100, 4000)
        foreground = prompt_color("Triangle color", DEFAULT_TRIANGLE)
        background = prompt_color("Background color", DEFAULT_BACKGROUND)
        path = prompt_and_write(generate_svg(depth, width, foreground, background))
        print(f"Saved {path} ({3 ** depth:,} triangles).")
        return 0
    except (EOFError, KeyboardInterrupt):
        print("\nCancelled; no further output written.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
