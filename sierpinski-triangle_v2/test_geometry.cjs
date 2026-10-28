const { test } = require('node:test');
const assert = require('node:assert/strict');
const { DEFAULTS, validate, vertices, triangles, buildSVG } = require('./geometry.js');
const area = ([a,b,c]) => Math.abs((b[0]-a[0])*(c[1]-a[1])-(c[0]-a[0])*(b[1]-a[1]))/2;
const near = (a,b) => assert.ok(Math.abs(a-b) <= Math.max(1, Math.abs(b))*1e-10, `${a} ≈ ${b}`);
test('equilateral outer triangle and centered bounds at size limits', () => {
  for (const size of [100,800,4000]) {
    const v = vertices(size);
    for (let i=0;i<3;i++) near(Math.hypot(v[i][0]-v[(i+1)%3][0],v[i][1]-v[(i+1)%3][1]), .9*size);
    for (const axis of [0,1]) near((Math.min(...v.map(p=>p[axis]))+Math.max(...v.map(p=>p[axis])))/2,size/2);
  }
});
for (const depth of [0,1,2,6,8]) test(`depth ${depth}: count, finite points, positive area and filled area`, () => {
  const result = triangles(800,depth);
  assert.equal(result.length,3**depth);
  result.forEach(t => { assert.ok(t.flat().every(Number.isFinite)); assert.ok(area(t)>0); });
  near(result.reduce((sum,t)=>sum+area(t),0),area(vertices(800))*(3/4)**depth);
});
test('depth one contains exactly the three midpoint corner triangles', () => {
  const [a,b,c] = vertices(800);
  const mid = (p,q)=>p.map((v,i)=>(v+q[i])/2);
  const ab=mid(a,b),bc=mid(b,c),ca=mid(c,a);
  assert.deepEqual(triangles(800,1),[[a,ab,ca],[ab,b,bc],[ca,bc,c]]);
  assert.ok(!triangles(800,1).some(t=>JSON.stringify(t)===JSON.stringify([ab,bc,ca])));
});
test('defaults, bounds, normalized custom colors and SVG contract', () => {
  assert.ok(validate(DEFAULTS).valid);
  for (const size of [100,4000]) assert.ok(validate({...DEFAULTS,size}).valid);
  const svg=buildSVG({depth:'3',size:'300',color:'#0055AA',background:'#fff4dd'});
  assert.match(svg,/xmlns="http:\/\/www.w3.org\/2000\/svg"/);
  assert.match(svg,/width="300" height="300" viewBox="0 0 300 300"/);
  assert.match(svg,/<title[^>]*>Sierpiński triangle, depth 3<\/title>/);
  assert.match(svg,/<rect[^>]*fill="#fff4dd"/);
  assert.match(svg,/<g fill="#0055aa">/);
  assert.equal((svg.match(/<polygon /g)||[]).length,27);
});
test('invalid inputs rejected before geometry can be generated', () => {
  const cases={depth:[-1,9,1.5,'',' ','bad',Infinity,NaN,null],size:[99,4001,100.5,'',' ',Infinity,'bad',null],color:['red','#fff','#gg0000','<script>'],background:['','#12345','#1234567']};
  for (const [field,values] of Object.entries(cases)) for (const value of values) {
    const input={...DEFAULTS,[field]:value};
    assert.ok(validate(input).errors[field],`${field}: ${value}`);
    assert.throws(()=>buildSVG(input),RangeError);
  }
  assert.throws(()=>triangles(800,9),RangeError);
  // Both fields fail validation before recursion, even with a huge requested depth.
  assert.throws(()=>buildSVG({...DEFAULTS,depth:100000000,size:99}),/Recursion depth.*Drawing size/);
});
