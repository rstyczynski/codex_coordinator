import contextlib
import io
import math
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

import sierpinski as s


def area(triangle):
    a, b, c = triangle
    return abs((b[0]-a[0])*(c[1]-a[1]) - (c[0]-a[0])*(b[1]-a[1])) / 2


class GeometryTests(unittest.TestCase):
    def test_counts_areas_and_bounds(self):
        vertices = s.outer_vertices(800)
        lengths = [math.dist(vertices[i], vertices[(i+1) % 3]) for i in range(3)]
        self.assertAlmostEqual(lengths[0], lengths[1])
        self.assertAlmostEqual(lengths[1], lengths[2])
        for depth, count in ((0, 1), (1, 3), (2, 9), (6, 729), (8, 6561)):
            with self.subTest(depth=depth):
                triangles = list(s.terminal_triangles(vertices, depth))
                self.assertEqual(len(triangles), count)
                self.assertTrue(all(area(t) > 0 for t in triangles))
                self.assertAlmostEqual(sum(map(area, triangles)), area(vertices)*(3/4)**depth, places=5)
                self.assertTrue(all(40 <= coord <= 760 for t in triangles for point in t for coord in point))

    def test_depth_one_midpoints(self):
        a, b, c = s.outer_vertices(800)
        ab, bc, ca = s.midpoint(a, b), s.midpoint(b, c), s.midpoint(c, a)
        self.assertEqual(list(s.terminal_triangles((a, b, c), 1)),
                         [(a, ab, ca), (ab, b, bc), (ca, bc, c)])

    def test_svg_structure_and_custom_parameters(self):
        ns = '{http://www.w3.org/2000/svg}'
        for depth, width, fg, bg in ((6, 800, '#1f2937', '#ffffff'), (3, 600, '#0055AA', '#fff4dd'), (0, 100, '#000000', '#ffffff'), (1, 4000, '#000000', '#ffffff'), (2, 800, '#000000', '#ffffff'), (8, 800, '#000000', '#ffffff')):
            root = ET.fromstring(s.generate_svg(depth, width, fg, bg))
            self.assertEqual(root.tag, ns+'svg')
            self.assertEqual(root.attrib, dict(width=str(width), height=str(width), viewBox=f'0 0 {width} {width}'))
            self.assertEqual(root.find(ns+'rect').attrib, dict(width=str(width), height=str(width), fill=bg))
            polygons = root.findall(ns+'polygon')
            self.assertEqual(len(polygons), 3**depth)
            for polygon in polygons:
                self.assertEqual(polygon.attrib['fill'], fg.lower())
                values = polygon.attrib['points'].replace(',', ' ').split()
                self.assertEqual(len(values), 6)
                self.assertTrue(all(math.isfinite(float(v)) for v in values))

    def test_public_input_validation(self):
        for kwargs in (dict(depth=-1), dict(depth=9), dict(depth=1.5), dict(depth=True), dict(width=99), dict(width=4001), dict(triangle_color='red'), dict(background_color='#fff')):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                s.generate_svg(**kwargs)


class PromptTests(unittest.TestCase):
    def run_prompt(self, answers, function, *args):
        stream = io.StringIO()
        with patch('builtins.input', side_effect=answers) as mocked, contextlib.redirect_stdout(stream):
            result = function(*args)
        return result, mocked, stream.getvalue()

    def test_defaults_and_reprompt(self):
        result, mocked, _ = self.run_prompt(['  '], s.prompt_integer, 'Depth', 6, 0, 8)
        self.assertEqual(result, 6)
        self.assertIn('[6]', mocked.call_args.args[0])
        for lower, upper in ((0, 8), (100, 4000)):
            for boundary in (lower, upper):
                result, _, message = self.run_prompt(['abc', '1.5', str(lower-1), str(upper+1), str(boundary)], s.prompt_integer, 'Value', lower, lower, upper)
                self.assertEqual(result, boundary)
                self.assertEqual(message.count('Enter a whole number'), 4)
        result, mocked, _ = self.run_prompt([' '], s.prompt_color, 'Color', '#ffffff')
        self.assertEqual(result, '#ffffff')
        self.assertIn('[#ffffff]', mocked.call_args.args[0])
        result, _, message = self.run_prompt(['red', '#fff', '#GG0000', '#0055AA'], s.prompt_color, 'Color', '#ffffff')
        self.assertEqual(result, '#0055aa')
        self.assertEqual(message.count('six hexadecimal'), 3)

    def test_path_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            for invalid in ('', str(base), str(base/'missing'/'a.svg'), str(base/'a.png')):
                with self.subTest(path=invalid), self.assertRaises(ValueError):
                    s.validate_output_path(invalid)
            self.assertEqual(s.validate_output_path(str(base/'with spaces.SVG')), base/'with spaces.SVG')
            self.assertEqual(s.validate_output_path('sierpinski.svg'), Path.cwd()/'sierpinski.svg')
            self.assertEqual(s.validate_output_path('~/drawing.svg'), Path.home()/'drawing.svg')

    def test_overwrite_decline_default_and_success(self):
        with tempfile.TemporaryDirectory() as directory:
            old, new = Path(directory)/'old.svg', Path(directory)/'new.svg'
            old.write_text('keep')
            result, _, _ = self.run_prompt([str(old), '', str(new)], s.prompt_and_write, 'new drawing')
            self.assertEqual(result, new)
            self.assertEqual(old.read_text(), 'keep')
            self.assertEqual(new.read_text(), 'new drawing')
            self.run_prompt([str(old), 'maybe', 'yes'], s.prompt_and_write, 'replacement')
            self.assertEqual(old.read_text(), 'replacement')
            with self.assertRaises(FileExistsError):
                s.write_svg(old, 'must not replace')
            self.assertEqual(old.read_text(), 'replacement')
            self.assertEqual(set(Path(directory).iterdir()), {old, new})

    def test_write_error_retry_and_default_path(self):
        with patch.object(s, 'validate_output_path', return_value=Path('/example.svg')) as validator, patch.object(s, 'write_svg', side_effect=[OSError('disk full'), None]):
            result, mocked, message = self.run_prompt(['', 'other.svg'], s.prompt_and_write, 'drawing')
            self.assertEqual(result, Path('/example.svg'))
            self.assertEqual(validator.call_args_list[0].args, ('sierpinski.svg',))
            self.assertIn('[sierpinski.svg]', mocked.call_args_list[0].args[0])
            self.assertIn('disk full', message)

    def test_failed_overwrite_preserves_original(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'old.svg'
            path.write_text('original')
            with patch.object(s.os, 'replace', side_effect=OSError('failure')), self.assertRaises(OSError):
                s.write_svg(path, 'new', overwrite=True)
            self.assertEqual(path.read_text(), 'original')
            self.assertEqual(list(Path(directory).iterdir()), [path])

    def test_cancellation(self):
        for exception in (EOFError, KeyboardInterrupt):
            with patch('builtins.input', side_effect=exception), contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(s.main(), 1)
                self.assertIn('Cancelled', output.getvalue())


if __name__ == '__main__':
    unittest.main()
