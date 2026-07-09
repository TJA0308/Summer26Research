
// ---------- Loading screen ----------
window.addEventListener('load', () => {
  setTimeout(() => {
    const loader = document.getElementById('loader');
    if (loader) loader.classList.add('done');
    // Trigger name glitch after loader fades
    setTimeout(triggerGlitch, 400);
  }, 1500);
});

function triggerGlitch() {
  document.querySelectorAll('.glitch').forEach(el => {
    el.classList.add('glitching');
    setTimeout(() => el.classList.remove('glitching'), 1300);
  });
}

// ---------- Nav scrolled state ----------
const nav = document.querySelector('.nav');
window.addEventListener('scroll', () => {
  nav.classList.toggle('scrolled', window.scrollY > 20);
});

// ---------- Mobile toggle ----------
document.getElementById('navToggle').addEventListener('click', () => {
  nav.classList.toggle('open');
});
document.querySelectorAll('.nav-links a').forEach(a =>
  a.addEventListener('click', () => nav.classList.remove('open'))
);

// ---------- Nav sliding underline ----------
const navLinks = document.getElementById('navLinks');
const navUnderline = document.getElementById('navUnderline');
if (navLinks && navUnderline) {
  const anchors = navLinks.querySelectorAll('a');
  anchors.forEach(a => {
    a.addEventListener('mouseenter', () => {
      const rect = a.getBoundingClientRect();
      const parentRect = navLinks.getBoundingClientRect();
      navUnderline.style.left = (rect.left - parentRect.left) + 'px';
      navUnderline.style.width = rect.width + 'px';
      navUnderline.classList.add('visible');
    });
  });
  navLinks.addEventListener('mouseleave', () => {
    navUnderline.classList.remove('visible');
  });
}

// ---------- Flowing mesh grid ----------
(function flowingMesh() {
  const canvas = document.getElementById('particleCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const COLS = 25, ROWS = 15;
  const mouse = { x: -9999, y: -9999 };
  let w, h, cellW, cellH;

  function resize() {
    w = canvas.width = window.innerWidth;
    h = canvas.height = window.innerHeight;
    cellW = w / (COLS - 1);
    cellH = h / (ROWS - 1);
  }
  resize();
  window.addEventListener('resize', resize);
  window.addEventListener('mousemove', e => { mouse.x = e.clientX; mouse.y = e.clientY; });
  window.addEventListener('mouseleave', () => { mouse.x = -9999; mouse.y = -9999; });

  // Color palette cycling: deep blue -> purple -> pink -> cyan
  const palette = [
    [56, 96, 220],    // deep blue
    [167, 139, 250],  // purple
    [244, 114, 182],  // pink
    [125, 211, 252]   // cyan
  ];
  function paletteAt(t) {
    const n = palette.length;
    const scaled = (t % 1 + 1) % 1 * n;
    const i = Math.floor(scaled);
    const f = scaled - i;
    const a = palette[i];
    const b = palette[(i + 1) % n];
    return [
      a[0] + (b[0] - a[0]) * f,
      a[1] + (b[1] - a[1]) * f,
      a[2] + (b[2] - a[2]) * f
    ];
  }

  const start = performance.now();
  const points = new Array(COLS * ROWS);

  function step(now) {
    const t = (now - start) / 1000;
    ctx.clearRect(0, 0, w, h);

    // Compute point positions
    for (let r = 0; r < ROWS; r++) {
      for (let c = 0; c < COLS; c++) {
        const baseX = c * cellW;
        const baseY = r * cellH;
        // Sine wave displacements with position-based phase offsets
        const dx = Math.sin(t * 0.7 + c * 0.35 + r * 0.22) * 18
                 + Math.cos(t * 0.4 + r * 0.5) * 10;
        const dy = Math.cos(t * 0.6 + r * 0.4 + c * 0.18) * 18
                 + Math.sin(t * 0.5 + c * 0.3) * 10;
        let px = baseX + dx;
        let py = baseY + dy;

        // Mouse repulsion within 150px, max 30px push
        const mdx = px - mouse.x;
        const mdy = py - mouse.y;
        const md2 = mdx * mdx + mdy * mdy;
        if (md2 < 150 * 150 && md2 > 0.01) {
          const md = Math.sqrt(md2);
          const push = (1 - md / 150) * 30;
          px += (mdx / md) * push;
          py += (mdy / md) * push;
        }
        points[r * COLS + c] = { x: px, y: py };
      }
    }

    // Gradient color cycling over time
    const rgb = paletteAt(t * 0.05);
    const rgbStr = `${Math.round(rgb[0])},${Math.round(rgb[1])},${Math.round(rgb[2])}`;
    ctx.lineWidth = 1;

    // Reference "rest" distances for opacity mapping
    const restH = cellW;
    const restV = cellH;

    // Horizontal connections
    for (let r = 0; r < ROWS; r++) {
      for (let c = 0; c < COLS - 1; c++) {
        const a = points[r * COLS + c];
        const b = points[r * COLS + c + 1];
        const dx = a.x - b.x, dy = a.y - b.y;
        const d = Math.sqrt(dx * dx + dy * dy);
        // Closer = more opaque
        const ratio = Math.min(d / (restH * 1.8), 1);
        const alpha = (1 - ratio) * 0.55 + 0.05;
        ctx.strokeStyle = `rgba(${rgbStr},${alpha.toFixed(3)})`;
        ctx.beginPath();
        ctx.moveTo(a.x, a.y);
        ctx.lineTo(b.x, b.y);
        ctx.stroke();
      }
    }
    // Vertical connections
    for (let r = 0; r < ROWS - 1; r++) {
      for (let c = 0; c < COLS; c++) {
        const a = points[r * COLS + c];
        const b = points[(r + 1) * COLS + c];
        const dx = a.x - b.x, dy = a.y - b.y;
        const d = Math.sqrt(dx * dx + dy * dy);
        const ratio = Math.min(d / (restV * 1.8), 1);
        const alpha = (1 - ratio) * 0.55 + 0.05;
        ctx.strokeStyle = `rgba(${rgbStr},${alpha.toFixed(3)})`;
        ctx.beginPath();
        ctx.moveTo(a.x, a.y);
        ctx.lineTo(b.x, b.y);
        ctx.stroke();
      }
    }

    requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
})();

// ---------- Typewriter ----------
const words = ['think', 'see', 'learn', 'play', 'compute', 'help'];
const typeEl = document.getElementById('typeTarget');
let wi = 0, ci = 0, del = false;
function type() {
  const w = words[wi];
  typeEl.textContent = w.slice(0, ci);
  if (!del) {
    ci++;
    if (ci > w.length) { del = true; setTimeout(type, 1400); return; }
    setTimeout(type, 90);
  } else {
    ci--;
    if (ci < 0) { del = false; wi = (wi + 1) % words.length; setTimeout(type, 200); return; }
    setTimeout(type, 45);
  }
}
type();

// ---------- Reveal on load ----------
window.addEventListener('load', () => {
  document.querySelectorAll('.reveal').forEach((el, i) => {
    setTimeout(() => el.classList.add('in'), 1600 + i * 100);
  });
});

// ---------- IntersectionObserver for sections ----------
const io = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('in-view');
      io.unobserve(e.target);
    }
  });
}, { threshold: 0.12, rootMargin: '0px 0px -50px 0px' });

