/* Лёгкие SVG-графики без внешних библиотек. Единый стиль с темой (CSS-переменные). */
(function (global) {
  const NF = new Intl.NumberFormat('ru-RU');
  const nf = n => NF.format(Math.round(n || 0));

  let tip = document.getElementById('tmchart-tip');
  if (!tip) {
    tip = document.createElement('div');
    tip.id = 'tmchart-tip';
    tip.style.cssText = 'position:fixed;pointer-events:none;z-index:1080;opacity:0;transform:translate(-50%,-120%);' +
      'background:#15171b;color:#fff;padding:8px 10px;border-radius:8px;font-size:12.5px;' +
      'box-shadow:0 8px 24px rgba(0,0,0,.28);transition:opacity .1s;max-width:260px';
    document.addEventListener('DOMContentLoaded', () => document.body.appendChild(tip));
    if (document.body) document.body.appendChild(tip);
  }
  const showTip = (html, x, y) => { tip.innerHTML = html; tip.style.left = x + 'px'; tip.style.top = y + 'px'; tip.style.opacity = 1; };
  const hideTip = () => { tip.style.opacity = 0; };
  const row = (color, name, val) =>
    `<div style="display:flex;justify-content:space-between;gap:14px">
       <span>${color ? `<i style="display:inline-block;width:8px;height:8px;border-radius:2px;background:${color};margin-right:6px"></i>` : ''}${name}</span>
       <b style="font-variant-numeric:tabular-nums">${val}</b></div>`;
  const tm = txt => `<div style="font-family:ui-monospace,monospace;font-size:11px;opacity:.7;margin-bottom:4px">${txt}</div>`;

  function niceMax(v, step) { step = step || Math.pow(10, Math.max(0, String(Math.round(v)).length - 2)); return Math.max(step, Math.ceil(v / step) * step); }

  // Линейный график: opts = {x:[...], series:[{name,color,values}], normalize, height, unit}
  function line(el, opts) {
    if (typeof el === 'string') el = document.getElementById(el);
    if (!el) return;
    const x = opts.x, series = opts.series, norm = opts.normalize;
    const W = 960, H = opts.height || 280, P = { t: 16, r: 14, b: 34, l: 52 };
    const pw = W - P.l - P.r, ph = H - P.t - P.b;
    const rawMax = Math.max(1, ...series.flatMap(s => s.values));
    const perMax = series.map(s => Math.max(1, ...s.values));
    const max = norm ? 100 : niceMax(rawMax);
    const px = i => P.l + (x.length === 1 ? pw / 2 : i * pw / (x.length - 1));
    const py = v => P.t + ph - (v / max) * ph;
    const val = (s, i, si) => norm ? s.values[i] / perMax[si] * 100 : s.values[i];
    let grid = '';
    const ticks = 4;
    for (let k = 0; k <= ticks; k++) {
      const v = max / ticks * k;
      grid += `<line x1="${P.l}" y1="${py(v)}" x2="${W - P.r}" y2="${py(v)}" stroke="var(--tm-line,#e6e6e0)"/>` +
              `<text x="${P.l - 8}" y="${py(v) + 3}" text-anchor="end" fill="var(--tm-muted,#8b8e94)" font-size="11" font-family="ui-monospace,monospace">${norm ? v + '%' : nf(v)}</text>`;
    }
    let xl = '';
    x.forEach((lb, i) => { if (x.length <= 14 || i % 2 === 0 || i === x.length - 1) xl += `<text x="${px(i)}" y="${H - 12}" text-anchor="middle" fill="var(--tm-muted,#8b8e94)" font-size="11" font-family="ui-monospace,monospace">${lb}</text>`; });
    let paths = '', dots = '';
    series.forEach((s, si) => {
      const d = 'M ' + x.map((_, i) => `${px(i)},${py(val(s, i, si))}`).join(' L ');
      paths += `<path d="${d}" fill="none" stroke="${s.color}" stroke-width="2"/>`;
      dots += x.map((_, i) => `<circle cx="${px(i)}" cy="${py(val(s, i, si))}" r="2.6" fill="${s.color}"/>`).join('');
    });
    const cw = pw / x.length;
    const cols = x.map((_, i) => `<rect x="${px(i) - cw / 2}" y="${P.t}" width="${cw}" height="${ph}" fill="transparent" data-i="${i}" style="cursor:pointer"/>`).join('');
    el.innerHTML = `<svg viewBox="0 0 ${W} ${H}" style="width:100%;height:auto;overflow:visible">
      ${grid}${paths}${dots}
      <line id="_ch" x1="0" y1="${P.t}" x2="0" y2="${P.t + ph}" stroke="var(--tm-ink-2,#585c63)" stroke-dasharray="3 3" opacity="0"/>
      <line x1="${P.l}" y1="${P.t + ph}" x2="${W - P.r}" y2="${P.t + ph}" stroke="var(--tm-muted,#c9cac4)"/>${xl}${cols}</svg>`;
    const chair = el.querySelector('#_ch');
    el.querySelectorAll('[data-i]').forEach(c => {
      c.addEventListener('mousemove', e => {
        const i = +c.dataset.i;
        chair.setAttribute('x1', px(i)); chair.setAttribute('x2', px(i)); chair.style.opacity = .8;
        showTip(tm(x[i]) + series.map(s => row(s.color, s.name, nf(s.values[i]) + (s.unit || opts.unit || ''))).join(''), e.clientX, e.clientY);
      });
      c.addEventListener('mouseleave', () => { chair.style.opacity = 0; hideTip(); });
    });
  }

  // Вертикальные столбцы: opts = {labels, values, color, unit, height}
  function vbars(el, opts) {
    if (typeof el === 'string') el = document.getElementById(el);
    if (!el) return;
    const lb = opts.labels, vals = opts.values, color = opts.color || 'var(--tm-brand,#2456c8)';
    const W = 960, H = opts.height || 280, P = { t: 16, r: 14, b: 34, l: 52 };
    const pw = W - P.l - P.r, ph = H - P.t - P.b;
    const max = niceMax(Math.max(1, ...vals));
    const bw = pw / lb.length * 0.6;
    const cx = i => P.l + (i + 0.5) * pw / lb.length;
    const py = v => P.t + ph - (v / max) * ph;
    let grid = '';
    for (let k = 0; k <= 4; k++) { const v = max / 4 * k; grid += `<line x1="${P.l}" y1="${py(v)}" x2="${W - P.r}" y2="${py(v)}" stroke="var(--tm-line,#e6e6e0)"/><text x="${P.l - 8}" y="${py(v) + 3}" text-anchor="end" fill="var(--tm-muted,#8b8e94)" font-size="11" font-family="ui-monospace,monospace">${nf(v)}</text>`; }
    let bars = '', xl = '';
    lb.forEach((l, i) => {
      bars += `<rect x="${cx(i) - bw / 2}" y="${py(vals[i])}" width="${bw}" height="${ph - (py(vals[i]) - P.t)}" rx="3" fill="${color}"/>` +
              `<rect x="${cx(i) - pw / lb.length / 2}" y="${P.t}" width="${pw / lb.length}" height="${ph}" fill="transparent" data-i="${i}" style="cursor:pointer"/>`;
      if (lb.length <= 14 || i % 2 === 0 || i === lb.length - 1) xl += `<text x="${cx(i)}" y="${H - 12}" text-anchor="middle" fill="var(--tm-muted,#8b8e94)" font-size="11" font-family="ui-monospace,monospace">${l}</text>`;
    });
    el.innerHTML = `<svg viewBox="0 0 ${W} ${H}" style="width:100%;height:auto;overflow:visible">${grid}${bars}<line x1="${P.l}" y1="${P.t + ph}" x2="${W - P.r}" y2="${P.t + ph}" stroke="var(--tm-muted,#c9cac4)"/>${xl}</svg>`;
    el.querySelectorAll('[data-i]').forEach(c => {
      c.addEventListener('mousemove', e => { const i = +c.dataset.i; showTip(tm(lb[i]) + row(color, opts.name || 'Значение', nf(vals[i]) + (opts.unit || '')), e.clientX, e.clientY); });
      c.addEventListener('mouseleave', hideTip);
    });
  }

  // Горизонтальные бары (DOM): items=[{label,value,sub,color}], opts={unit,max}
  function hbars(el, items, opts) {
    if (typeof el === 'string') el = document.getElementById(el);
    if (!el) return;
    opts = opts || {};
    const max = opts.max || Math.max(1, ...items.map(i => i.value));
    el.innerHTML = items.map(it => {
      const w = Math.max(2, it.value / max * 100);
      const col = it.color || 'var(--tm-brand,#2456c8)';
      return `<div style="display:grid;grid-template-columns:minmax(120px,180px) 1fr auto;gap:12px;align-items:center;font-size:13px;margin:9px 0">
        <div style="white-space:nowrap;overflow:hidden;text-overflow:ellipsis" title="${it.label}${it.sub ? ' · ' + it.sub : ''}">${it.label}</div>
        <div style="background:color-mix(in srgb,var(--tm-ink,#15171b) 7%,transparent);border-radius:5px;height:16px;overflow:hidden">
          <div style="height:100%;border-radius:5px;width:${w}%;background:${col}"></div></div>
        <div style="font-family:ui-monospace,monospace;font-size:12.5px;color:var(--tm-ink-2,#585c63);text-align:right;min-width:70px">${nf(it.value)}${opts.unit || ''}</div>
      </div>`;
    }).join('');
  }

  global.TMChart = { line, vbars, hbars, nf };
})(window);
