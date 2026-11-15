// Compact lecture DSL on top of the handwritten engine.
// scenes.js defines: TEXTS {beat: text}, LAYERS [..] (framework), LECT {num, title}, and calls
//   intro(id, hookBeat, titleBeat, hookItems)   section(id, layerIdx, colour, [beatSpec...])   recap(id, recapBeat, outroBeat, lines, nextText)
// beatSpec = {b:'beatId', t:'panel title', cite:'grey source', v:[item,...]}
// item = [type, ...args, {opts}]  opts: at:'word' (sync), f:0.4 (fraction of beat), bad/good/pt flags
const SCENES = {};
const PW = 2100;                       // panel spacing in world x
let _measure = null; let LASTW = 0;
function tw(str, size) {               // rendered width of handwritten text at engine size
  if (!_measure) _measure = document.createElement('canvas').getContext('2d');
  _measure.font = `${(size * 1.65).toFixed(1)}px Hand`;
  return _measure.measureText(str).width * 1.06;
}
function wrap(str, size, w) {
  const out = []; let cur = '';
  for (const word of String(str).split(' ')) {
    const t = cur ? cur + ' ' + word : word;
    if (tw(t, size) > w && cur) { out.push(cur); cur = word } else cur = t;
  }
  if (cur) out.push(cur); return out;
}
const norm = s => s.toLowerCase().replace(/[^a-z0-9%$]/g, '');
function wordT(b, word, occ) {          // time spec (fraction) for a word in a beat's narration
  const ws = (TEXTS[b] || '').split(/\s+/).map(norm); const w = norm(word); let n = 0;
  for (let i = 0; i < ws.length; i++) if (ws[i].startsWith(w) && ++n >= (occ || 1)) return [b, Math.max(0, i / ws.length - 0.02), 'f'];
  console.log('WORDMISS', b, word); return null;
}
function hud(fn) { const prev = PARENT; PARENT = document.getElementById('hud'); fn(); PARENT = prev }
function miniStack(S, t, hi, col) {
  const x = 1580, y = 52, w = 280, rh = Math.min(48, 300 / LAYERS.length);
  hud(() => {
    LAYERS.forEach((lab, i) => {
      S.rect(x, y + i * rh, w, rh, { t: sh(t, i * 0.08), c: i === hi ? col : 'gr', sw: i === hi ? 3 : 2, dur: .25 });
      let fz = Math.min(28, rh * .55); while (fz > 14 && tw(lab, fz) > w - 16) fz -= 1;
      S.text(x + w / 2, y + i * rh + rh * 0.68, lab, { t: sh(t, .1 + i * .08), anchor: 'middle', size: fz, c: i === hi ? col : 'gr', dur: .3 });
    });
    if (hi != null) {
      const yy = y + hi * rh;
      S.arrow(x - 70, yy + rh / 2, x - 12, yy + rh / 2, { t: sh(t, .7), c: col, sw: 3, head: 14 });
    }
  });
}
// ---------- item renderers: draw(S, x, y, w, t, args, o) -> height ; size(w,args,o) -> height
const IT = {};
function txtBlock(S, x, y, w, t, str, size, c, anchor, dly) {
  const lines = wrap(str, size, w); const lh = size * 1.5; LASTW = Math.max(...lines.map(l => tw(l, size)));
  lines.forEach((ln, i) => S.text(anchor === 'middle' ? x + w / 2 : x, y + size * 1.02 + i * lh, ln, { t: sh(t, i * (dly ?? .45)), c, size, anchor }));
  return lines.length * lh + 6;
}
IT.big = {
  h: (w, [s, c, sz]) => wrap(s, sz || 62, w).length * (sz || 62) * 1.5 + 10,
  d: (S, x, y, w, t, [s, c, sz]) => txtBlock(S, x, y, w, t, s, sz || 62, c || 'w', 'middle')
};
IT.text = {
  h: (w, [s, c, sz]) => wrap(s, sz || 40, w).length * (sz || 40) * 1.5 + 6,
  d: (S, x, y, w, t, [s, c, sz]) => txtBlock(S, x, y, w, t, s, sz || 40, c || 'w')
};
IT.note = {
  h: (w, [s]) => wrap(s, 38, w - 60).length * 38 * 1.5 + 14,
  d: (S, x, y, w, t, [s, c]) => {
    S.arrow(x, y + 30, x + 44, y + 30, { t, c: c || 'o', sw: 3, head: 13 });
    return txtBlock(S, x + 60, y, w - 60, sh(t, .2), s, 38, c || 'o') + 8;
  }
};
IT.list = {
  h: (w, [lines, c, o = {}]) => lines.reduce((a, l) => a + wrap(l, o.size || 38, w - 60).length * (o.size || 38) * 1.5 + 12, 0),
  d: (S, x, y, w, t, [lines, c, o = {}]) => {
    let yy = y; const sz = o.size || 38;
    lines.forEach((l, i) => {
      const ti = o.times ? T(o.times[i]) : sh(t, i * (o.step || 1.1));
      const lab = o.num ? (i + 1) + '.' : (o.tick ? '' : '•');
      if (o.tick) S.tick(x + 18, yy + sz * .75, 13, { t: ti, c: 'g', sw: 3 });
      else S.text(x, yy + sz, lab, { t: ti, c: c || 'w', size: sz });
      yy += txtBlock(S, x + 52, yy, w - 60, sh(ti, .15), l, sz, c || 'w', null, .3) + 12;
    });
    return yy - y;
  }
};
IT.col = {   // titled column: [title, colour, lines]
  h: (w, [ti, c, lines]) => 70 + IT.list.h(w, [lines, 'w', { size: 34 }]),
  d: (S, x, y, w, t, [ti, c, lines, o = {}]) => {
    let fz = 48; while (fz > 26 && tw(ti, fz) > w - 10) fz -= 2; S.text(x, y + 46, ti, { t, c, size: fz }); S.underline(x, y + 62, x + Math.min(w, tw(ti, fz)), { t: sh(t, .4), c, sw: 3 });
    return 70 + IT.list.d(S, x, y + 74, w, sh(t, .8), [lines, 'w', { size: 34, step: o.step || 0.9, times: o.times }]);
  }
};
IT.stack = {
  h: (w, [labels, o = {}]) => labels.length * (o.rh || 74),
  d: (S, x, y, w, t, [labels, o = {}]) => {
    const rh = o.rh || 74, ww = Math.min(w, o.w || 640), xx = x + (w - ww) / 2;
    labels.forEach((lab, i) => {
      const ti = o.times ? T(o.times[i]) : sh(t, i * (o.step || .6)); const c = (o.cols && o.cols[i]) || o.c || 'w';
      S.rect(xx, y + i * rh, ww, rh, { t: ti, c, sw: 3, dur: .4 });
      let fz = o.size || 36; while (fz > 18 && tw(lab, fz) > ww - 30) fz -= 1; S.text(xx + ww / 2, y + i * rh + rh * .66, lab, { t: sh(ti, .25), anchor: 'middle', size: fz, c });
    });
    if (o.hi != null) {
      const yy = y + o.hi * rh, hc = o.hic || 'y', th = o.hit ? T(o.hit) : sh(t, labels.length * (o.step || .6) + .3);
      S.bracketL(xx - 16, yy + 5, yy + rh - 5, { t: th, c: hc, sw: 4 }); S.bracketR(xx + ww + 16, yy + 5, yy + rh - 5, { t: sh(th, .1), c: hc, sw: 4 });
    }
    return labels.length * rh;
  }
};
IT.flow = {   // [labels[], colours[]|colour, {sub:[...]}]
  h: (w, [labels, cs, o = {}]) => 170 + (o.sub ? 60 : 0),
  d: (S, x, y, w, t, [labels, cs, o = {}]) => {
    const n = labels.length, gap = 70, bw = Math.min(330, (w - gap * (n - 1)) / n), tot = n * bw + (n - 1) * gap, x0 = x + (w - tot) / 2;
    labels.forEach((lab, i) => {
      const c = Array.isArray(cs) ? cs[i] : (cs || 'w'); const ti = o.times ? T(o.times[i]) : sh(t, i * (o.step || .9)); const bx = x0 + i * (bw + gap);
      S.rect(bx, y, bw, 150, { t: ti, c, sw: 3, dur: .4 });
      let fz = 34; while (fz > 20 && (Math.max(...lab.split(' ').map(x => tw(x, fz))) > bw - 22 || wrap(lab, fz, bw - 22).length > 3)) fz -= 2; const ls = wrap(lab, fz, bw - 22); ls.forEach((l, k) => S.text(bx + bw / 2, y + 75 + (k - (ls.length - 1) / 2) * fz * 1.45 + fz * .45, l, { t: sh(ti, .25), anchor: 'middle', size: fz, c }));
      if (o.sub && o.sub[i]) S.text(bx + bw / 2, y + 205, o.sub[i], { t: sh(ti, .5), anchor: 'middle', size: 28, c: 'gr' });
      if (i < n - 1) S.arrow(bx + bw + 8, y + 75, bx + bw + gap - 8, y + 75, { t: sh(ti, .45), c: 'gr', sw: 3, head: 14 });
    });
    return 170 + (o.sub ? 60 : 0);
  }
};
IT.bars = {   // vertical: [[label, value, colour, valueLabel],...], {h}
  h: (w, [data, o = {}]) => (o.h || 330) + 110 + (data.some(d => wrap(d[0], 30, w / data.length - 10).length > 1) ? 44 : 0),
  d: (S, x, y, w, t, [data, o = {}]) => {
    const H = o.h || 330, n = data.length, mx = o.max || Math.max(...data.map(d => d[1])), bw = Math.min(170, w / n * .55), sp = w / n, base = y + H + 50;
    S.line(x, base, x + w, base, { t, c: 'gr', sw: 2.5 });
    data.forEach(([lab, v, c, vl], i) => {
      const ti = o.times ? T(o.times[i]) : sh(t, .3 + i * (o.step || .8)); const bx = x + sp * i + (sp - bw) / 2; const h = Math.max(6, H * v / mx);
      S.bar(bx, base, bw, h, vl === undefined ? String(v) : vl, { t: ti, c: c || 'v' });
      wrap(lab, 30, sp - 10).forEach((l, k) => S.text(bx + bw / 2, base + 46 + k * 44, l, { t: sh(ti, .2), anchor: 'middle', size: 30, c: 'gr' }));
    });
    return H + 110 + (data.some(d => wrap(d[0], 30, sp - 10).length > 1) ? 44 : 0);
  }
};
IT.hbars = {  // horizontal: [[label, value, colour, valueLabel],...]
  h: (w, [data]) => data.length * 74,
  d: (S, x, y, w, t, [data, o = {}]) => {
    const lw = o.lw || 360, mx = o.max || Math.max(...data.map(d => d[1])), W = w - lw - 170;
    data.forEach(([lab, v, c, vl], i) => {
      const ti = o.times ? T(o.times[i]) : sh(t, i * (o.step || .8)), yy = y + i * 74;
      let fz = 34; while (fz > 20 && tw(lab, fz) > lw - 30) fz -= 1; S.text(x + lw - 20, yy + 44, lab, { t: ti, anchor: 'end', size: fz, c: 'w' });
      const bw = Math.max(8, W * v / mx);
      S.rect(x + lw, yy + 10, bw, 48, { t: sh(ti, .2), c: c || 'v', sw: 3, dur: .5 });
      S.text(x + lw + bw + 16, yy + 46, vl === undefined ? String(v) : vl, { t: sh(ti, .6), size: 34, c: c || 'v' });
    });
    return data.length * 74;
  }
};
IT.tokens = {  // [words[], colour] — wraps into rows
  rows: (w, words) => { const ws = words.map(s => Math.max(80, tw(s, 34) + 34)); const rows = [[]]; let cur = 0;
    ws.forEach((x, i) => { if (cur + x > w && rows[rows.length - 1].length) { rows.push([]); cur = 0 } rows[rows.length - 1].push(i); cur += x + 16 }); return [rows, ws] },
  h: (w, [words]) => IT.tokens.rows(w, words)[0].length * 96 + 4,
  d: (S, x, y, w, t, [words, c, o = {}]) => {
    const [rows, ws] = IT.tokens.rows(w, words);
    rows.forEach((r, ri) => {
      const tot = r.reduce((a, i) => a + ws[i], 0) + 16 * (r.length - 1); let xx = x + Math.max(0, (w - tot) / 2); const yy = y + ri * 96;
      r.forEach(i => {
        const s = words[i]; const ti = o.times ? T(o.times[i]) : sh(t, i * (o.step || .35)); const cc = (o.cols && o.cols[i]) || c || 'g';
        S.rect(xx, yy + 10, ws[i], 74, { t: ti, c: cc, sw: 2.6, dur: .3 }); S.text(xx + ws[i] / 2, yy + 58, s, { t: sh(ti, .15), anchor: 'middle', size: 34, c: cc }); xx += ws[i] + 16;
      });
    });
    return rows.length * 96 + 4;
  }
};
IT.grid = {   // [rows, cols, colour, {hi:n, hic, label}]
  h: (w, [r]) => r * 30 + 10,
  d: (S, x, y, w, t, [r, cn, c, o = {}]) => {
    const s = 22, g = 8, tot = cn * (s + g), x0 = x + (w - tot) / 2; let k = 0;
    for (let i = 0; i < r; i++) for (let j = 0; j < cn; j++, k++) {
      const cc = o.hi && k < o.hi ? (o.hic || 'p') : c || 'v';
      S.rect(x0 + j * (s + g), y + i * (s + g), s, s, { t: sh(t, (i * cn + j) * (o.step || .012)), c: cc, sw: 2, dur: .12 });
    }
    return r * (s + g) + 10;
  }
};
IT.gpus = {   // [n, colour, label, {sub}]
  h: () => 190,
  d: (S, x, y, w, t, [n, c, label, o = {}]) => {
    const bw = Math.min(130, (w - 20 * (n - 1)) / n), tot = n * bw + 20 * (n - 1), x0 = x + (w - tot) / 2;
    for (let i = 0; i < n; i++) { const bx = x0 + i * (bw + 20); S.rect(bx, y, bw, 110, { t: sh(t, i * .15), c: c || 'b', sw: 3, dur: .3 }); S.rect(bx + bw * .25, y + 28, bw * .5, 54, { t: sh(t, i * .15 + .2), c: c || 'b', sw: 2, dur: .25 }); }
    if (label) { let fz = 36; while (fz > 22 && tw(label, fz) > w) fz -= 1; S.text(x + w / 2, y + 160, label, { t: sh(t, n * .15 + .2), anchor: 'middle', size: fz, c: c || 'b' }) }
    return 190;
  }
};
IT.people = {
  h: () => 140,
  d: (S, x, y, w, t, [n, c, label]) => {
    const tot = n * 44, x0 = x + (w - tot) / 2 + 22; S.crowd(x0, y + 70, n, { t, c: c || 'w' });
    if (label) S.text(x + w / 2, y + 135, label, { t: sh(t, n * .08 + .2), anchor: 'middle', size: 32, c: 'gr' });
    return 145;
  }
};
IT.timeline = {  // [[label, sub, colour],...]
  h: () => 170,
  d: (S, x, y, w, t, [pts, o = {}]) => {
    const yy = y + 60; S.arrow(x, yy, x + w, yy, { t, c: 'gr', sw: 3 });
    pts.forEach(([lab, sub, c], i) => {
      const px = x + w * (i + .5) / pts.length, ti = o.times ? o.times[i] : sh(t, .4 + i * (o.step || .8));
      S.line(px, yy - 16, px, yy + 16, { t: ti, c: c || 'y', sw: 3 });
      S.text(px, yy - 30, lab, { t: sh(ti, .1), anchor: 'middle', size: 36, c: c || 'y' });
      if (sub) wrap(sub, 28, w / pts.length - 20).forEach((l, k) => S.text(px, yy + 60 + k * 42, l, { t: sh(ti, .3), anchor: 'middle', size: 28, c: 'w' }));
    });
    return 170;
  }
};
IT.card = {   // printed evidence card: [title, rows[][], {hi:[row idx], src, widths}]
  h: (w, [ti, rows]) => 100 + rows.length * 62 + 44,
  d: (S, x, y, w, t, [ti, rows, o = {}]) => {
    const cw = Math.min(w, o.w || 1100), h = 100 + rows.length * 62 + 44, cx = x + (w - cw) / 2;
    const g = S.card(cx, y, cw, h, { t });
    S.ptext(cx + 30, y + 58, ti, { size: 36, weight: 700 }, g);
    const nc = rows[0].length, wd = o.widths || rows[0].map(() => (cw - 60) / nc);
    rows.forEach((r, i) => {
      const ry = y + 86 + i * 62; S.prect(cx + 20, ry, cw - 40, 62, i === 0 ? '#e4e4de' : (i % 2 ? '#fff' : '#f0f0ec'), g);
      let xx = cx + 30; r.forEach((cell, j) => { S.ptext(xx, ry + 42, String(cell), { size: 29, weight: i === 0 ? 700 : 400 }, g); xx += wd[j] });
    });
    if (o.src) S.ptext(cx + 30, y + h - 14, o.src, { size: 20, c: '#888' }, g);
    (o.hi || []).forEach((ri, k) => {
      const ry = y + 86 + ri * 62; const th = o.hit ? T(o.hit[k]) : t + 1.2 + k * .8; const hc = (o.hic && o.hic[k]) || 'p';
      S.ell(cx + cw / 2, ry + 31, cw + 30, 88, { t: th, c: hc, sw: 3.5 });
    });
    return h;
  }
};
IT.eq = {
  h: () => 110,
  d: (S, x, y, w, t, [s, c]) => { let fz = 64; while (fz > 30 && tw(s, fz) > w - 20) fz -= 2; LASTW = tw(s, fz); S.text(x + w / 2, y + 80, s, { t, anchor: 'middle', size: fz, c: c || 'y' }); S.underline(x + w / 2 - LASTW / 2, y + 100, x + w / 2 + LASTW / 2, { t: sh(t, 1), c: c || 'y', sw: 3 }); return 115 }
};
IT.down = {
  h: () => 90,
  d: (S, x, y, w, t, [lab, c]) => { S.arrow(x + w / 2, y + 5, x + w / 2, y + 80, { t, c: c || 'gr', sw: 3 }); if (lab) S.text(x + w / 2 + 30, y + 55, lab, { t: sh(t, .2), size: 32, c: c || 'gr' }); return 90 }
};
IT.row = {   // side-by-side sub-items: [[item, item, ...], {gap}]
  h: (w, [items, o = {}]) => { const n = items.length, g = o.gap || 80, cw = (w - g * (n - 1)) / n; return Math.max(...items.map(it => IT[it[0]].h(cw, it.slice(1)))) },
  d: (S, x, y, w, t, [items, o = {}], bspec) => {
    const n = items.length, g = o.gap || 80, cw = (w - g * (n - 1)) / n; let mh = 0;
    items.forEach((it, i) => {
      const op = optsOf(it); const ti = op.at ? T(wordT(bspec.b, op.at, op.occ) || t + i * 1.5) : op.f != null ? T([bspec.b, op.f, 'f']) : t + i * (o.step || 2);
      const hh = IT[it[0]].d(S, x + i * (cw + g), y, cw, ti, argsOf(it), bspec); mh = Math.max(mh, hh); decorate(S, op, x + i * (cw + g), y, cw, hh, ti);
      if (o.vs && i < n - 1) S.text(x + (i + 1) * cw + i * g + g / 2, y + hh / 2, 'vs', { t: ti, anchor: 'middle', size: 40, c: 'gr' });
    });
    return mh;
  }
};
const isOpt = a => a && typeof a === 'object' && !Array.isArray(a) && ('at' in a || 'f' in a || 'bad' in a || 'good' in a || 'pt' in a || 'occ' in a || 'circ' in a);
const optsOf = it => isOpt(it[it.length - 1]) ? it[it.length - 1] : {};
const OPTK = ['at', 'f', 'bad', 'good', 'pt', 'occ', 'circ', 'late', 'ptc', 'until', 'dly'];
const argsOf = it => { const l = it[it.length - 1]; return it.slice(1, isOpt(l) && Object.keys(l).every(k => OPTK.includes(k)) ? -1 : undefined) };
function decorate(S, op, x, y, w, h, t) {
  const t2 = sh(t, op.dly || 1.4);
  const ew = op.typ === 'text' ? LASTW : Math.min(w, 900), ecx = op.typ === 'text' ? x + LASTW / 2 : x + w / 2;
  if (op.bad) { S.ell(ecx, y + h / 2, ew + 60, h + 50, { t: t2, c: 'p', sw: 3.5 }) }
  if (op.circ) { S.ell(x + w / 2, y + h / 2, Math.min(w, 900) + 60, h + 50, { t: t2, c: op.circ, sw: 3.5 }) }
  if (op.good) { S.bracketR(x + Math.min(w, 1300) + 30, y - 5, y + h + 5, { t: t2, c: 'g', sw: 4 }) }
  if (op.pt) { const cx = op.ptc ? x + (w - LASTW) / 2 - 20 : x - 20; S.pointer(cx, y + Math.min(h, 120) / 2, 0, { t: t2, until: op.until ? T(op.until) : t2 + 4, s: .7 }) }
}
// ---------- one panel per beat
function panel(S, i, spec, defTitle, defCite) {
  const ox = i * PW; const b = spec.b; const t0 = T([b, .05]);
  const title = spec.t === undefined ? defTitle : spec.t; let y = 110;
  const g = S.group(() => {
    if (title) {
      S.text(ox + 120, 130, title, { t: t0, size: 56 }); S.underline(ox + 120, 152, ox + 120 + Math.min(1300, tw(title, 56)), { t: T([b, .9]), sw: 3 }); y = 185;
      const cite = spec.cite === undefined ? null : spec.cite;
      if (cite) { S.text(ox + 130, 212, cite, { t: T([b, 1.3]), c: 'gr', size: 28 }); y = 235 }
    }
    const X = ox + 120, W0 = spec.w || 1340, items = spec.v || []; y += 30; const gap = 40; const avail = 1040 - y;
    const meas = W => items.map(it => IT[it[0]].h(W, argsOf(it)) + (it[0] === 'note' ? 10 : 0));
    const total = hs => hs.reduce((a, b) => a + b, 0) + gap * (items.length - 1);
    let sc = Math.min(spec.zoom || 1.3, avail / total(meas(W0))), W = W0 / sc, hs = meas(W);
    for (let k = 0; k < 4 && total(hs) * sc > avail; k++) { sc = avail / total(hs); W = W0 / sc; hs = meas(W) }
    let yy = y + Math.max(0, (avail - total(hs) * sc) * .35);
    items.forEach((it, k) => {
      const op = optsOf(it); const n = items.length;
      const ti = T(op.at ? (wordT(b, op.at, op.occ) || [b, .05 + .75 * k / n, 'f']) : op.f != null ? [b, op.f, 'f'] : [b, (title ? .12 : .02) + .72 * k / n, 'f']);
      const lim = BEATS[b].s + BEATS[b].d - (op.late || 2.6); const tiC = Math.max(BEATS[b].s, Math.min(ti, lim));
      const gi = S.group(() => { const hh = IT[it[0]].d(S, X, yy, W, tiC, argsOf(it), spec); decorate(S, Object.assign({ typ: it[0] }, op), X, yy, W, hh, tiC) });
      if (sc !== 1) gi.setAttribute('transform', `translate(${X} ${yy}) scale(${sc}) translate(${-X} ${-yy})`);
      yy += (hs[k] + gap) * sc;
    });
  });
  return g;
}
function addScene(id, beats, specsFn, opts) {
  SCENES[id] = {
    beats, build(S) {
      const specs = specsFn();
      if (opts.hi !== undefined) miniStack(S, T([specs[0].b, .05]), opts.hi, opts.c);
      specs.forEach((s, i) => { if (i > 0) S.cam([s.b, -0.35], i * PW + 960, 540, 1, .8); panel(S, i, s, opts.title, opts.cite) });
    }
  };
}
// public helpers used by scenes.js
function section(id, layer, col, specs, title) { addScene(id, specs.map(s => s.b), () => specs, { hi: layer, c: col, title: title ?? LAYERS[layer] }) }
function intro(id, hook, titleB, hookItems) {
  addScene(id, [hook, titleB], () => [
    { b: hook, t: null, w: 1680, v: hookItems },
    { b: titleB, t: null, w: 1680, v: [['text', LECT.label, 'gr', 34], ['big', LECT.title, 'w', 96], ['stack', LAYERS, { rh: 66, size: 34, w: 620, step: (BEATS_DUR(titleB) * .4) / LAYERS.length, c: 'v' }]] }
  ], {});
}
function recap(id, rb, ob, lines, next) {
  addScene(id, [rb, ob], () => [
    { b: rb, t: 'Recap', w: 1650, v: [['row', [['stack', LAYERS, { rh: 64, size: 30, w: 460, c: 'v', step: .3 }], ['list', lines, 'o', { tick: true, size: 34, step: Math.max(.9, BEATS_DUR(rb) * .85 / lines.length) }]], { gap: 60, step: .6 }]] },
    { b: ob, t: null, w: 1680, v: [['text', 'up next', 'gr', 40], ['big', next, 'y', 80], ['stack', LAYERS, { rh: 60, size: 30, w: 520, c: 'gr', step: .2 }]] }
  ], {});
}
function BEATS_DUR(b) { return BEATS[b].d }
// hand-drawn chart: [series [[pts(0..1), colour, label], ...], {xl, yl, dots:[[x,y,label,colour,time]], h, times}]
IT.chart = {
  h: (w, [series, o = {}]) => (o.h || 380) + 70,
  d: (S, x, y, w, t, [series, o = {}]) => {
    const H = o.h || 380, W = Math.min(w, o.w || 1000), x0 = x + (w - W) / 2 + 40, y0 = y + H, X = v => x0 + v * (W - 60), Y = v => y0 - v * (H - 20);
    S.arrow(x0, y0, x0 + W - 30, y0, { t, c: 'gr', sw: 2.5, head: 14 }); S.arrow(x0, y0, x0, y + 5, { t: t + .2, c: 'gr', sw: 2.5, head: 14 });
    if (o.xl) S.text(x0 + W - 40, y0 + 46, o.xl, { t: t + .4, anchor: 'end', size: 30, c: 'gr' });
    if (o.yl) S.text(x0 + 14, y + 24, o.yl, { t: t + .4, size: 30, c: 'gr' });
    series.forEach(([pts, c, lab], i) => {
      const ti = o.times ? T(o.times[i]) : t + .6 + i * 1.2;
      S.path('M' + pts.map(([a, b]) => X(a) + ' ' + Y(b)).join(' L'), { t: ti, c: c || 'y', sw: 4, rough: .4, dur: 1.2 });
      if (lab) { const [a, b] = pts[pts.length - 1]; S.text(X(a) - 10, Y(b) - 20, lab, { t: ti + 1, anchor: 'end', size: 34, c: c || 'y' }) }
    });
    (o.dots || []).forEach(([a, b, lab, c, tt], i) => {
      const ti = tt ? T(tt) : t + 2 + i;
      S.dot(X(a), Y(b), 11, { t: ti, c: c || 'p' }); if (lab) S.text(X(a) + 18, Y(b) + 40, lab, { t: ti + .1, size: 32, c: c || 'p' });
    });
    return H + 70;
  }
};
// analogy box: [label, text, colour]
IT.analogy = {
  h: (w, [lab, s]) => wrap(s, 40, w - 80).length * 60 + 90,
  d: (S, x, y, w, t, [lab, s, c]) => {
    const lines = wrap(s, 40, w - 80), h = lines.length * 60 + 80, bw = Math.min(w, Math.max(...lines.map(l => tw(l, 40))) + 80);
    S.rect(x, y, bw, h, { t, c: c || 'o', sw: 2.6, dur: .5, rough: 1.3 });
    S.text(x + 24, y + 36, lab || 'think of it like…', { t: t + .3, c: 'gr', size: 28 });
    lines.forEach((l, i) => S.text(x + 40, y + 92 + i * 60, l, { t: t + .6 + i * .5, c: c || 'o', size: 40 }));
    return h;
  }
};
// narration registry for extraction
const SAY = {}; function say(o) { Object.assign(SAY, o) }