document.querySelectorAll('.section-head, .skill-group, .about-copy, .about-side, .contact-card')
  .forEach(el => io.observe(el));

document.querySelectorAll('.skill-group').forEach((c, i) => {
  c.style.transitionDelay = `${i * 80}ms`;
});
document.querySelectorAll('.contact-card').forEach((c, i) => {
  c.style.transitionDelay = `${i * 80}ms`;
});

// ---------- Scroll-reveal for project cards ----------
const cardObserver = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (!e.isIntersecting) return;
    const delay = parseInt(e.target.dataset.flipDelay || 0, 10);
    setTimeout(() => e.target.classList.add('flipped'), delay);
    cardObserver.unobserve(e.target);
  });
}, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

document.querySelectorAll('.project-card').forEach((c, i) => {
  // Cards stagger by row; both cards in the same row reveal together
  const row = Math.floor(i / 2);
  c.dataset.flipDelay = row * 90;
  cardObserver.observe(c);
});

// ---------- Skill chips spring wave ----------
const skillObserver = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (!e.isIntersecting) return;
    const chips = e.target.querySelectorAll('.chip.spring');
    chips.forEach((chip, i) => {
      setTimeout(() => chip.classList.add('pop'), i * 70);
    });
    skillObserver.unobserve(e.target);
  });
}, { threshold: 0.2 });
document.querySelectorAll('.skill-group').forEach(g => skillObserver.observe(g));

// ---------- Count-up stats with burst ----------
const statObserver = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (!e.isIntersecting) return;
    const el = e.target;
    const target = parseInt(el.dataset.target, 10);
    const dur = 1200;
    const start = performance.now();
    function tick(now) {
      const t = Math.min(1, (now - start) / dur);
      const eased = 1 - Math.pow(1 - t, 3);
      el.textContent = Math.round(target * eased) + (t === 1 ? '+' : '');
      if (t < 1) requestAnimationFrame(tick);
      else spawnBurst(el);
    }
    requestAnimationFrame(tick);
    statObserver.unobserve(el);
  });
}, { threshold: 0.5 });
document.querySelectorAll('.stat-num').forEach(el => statObserver.observe(el));

function spawnBurst(el) {
  const parent = el.parentElement;
  if (!parent) return;
  const burst = document.createElement('div');
  burst.className = 'stat-burst';
  const rect = el.getBoundingClientRect();
  const prect = parent.getBoundingClientRect();
  burst.style.left = (rect.left - prect.left + rect.width / 2) + 'px';
  burst.style.top = (rect.top - prect.top + rect.height / 2) + 'px';
  const colors = ['#7dd3fc', '#a78bfa', '#f472b6', '#34d399'];
  for (let i = 0; i < 14; i++) {
    const p = document.createElement('span');
    const angle = (Math.PI * 2 * i) / 14;
    const dist = 40 + Math.random() * 30;
    p.style.setProperty('--bx', Math.cos(angle) * dist + 'px');
    p.style.setProperty('--by', Math.sin(angle) * dist + 'px');
    p.style.background = colors[i % colors.length];
    p.style.boxShadow = `0 0 8px ${colors[i % colors.length]}`;
    p.style.animationDelay = (i * 15) + 'ms';
    burst.appendChild(p);
  }
  parent.style.position = 'relative';
  parent.appendChild(burst);
  setTimeout(() => burst.remove(), 1200);
}

// ---------- Build chessboard ----------
const cb = document.querySelector('.chessboard');
if (cb) {
  for (let r = 0; r < 8; r++) {
    for (let c = 0; c < 8; c++) {
      const sq = document.createElement('div');
      sq.className = ((r + c) % 2 === 0) ? 'light' : 'dark';
      cb.appendChild(sq);
    }
  }
}


// ---------- Periodic re-glitch of hero name ----------
setInterval(() => {
  if (document.hidden) return;
  triggerGlitch();
}, 9000);
