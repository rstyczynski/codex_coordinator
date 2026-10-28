'use strict';
(() => {
  const api = Sierpinski;
  const fields = Object.keys(api.DEFAULTS);
  const form = document.getElementById('controls');
  const errors = document.getElementById('errors');
  const status = document.getElementById('status');
  let rendered;
  function clearErrors() {
    errors.replaceChildren();
    fields.forEach(key => document.getElementById(key).removeAttribute('aria-invalid'));
  }
  function redraw() {
    clearErrors();
    const input = Object.fromEntries(fields.map(key => [key, document.getElementById(key).value]));
    const checked = api.validate(input);
    if (!checked.valid) {
      for (const [field, message] of Object.entries(checked.errors)) {
        document.getElementById(field).setAttribute('aria-invalid', 'true');
        const p = document.createElement('p'); p.textContent = message; errors.append(p);
      }
      status.textContent = 'Please correct the highlighted fields. Your last drawing is still shown.';
      document.getElementById(Object.keys(checked.errors)[0]).focus();
      return;
    }
    const svg = api.buildSVG(checked.values);
    document.getElementById('preview').innerHTML = svg;
    rendered = { ...checked.values, svg };
    document.getElementById('dimensions').textContent = `${rendered.size} × ${rendered.size} px`;
    status.textContent = `Depth ${rendered.depth} · ${(3 ** rendered.depth).toLocaleString('en-US')} ${rendered.depth === 0 ? 'triangle' : 'triangles'}.${rendered.color === rendered.background ? ' Triangle and background colors match; the pattern is invisible.' : ''}`;
  }
  form.addEventListener('submit', event => { event.preventDefault(); redraw(); });
  document.getElementById('reset').addEventListener('click', () => {
    fields.forEach(key => { document.getElementById(key).value = api.DEFAULTS[key]; });
    redraw();
  });
  form.addEventListener('input', () => { status.textContent = 'Edits pending. Select Redraw to update the drawing; download saves the last rendered image.'; });
  document.getElementById('download').addEventListener('click', () => {
    const url = URL.createObjectURL(new Blob([rendered.svg], { type: 'image/svg+xml;charset=utf-8' }));
    const link = document.createElement('a');
    link.href = url; link.download = `sierpinski-depth-${rendered.depth}-${rendered.size}px.svg`;
    document.body.append(link); link.click(); link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 10000);
    status.textContent = `SVG download requested for the last rendered drawing (depth ${rendered.depth}, ${rendered.size} × ${rendered.size} px).`;
  });
  redraw();
})();
