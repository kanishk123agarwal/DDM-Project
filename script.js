/* ============================================================
   script.js — DDM Portfolio Animations & Interactions
   ============================================================ */

// ===== PARTICLE CANVAS =====
(function initParticles() {
  const canvas = document.getElementById('particle-canvas');
  const ctx    = canvas.getContext('2d');

  let W, H, particles = [], animId;
  const PARTICLE_COUNT = 120;
  const COLORS = ['#6C63FF', '#00D2FF', '#FF6B9D', '#43E97B', '#FFB347'];

  let mouse = { x: null, y: null, radius: 100 };

  window.addEventListener('mousemove', e => {
    mouse.x = e.x;
    mouse.y = e.y;
  });
  window.addEventListener('mouseout', () => {
    mouse.x = undefined;
    mouse.y = undefined;
  });

  // Explosion effect on click
  window.addEventListener('click', e => {
    for (let i = 0; i < 15; i++) {
        particles.push(new ExplosionParticle(e.x, e.y));
    }
  });

  function resize() {
    W = canvas.width  = window.innerWidth;
    H = canvas.height = window.innerHeight;
  }

  class Particle {
    constructor() { this.reset(true); }
    reset(init = false) {
      this.x  = Math.random() * W;
      this.y  = init ? Math.random() * H : H + 10;
      this.r  = Math.random() * 2 + 0.5;
      this.vx = (Math.random() - 0.5) * 0.4;
      this.vy = -(Math.random() * 0.5 + 0.2);
      this.alpha  = Math.random() * 0.6 + 0.1;
      this.color  = COLORS[Math.floor(Math.random() * COLORS.length)];
      this.dAlpha = (Math.random() * 0.002 + 0.001) * (Math.random() < 0.5 ? 1 : -1);
      this.isExplosion = false;
    }
    update() {
      // Repel from mouse
      if (mouse.x != null) {
        let dx = mouse.x - this.x;
        let dy = mouse.y - this.y;
        let distance = Math.sqrt(dx * dx + dy * dy);
        if (distance < mouse.radius) {
          const forceDirectionX = dx / distance;
          const forceDirectionY = dy / distance;
          const maxDistance = mouse.radius;
          const force = (maxDistance - distance) / maxDistance;
          const directionX = forceDirectionX * force * 5;
          const directionY = forceDirectionY * force * 5;
          this.x -= directionX;
          this.y -= directionY;
        }
      }

      this.x += this.vx;
      this.y += this.vy;
      this.alpha += this.dAlpha;
      if (this.alpha > 0.7 || this.alpha < 0.05) this.dAlpha *= -1;
      if (this.y < -10 || this.x < -10 || this.x > W + 10) this.reset();
    }
    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
      ctx.fillStyle = this.color;
      ctx.globalAlpha = Math.max(0, this.alpha);
      ctx.fill();
    }
  }

  class ExplosionParticle extends Particle {
    constructor(x, y) {
      super();
      this.x = x;
      this.y = y;
      this.vx = (Math.random() - 0.5) * 10;
      this.vy = (Math.random() - 0.5) * 10;
      this.alpha = 1;
      this.dAlpha = -0.02;
      this.r = Math.random() * 4 + 1;
      this.isExplosion = true;
    }
    update() {
      this.x += this.vx;
      this.y += this.vy;
      this.alpha += this.dAlpha;
      if (this.alpha <= 0) {
          particles.splice(particles.indexOf(this), 1);
      }
    }
  }

  function drawConnections() {
    ctx.globalAlpha = 1;
    for (let i = 0; i < particles.length; i++) {
        // Skip connections for explosion particles
      if(particles[i].isExplosion) continue;
      for (let j = i + 1; j < particles.length; j++) {
        if(particles[j].isExplosion) continue;
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 120) {
          ctx.beginPath();
          ctx.strokeStyle = particles[i].color;
          ctx.globalAlpha = (1 - dist / 120) * 0.08;
          ctx.lineWidth = 0.5;
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.stroke();
        }
      }
    }
  }

  function loop() {
    ctx.clearRect(0, 0, W, H);
    // iterate backwards to safely remove explosion particles
    for(let i = particles.length - 1; i >= 0; i--) {
        particles[i].update();
        particles[i].draw();
    }
    drawConnections();
    ctx.globalAlpha = 1;
    animId = requestAnimationFrame(loop);
  }

  window.addEventListener('resize', resize);
  resize();
  for (let i = 0; i < PARTICLE_COUNT; i++) particles.push(new Particle());
  loop();
})();


// ===== NAVBAR SCROLL EFFECT =====
(function initNavbar() {
  const navbar = document.getElementById('navbar');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 60) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  }, { passive: true });
})();


