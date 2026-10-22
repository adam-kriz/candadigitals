(() => {
  const root = document.documentElement;
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const canHover = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  const hasGsap = typeof window.gsap !== 'undefined' && typeof window.ScrollTrigger !== 'undefined';

  // Without GSAP (or with reduced motion) everything just shows up, no animations.
  if (!hasGsap || reduceMotion) root.classList.remove('js');
  if (hasGsap) gsap.registerPlugin(ScrollTrigger);

  /* Smooth scroll */
  let lenis = null;
  if (hasGsap && !reduceMotion && typeof window.Lenis !== 'undefined') {
    lenis = new Lenis({ lerp: 0.1 });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add((t) => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
  }

  const scrollToTarget = (target) => {
    if (lenis) lenis.scrollTo(target, { offset: 0, duration: 1.4 });
    else (typeof target === 'number' ? window.scrollTo({ top: target, behavior: reduceMotion ? 'auto' : 'smooth' }) : target.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth' }));
  };

  /* Menu */
  const menuBtn = document.querySelector('.menu-btn');
  const menu = document.getElementById('menu');
  const header = document.querySelector('.header');

  /* Frosted header once the page has scrolled */
  const onScrollHeader = () => header.classList.toggle('is-scrolled', window.scrollY > 10);
  onScrollHeader();
  window.addEventListener('scroll', onScrollHeader, { passive: true });
  const animateMenu = hasGsap && !reduceMotion;
  const menuItems = menu.querySelectorAll('li, .menu-foot');
  // The overlay wipes down to open and back up to close, with a soft rounded edge.
  const shut = 'inset(0% 0% 100% 0% round 0px 0px 50% 50%)';
  const full = 'inset(0% 0% 0% 0% round 0px 0px 0% 0%)';
  let menuOpen = false;
  let menuTl = null;

  const setMenu = (open) => {
    if (open === menuOpen) return;
    menuOpen = open;
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.classList.toggle('menu-open-state', open);
    if (open) header.classList.add('menu-on');
    document.body.style.overflow = open ? 'hidden' : '';
    if (lenis) open ? lenis.stop() : lenis.start();
    if (menuTl) menuTl.kill();

    if (!animateMenu) { menu.hidden = !open; header.classList.toggle('menu-on', open); return; }

    if (open) {
      menu.hidden = false;
      menuTl = gsap.timeline()
        .fromTo(menu, { clipPath: shut }, { clipPath: full, duration: 0.9, ease: 'expo.inOut' })
        .fromTo(menuItems, { yPercent: 80, opacity: 0 }, { yPercent: 0, opacity: 1, duration: 0.8, stagger: 0.05, ease: 'expo.out' }, 0.35);
    } else {
      menuTl = gsap.timeline({ onComplete: () => { menu.hidden = true; header.classList.remove('menu-on'); } })
        .to(menuItems, { yPercent: -40, opacity: 0, duration: 0.35, stagger: 0.03, ease: 'power2.in' })
        .to(menu, { clipPath: shut, duration: 0.8, ease: 'expo.inOut' }, 0.15);
    }
  };
  menuBtn.addEventListener('click', () => setMenu(!menuOpen));
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && menuOpen) { setMenu(false); menuBtn.focus(); } });

  /* In-page links (menu, "Your business", brand) */
  document.querySelectorAll('a[href^="#"]').forEach((a) => {
    a.addEventListener('click', (e) => {
      const id = a.getAttribute('href');
      const target = id === '#top' ? 0 : document.querySelector(id);
      if (target === null) return;
      e.preventDefault();
      if (menuOpen) setMenu(false);
      scrollToTarget(target);
    });
  });
  document.querySelector('.to-top').addEventListener('click', () => scrollToTarget(0));

  /* Clocks: Florida and Prague */
  const clocks = document.querySelectorAll('.clock');
  const tick = () => clocks.forEach((c) => {
    c.querySelector('.clock-time').textContent = new Intl.DateTimeFormat('en-US', {
      hour: 'numeric', minute: '2-digit', timeZone: c.dataset.tz
    }).format(new Date());
  });
  tick();
  setInterval(tick, 15000);

  /* Copy email */
  document.querySelectorAll('.copy').forEach((btn) => {
    btn.addEventListener('click', async () => {
      const done = btn.parentElement.querySelector('.copy-done');
      try {
        await navigator.clipboard.writeText(btn.dataset.copy);
        done.textContent = 'Copied to clipboard.';
      } catch (_) {
        done.textContent = 'Copy failed, select the address instead.';
      }
      setTimeout(() => { done.textContent = ''; }, 2500);
    });
  });

  /* Services: one open at a time */
  const accItems = document.querySelectorAll('.acc-item');
  accItems.forEach((item) => item.addEventListener('toggle', () => {
    if (item.open) accItems.forEach((other) => { if (other !== item) other.open = false; });
  }));

  /* Work: preview follows the cursor */
  const preview = document.querySelector('.work-preview');
  if (canHover && hasGsap && preview) {
    const img = preview.querySelector('img');
    const xTo = gsap.quickTo(preview, 'x', { duration: 0.5, ease: 'power3' });
    const yTo = gsap.quickTo(preview, 'y', { duration: 0.5, ease: 'power3' });
    // Check what is under the pointer on every move AND every scroll: when the page
    // scrolls under a still mouse, no mouseleave fires and the preview would get stuck.
    let px = -1, py = -1, current = null;
    const update = () => {
      const el = px < 0 ? null : document.elementFromPoint(px, py);
      const row = el ? el.closest('.work-row[data-img]') : null;
      if (row === current) return;
      current = row;
      if (row) {
        img.src = row.dataset.img;
        gsap.to(preview, { opacity: 1, scale: 1, duration: 0.4, ease: 'power3.out', overwrite: 'auto' });
      } else {
        gsap.to(preview, { opacity: 0, scale: 0.85, duration: 0.3, overwrite: 'auto' });
      }
    };
    window.addEventListener('mousemove', (e) => { px = e.clientX; py = e.clientY; xTo(px); yTo(py); update(); });
    window.addEventListener('scroll', update, { passive: true });
    document.addEventListener('mouseleave', () => { px = -1; update(); });
  }

  /* Magnetic buttons */
  if (canHover && hasGsap && !reduceMotion) {
    document.querySelectorAll('.magnetic').forEach((el) => {
      const inner = el.querySelector('span');
      el.addEventListener('mousemove', (e) => {
        const r = el.getBoundingClientRect();
        const x = e.clientX - r.left - r.width / 2;
        const y = e.clientY - r.top - r.height / 2;
        gsap.to(el, { x: x * 0.3, y: y * 0.4, duration: 0.5, ease: 'power3.out' });
        if (inner) gsap.to(inner, { x: x * 0.15, y: y * 0.2, duration: 0.5, ease: 'power3.out' });
      });
      el.addEventListener('mouseleave', () => {
        gsap.to([el, inner].filter(Boolean), { x: 0, y: 0, duration: 0.8, ease: 'elastic.out(1, 0.4)' });
      });
    });
  }

  /* Intro text: words light up while scrolling */
  const intro = document.querySelector('.intro-text');
  intro.innerHTML = intro.textContent.trim().split(/\s+/).map((w) => `<span class="w">${w}</span>`).join(' ');
  const words = intro.querySelectorAll('.w');

  if (!hasGsap || reduceMotion) {
    intro.classList.add('no-scrub');
  } else {
    ScrollTrigger.create({
      trigger: intro, start: 'top 80%', end: 'bottom 45%', scrub: true,
      onUpdate: (self) => {
        const lit = Math.round(self.progress * words.length);
        words.forEach((w, i) => { w.style.opacity = i < lit ? 1 : 0.18; });
      }
    });
  }

  /* Entrance and scroll animations */
  if (hasGsap && !reduceMotion) {
    const heroWords = document.querySelectorAll('.hero-title .word');
    gsap.timeline({ defaults: { ease: 'expo.out' } })
      .from(heroWords, { yPercent: 110, duration: 1.3, stagger: 0.08 })
      .from('.hero-layers .layer', { y: -60, opacity: 0, duration: 1.2, stagger: 0.12 }, 0.3)
      .to('.hero .fade', { opacity: 1, y: 0, duration: 1, stagger: 0.1 }, 0.6);

    // The three layers of the logo drift apart as you scroll away from the hero.
    // This moves the shapes inside each layer, while the entrance above moves the
    // layer groups, so scrolling during the entrance can't leave the logo scattered.
    gsap.timeline({ scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } })
      .fromTo('.layer-1 > *', { y: 0 }, { y: -70, immediateRender: false }, 0)
      .fromTo('.layer-3 > *', { y: 0 }, { y: 70, immediateRender: false }, 0)
      .to('.hero-layers', { rotate: -8 }, 0);

    // Small tilt toward the mouse.
    if (canHover) {
      const layers = document.querySelector('.hero-layers');
      const rx = gsap.quickTo(layers, 'rotationY', { duration: 0.8, ease: 'power3' });
      const ry = gsap.quickTo(layers, 'rotationX', { duration: 0.8, ease: 'power3' });
      gsap.set(layers, { transformPerspective: 800 });
      window.addEventListener('mousemove', (e) => {
        rx((e.clientX / window.innerWidth - 0.5) * 30);
        ry((e.clientY / window.innerHeight - 0.5) * -30);
      });
    }

    document.querySelectorAll('.section-title, .contact-title').forEach((el) => {
      gsap.from(el, { yPercent: 40, opacity: 0, duration: 1.2, ease: 'expo.out', scrollTrigger: { trigger: el, start: 'top 88%' } });
    });

    gsap.utils.toArray('.work-row, .acc-item, .pkg, .step, .extras-list li').forEach((el) => {
      gsap.from(el, { y: 40, opacity: 0, duration: 1, ease: 'expo.out', scrollTrigger: { trigger: el, start: 'top 92%' } });
    });

    gsap.fromTo('.steps', { '--progress': 0 }, {
      '--progress': 1, ease: 'none',
      scrollTrigger: { trigger: '.steps', start: 'top 80%', end: 'bottom 55%', scrub: true }
    });

    gsap.from('.footer-word', { yPercent: 60, duration: 1.4, ease: 'expo.out', scrollTrigger: { trigger: '.footer', start: 'top 85%' } });
  }

  /* "I need..." chips */
  const chipsBox = document.querySelector('.chips');
  const chips = [...chipsBox.querySelectorAll('.chip')];
  let dragDistance = 0;
  chips.forEach((chip) => chip.addEventListener('click', (e) => {
    if (dragDistance > 6) { e.preventDefault(); return; }
    chip.setAttribute('aria-pressed', String(chip.getAttribute('aria-pressed') !== 'true'));
  }));

  const usePhysics = typeof window.Matter !== 'undefined' && !reduceMotion && canHover && window.innerWidth >= 700;
  if (usePhysics) startPhysics();

  function startPhysics() {
    const { Engine, Bodies, Composite, Mouse, MouseConstraint, Events, Body, Sleeping } = Matter;
    chipsBox.classList.add('is-physics');
    let W = chipsBox.clientWidth;
    let H = chipsBox.clientHeight;

    // Sleeping stops resting chips from jittering; more iterations keep stacks stable.
    const engine = Engine.create({ gravity: { y: 1 }, enableSleeping: true, positionIterations: 12, velocityIterations: 8 });

    // Thick walls so a hard throw can't tunnel through them in a single step.
    const T = 400;
    const wallOpts = { isStatic: true, friction: 0.5, restitution: 0.2 };
    let walls = [];
    // Chips fall in from above, so the box starts open at the top. The ceiling goes
    // in the moment every chip is fully inside, and from then on nothing can fly out.
    let ceiling = false;
    const buildWalls = () => {
      if (walls.length) Composite.remove(engine.world, walls);
      walls = [
        Bodies.rectangle(W / 2, H + T / 2, W + T * 2, T, wallOpts),
        Bodies.rectangle(-T / 2, H / 2 - T, T, H + T * 4, wallOpts),
        Bodies.rectangle(W + T / 2, H / 2 - T, T, H + T * 4, wallOpts)
      ];
      if (ceiling) walls.push(Bodies.rectangle(W / 2, -T / 2, W + T * 2, T, wallOpts));
      Composite.add(engine.world, walls);
    };
    buildWalls();

    // Start every chip at a random, non-overlapping spot high above the box, tilted
    // at a random angle and with a small random nudge, so they drop in out of nowhere
    // and tumble down differently every time.
    const start = [];
    const placed = [];
    const SKY = 420; // how far above the box the chips can start
    chips.forEach((chip, i) => {
      const w = chip.offsetWidth;
      const h = chip.offsetHeight;
      let spot = null;
      for (let tries = 0; tries < 80 && !spot; tries++) {
        const x = w / 2 + 6 + Math.random() * Math.max(1, W - w - 12);
        const y = -h - Math.random() * SKY;
        const r = { l: x - w / 2 - 6, r: x + w / 2 + 6, t: y - h / 2 - 6, b: y + h / 2 + 6 };
        if (!placed.some((p) => r.l < p.r && r.r > p.l && r.t < p.b && r.b > p.t)) { spot = { x, y }; placed.push(r); }
      }
      start[i] = spot || { x: w / 2 + Math.random() * (W - w), y: -h - SKY - i * h };
    });
    const pairs = chips.map((chip, i) => {
      const w = chip.offsetWidth;
      const h = chip.offsetHeight;
      const body = Bodies.rectangle(start[i].x, start[i].y, w, h,
        { chamfer: { radius: h / 2 }, restitution: 0.15, friction: 0.45, frictionStatic: 0.7, frictionAir: 0.025, sleepThreshold: 40 });
      Body.setAngle(body, (Math.random() - 0.5) * 1.2);
      return { chip, body, w, h };
    });
    const nudge = () => pairs.forEach(({ body }) => {
      Body.setVelocity(body, { x: (Math.random() - 0.5) * 4, y: Math.random() * 3 });
      Body.setAngularVelocity(body, (Math.random() - 0.5) * 0.12);
    });
    const clamp = (v, lo, hi) => Math.min(Math.max(v, lo), hi);

    // Dragging. Matter listens on the box only, so letting go outside it used to leave
    // a chip stuck to the cursor; move and release are now heard on the whole window.
    const mouse = Mouse.create(chipsBox);
    ['mousewheel', 'DOMMouseScroll', 'wheel'].forEach((ev) => chipsBox.removeEventListener(ev, mouse.mousewheel));
    chipsBox.removeEventListener('mousemove', mouse.mousemove);
    chipsBox.removeEventListener('mouseup', mouse.mouseup);
    window.addEventListener('mousemove', mouse.mousemove);
    window.addEventListener('mouseup', mouse.mouseup);
    const mc = MouseConstraint.create(engine, {
      mouse, constraint: { stiffness: 0.12, damping: 0.08, angularStiffness: 0, render: { visible: false } }
    });
    Composite.add(engine.world, mc);
    Events.on(mc, 'startdrag', () => chipsBox.classList.add('is-grabbing'));
    Events.on(mc, 'enddrag', () => chipsBox.classList.remove('is-grabbing'));

    let downAt = null;
    chipsBox.addEventListener('mousedown', (e) => { downAt = { x: e.clientX, y: e.clientY }; dragDistance = 0; });
    window.addEventListener('mousemove', (e) => { if (downAt) dragDistance = Math.hypot(e.clientX - downAt.x, e.clientY - downAt.y); });
    window.addEventListener('mouseup', () => { downAt = null; setTimeout(() => { dragDistance = 0; }, 0); });

    const MAX_SPEED = 20;
    Events.on(engine, 'beforeUpdate', () => {
      pairs.forEach(({ body }) => {
        // Cap the speed of a throw so nothing flies off wildly.
        if (body.speed > MAX_SPEED) Body.setVelocity(body, { x: body.velocity.x * MAX_SPEED / body.speed, y: body.velocity.y * MAX_SPEED / body.speed });
        if (Math.abs(body.angularVelocity) > 0.25) Body.setAngularVelocity(body, Math.sign(body.angularVelocity) * 0.25);
      });
    });
    Events.on(engine, 'afterUpdate', () => {
      if (!ceiling) {
        const allIn = pairs.every(({ body }) => body.bounds.min.y > 2);
        // Fallback: if a chip is still hanging above after 4 s (say it was grabbed and
        // held up there), tuck it inside so the ceiling can close.
        if (!allIn && engine.timing.timestamp > 4000 && !mc.body) {
          pairs.forEach(({ body, w, h }) => {
            if (body.bounds.min.y <= 2) {
              Body.setPosition(body, { x: clamp(body.position.x, w / 2, W - w / 2), y: h });
              Body.setVelocity(body, { x: 0, y: 0 });
            }
          });
        }
        if (allIn || (engine.timing.timestamp > 4000 && !mc.body)) { ceiling = true; buildWalls(); }
      }
      // Safety net: anything that still ends up outside the box is put back inside.
      pairs.forEach(({ body, w, h }) => {
        const out = body.position.x < -w / 2 || body.position.x > W + w / 2 || body.position.y > H + h || body.position.y < (ceiling ? -h / 2 : -SKY - h * 12);
        if (out) {
          Body.setPosition(body, { x: clamp(body.position.x, w / 2, W - w / 2), y: H - h });
          Body.setVelocity(body, { x: 0, y: 0 });
        }
      });
    });

    const render = () => pairs.forEach(({ chip, body, w, h }) => {
      chip.style.transform = `translate3d(${body.position.x - w / 2}px, ${body.position.y - h / 2}px, 0) rotate(${body.angle}rad)`;
    });
    render(); // the chips wait above the box (hidden by its overflow) until it scrolls into view

    // Fixed small time steps, drawn every animation frame: smoother than Matter's Runner.
    const STEP = 1000 / 120;
    let running = false, last = 0, acc = 0;
    const frame = (t) => {
      if (!running) return;
      acc += last ? Math.min(t - last, 100) : STEP;
      last = t;
      while (acc >= STEP) { Engine.update(engine, STEP); acc -= STEP; }
      render();
      requestAnimationFrame(frame);
    };
    const setRunning = (on) => {
      if (on === running) return;
      running = on;
      if (on) { last = 0; acc = 0; requestAnimationFrame(frame); }
    };

    // Start when the box is in view, pause whenever it's scrolled away.
    let started = false;
    new IntersectionObserver((entries) => {
      const e = entries[0];
      if (!started && e.intersectionRatio >= 0.4) {
        started = true;
        Composite.add(engine.world, pairs.map((p) => p.body));
        nudge();
      }
      if (started) setRunning(e.isIntersecting);
    }, { threshold: [0, 0.4] }).observe(chipsBox);

    // Keep the walls on the box edges when the window is resized.
    new ResizeObserver(() => {
      const nw = chipsBox.clientWidth;
      const nh = chipsBox.clientHeight;
      if (nw === W && nh === H) return;
      W = nw; H = nh;
      buildWalls();
      pairs.forEach(({ body, w }) => {
        Sleeping.set(body, false);
        if (body.position.x > W - w / 2 || body.position.x < w / 2) Body.setPosition(body, { x: clamp(body.position.x, w / 2, W - w / 2), y: body.position.y });
      });
      if (!running) render();
    }).observe(chipsBox);
  }

  /* Form → /api/contact (Cloudflare Pages Function → email through Resend) */
  const form = document.querySelector('.form');
  const status = form.querySelector('.form-status');
  const sendBtn = form.querySelector('button[type="submit"]');
  form.addEventListener('input', (e) => e.target.removeAttribute('aria-invalid'));
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    let ok = true;
    ['name', 'email'].forEach((n) => {
      const f = form.elements[n];
      const bad = !f.value.trim() || (n === 'email' && !/^\S+@\S+\.\S+$/.test(f.value));
      f.setAttribute('aria-invalid', String(bad));
      if (bad) ok = false;
    });
    if (!ok) { status.textContent = 'Please add your name and a valid email.'; return; }
    form.elements.needs.value = chips.filter((c) => c.getAttribute('aria-pressed') === 'true').map((c) => c.textContent).join(', ');

    sendBtn.disabled = true;
    status.textContent = 'Sending…';
    let result = null;
    try {
      const res = await fetch(form.action, { method: 'POST', body: new FormData(form) });
      result = await res.json();
    } catch (_) { /* network error or no backend (local preview) */ }

    if (result && result.ok) {
      form.reset();
      chips.forEach((c) => c.setAttribute('aria-pressed', 'false'));
      status.textContent = 'Thanks! We got your message and will get back to you within one business day.';
    } else if (result && result.error === 'turnstile') {
      status.textContent = 'The spam check didn\'t go through. Please wait a moment and try again.';
    } else {
      status.textContent = 'Sorry, that didn\'t send. Please email us at candadigitals@gmail.com.';
    }
    if (window.turnstile) window.turnstile.reset();
    sendBtn.disabled = false;
  });
})();
