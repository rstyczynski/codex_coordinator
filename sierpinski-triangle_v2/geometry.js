(function (root) {
  'use strict';
  const DEFAULTS = Object.freeze({ depth: 6, size: 800, color: '#1f2937', background: '#ffffff' });
  function validate(input) {
    const errors = {};
    const values = {};
    for (const [field, min, max, label] of [['depth', 0, 8, 'Recursion depth'], ['size', 100, 4000, 'Drawing size']]) {
      const raw = input[field];
      const value = typeof raw === 'string' && raw.trim() === '' ? NaN : Number(raw);
      if (raw == null || !Number.isInteger(value) || value < min || value > max) errors[field] = `${label} must be a whole number from ${min} to ${max}.`;
      else values[field] = value;
    }
    for (const field of ['color', 'background']) {
      if (typeof input[field] !== 'string' || !/^#[0-9a-f]{6}$/i.test(input[field])) errors[field] = `${field === 'color' ? 'Triangle' : 'Background'} color must use six hexadecimal digits, such as #0055aa.`;
      else values[field] = input[field].toLowerCase();
    }
    return { values, errors, valid: Object.keys(errors).length === 0 };
  }
  function vertices(size) {
    const height = Math.sqrt(3) * 0.9 * size / 2;
    const top = (size - height) / 2;
    return [[size / 2, top], [size * 0.05, top + height], [size * 0.95, top + height]];
  }
  function triangles(size, depth) {
    if (!Number.isInteger(size) || size < 100 || size > 4000 || !Number.isInteger(depth) || depth < 0 || depth > 8) throw new RangeError('Invalid size or depth');
    const result = [];
    const midpoint = (a, b) => [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2];
    function visit(a, b, c, level) {
      if (level === 0) { result.push([a, b, c]); return; }
      const ab = midpoint(a, b), bc = midpoint(b, c), ca = midpoint(c, a);
      visit(a, ab, ca, level - 1);
      visit(ab, b, bc, level - 1);
      visit(ca, bc, c, level - 1);
    }
    visit(...vertices(size), depth);
    return result;
  }
  function buildSVG(input) {
    const checked = validate(input);
    if (!checked.valid) throw new RangeError(Object.values(checked.errors).join(' '));
    const { size, depth, color, background } = checked.values;
    const polygons = triangles(size, depth).map(t => `<polygon points="${t.map(p => p.join(',')).join(' ')}"/>`).join('');
    return `<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" role="img" aria-labelledby="drawing-title"><title id="drawing-title">Sierpiński triangle, depth ${depth}</title><rect width="${size}" height="${size}" fill="${background}"/><g fill="${color}">${polygons}</g></svg>`;
  }
  const api = { DEFAULTS, validate, vertices, triangles, buildSVG };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.Sierpinski = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