// ===== SMOOTH ACTIVE NAV LINK HIGHLIGHT =====
(function initActivNav() {
  const sections = document.querySelectorAll('section[id]');
  const links    = document.querySelectorAll('.nav-links a');

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        links.forEach(a => a.style.color = '');
        const active = document.querySelector(`.nav-links a[href="#${entry.target.id}"]`);
        if (active) active.style.color = 'var(--text-primary)';
      }
    });
  }, { threshold: 0.35 });

  sections.forEach(s => observer.observe(s));
})();


// ===== SCROLL REVEAL =====
(function initReveal() {
  const els = document.querySelectorAll('.reveal');
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

  els.forEach(el => observer.observe(el));
})();


// ===== ANIMATED COUNTER =====
(function initCounters() {
  function animateCounter(el, from, to, suffix, duration) {
    const start = performance.now();
    function tick(now) {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3); // easeOutCubic
      const value = Math.floor(from + (to - from) * eased);
      el.textContent = value + suffix;
      if (progress < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  const counters = [
    { id: 'counter-labs',   from: 0,  to: 3,  suffix: ''  },
    { id: 'counter-files',  from: 0,  to: 25, suffix: '+' },
    { id: 'counter-models', from: 0,  to: 3,  suffix: ''  },
  ];

  // trigger when hero stats come into view
  const statsEl = document.querySelector('.hero-stats');
  if (statsEl) {
    const obs = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        counters.forEach(c => {
          const el = document.getElementById(c.id);
          if (el) animateCounter(el, c.from, c.to, c.suffix, 1400);
        });
        obs.disconnect();
      }
    }, { threshold: 0.5 });
    obs.observe(statsEl);
  }
})();


// ===== GLASS CARD 3D TILT =====
(function initTilt() {
  const cards = document.querySelectorAll('.glass-card');
  const MAX_TILT = 8; // degrees

  cards.forEach(card => {
    // Add preserve-3d to children automatically
    card.style.transformStyle = 'preserve-3d';
    Array.from(card.children).forEach(child => {
      child.style.transform = 'translateZ(30px)';
      child.style.transition = 'transform 0.3s ease';
    });

    card.addEventListener('mousemove', e => {
      const rect = card.getBoundingClientRect();
      const cx = rect.left + rect.width  / 2;
      const cy = rect.top  + rect.height / 2;
      const dx = (e.clientX - cx) / (rect.width  / 2);
      const dy = (e.clientY - cy) / (rect.height / 2);
      card.style.transform = `perspective(800px) translateY(-6px) rotateY(${dx * MAX_TILT}deg) rotateX(${-dy * MAX_TILT}deg)`;
    });
    card.addEventListener('mouseleave', () => {
      card.style.transform = '';
    });
  });
})();

// ===== 3D HERO PARALLAX =====
(function initHero3D() {
  const heroInner = document.querySelector('.hero-inner');
  if (!heroInner) return;
  
  heroInner.style.transformStyle = 'preserve-3d';
  const children = Array.from(heroInner.children);
  children.forEach((c, idx) => {
    c.style.transform = `translateZ(${(idx + 1) * 20}px)`;
    c.style.transition = 'transform 0.1s ease-out';
  });

  document.addEventListener('mousemove', e => {
    const x = (e.clientX / window.innerWidth - 0.5) * 15;
    const y = (e.clientY / window.innerHeight - 0.5) * -15;
    heroInner.style.transform = `perspective(1000px) rotateY(${x}deg) rotateX(${y}deg)`;
  });
})();


// ===== CURSOR GLOW EFFECT =====
(function initCursorGlow() {
  const glow = document.createElement('div');
  glow.style.cssText = `
    position: fixed;
    width: 320px;
    height: 320px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(108,99,255,0.07) 0%, transparent 70%);
    pointer-events: none;
    z-index: 999;
    transform: translate(-50%, -50%);
    transition: left 0.12s ease, top 0.12s ease;
  `;
  document.body.appendChild(glow);

  window.addEventListener('mousemove', e => {
    glow.style.left = e.clientX + 'px';
    glow.style.top  = e.clientY + 'px';
  }, { passive: true });
})();


// ===== TYPING EFFECT on hero badge =====
(function initTyping() {
  const badge = document.querySelector('.hero-badge');
  if (!badge) return;
  const originalText = badge.childNodes[badge.childNodes.length - 1].textContent.trim();
  badge.childNodes[badge.childNodes.length - 1].textContent = ' ';
  let i = 0;
  function type() {
    if (i <= originalText.length) {
      badge.childNodes[badge.childNodes.length - 1].textContent = ' ' + originalText.slice(0, i);
      i++;
      setTimeout(type, 50);
    }
  }
  setTimeout(type, 800);
})();


// ===== SMOOTH SECTION GLOW on scroll =====
(function initSectionGlow() {
  const blobs = document.querySelectorAll('.blob');
  window.addEventListener('scroll', () => {
    const sy = window.scrollY;
    const maxScroll = document.body.scrollHeight - window.innerHeight;
    const pct = sy / maxScroll;
    blobs[0] && (blobs[0].style.transform = `translate(${pct * 40}px, ${-pct * 60}px) scale(${1 + pct * 0.2})`);
    blobs[1] && (blobs[1].style.transform = `translate(${-pct * 30}px, ${pct * 40}px) scale(${1 + pct * 0.15})`);
    blobs[2] && (blobs[2].style.transform = `translate(${pct * 20}px, ${-pct * 20}px) scale(${0.9 + pct * 0.2})`);
  }, { passive: true });
})();


// ===== FILE CARD HOVER COLOR =====
(function initFileCards() {
  const fileCards = document.querySelectorAll('.file-card');
  const colors = ['var(--accent1)', 'var(--accent2)', 'var(--accent3)', 'var(--accent4)', 'var(--accent5)'];
  fileCards.forEach((card, i) => {
    card.addEventListener('mouseenter', () => {
      card.style.borderColor = colors[i % colors.length];
    });
    card.addEventListener('mouseleave', () => {
      card.style.borderColor = '';
    });
  });
})();


// ===== PROGRESS BARS in metric pills =====
(function initMetricBars() {
  const pills = document.querySelectorAll('.metric-pill');
  const obs = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const num = entry.target.querySelector('.mp-num');
        if (num && !num.dataset.animated) {
          num.dataset.animated = '1';
          num.style.transition = 'opacity 0.5s ease';
          num.style.opacity = '0';
          setTimeout(() => { num.style.opacity = '1'; }, 100);
        }
      }
    });
  }, { threshold: 0.5 });
  pills.forEach(p => obs.observe(p));
})();


// ===== TOPIC LIST STAGGER =====
(function initTopicStagger() {
  const lists = document.querySelectorAll('.topic-list');
  lists.forEach(list => {
    const items = list.querySelectorAll('li');
    const obs = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        items.forEach((item, i) => {
          item.style.opacity = '0';
          item.style.transform = 'translateY(10px)';
          item.style.transition = `opacity 0.35s ease ${i * 50}ms, transform 0.35s ease ${i * 50}ms`;
          setTimeout(() => {
            item.style.opacity = '1';
            item.style.transform = 'translateY(0)';
          }, 100 + i * 50);
        });
        obs.disconnect();
      }
    }, { threshold: 0.3 });
    obs.observe(list);
  });
})();

console.log('%cDDM Portfolio loaded ✅', 'color:#6C63FF; font-size:14px; font-weight:bold;');


// ===== TAB SWITCHER =====
function showTab(labId, panelId) {
  // hide all panels in this lab's code-tab
  const allPanels = document.querySelectorAll(`#${labId}-tabs`).length
    ? document.querySelectorAll(`#${labId}-tabs`)[0].closest('.code-tabs').querySelectorAll('.tab-panel')
    : [];
  allPanels.forEach(p => p.classList.remove('active'));

  // deactivate all buttons in this tab bar
  const allBtns = document.querySelectorAll(`#${labId}-tabs .tab-btn`);
  allBtns.forEach(b => b.classList.remove('active'));

  // activate selected
  const panel = document.getElementById(`${labId}-${panelId}`);
  const btn   = document.getElementById(`tab-${labId}-${panelId}`);
  if (panel) panel.classList.add('active');
  if (btn)   btn.classList.add('active');

  // re-run Prism highlight on visible code
  if (window.Prism) {
    setTimeout(() => Prism.highlightAll(), 50);
  }
}

// ===== COPY CODE BUTTON =====
function copyCode(btn) {
  const panel = btn.closest('.tab-panel');
  const code  = panel ? panel.querySelector('code') : null;
  if (!code) return;
  navigator.clipboard.writeText(code.textContent).then(() => {
    btn.textContent = 'Copied!';
    btn.classList.add('copied');
    setTimeout(() => {
      btn.textContent = 'Copy';
      btn.classList.remove('copied');
    }, 2000);
  });
}

// ===== THEME TOGGLE =====
(function initThemeToggle() {
  const toggleBtn = document.getElementById('theme-toggle');
  if (!toggleBtn) return;

  const currentTheme = localStorage.getItem('theme') || 'dark';
  document.documentElement.setAttribute('data-theme', currentTheme);

  toggleBtn.addEventListener('click', () => {
    const isLight = document.documentElement.getAttribute('data-theme') === 'light';
    const newTheme = isLight ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
  });
})();
