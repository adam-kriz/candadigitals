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
    document.body.style.overflow = open ? 'hidden' : '';
    if (lenis) open ? lenis.stop() : lenis.start();
    if (menuTl) menuTl.kill();

    if (!animateMenu) { menu.hidden = !open; return; }

    if (open) {
      menu.hidden = false;
      menuTl = gsap.timeline()
        .fromTo(menu, { clipPath: shut }, { clipPath: full, duration: 0.9, ease: 'expo.inOut' })
        .fromTo(menuItems, { yPercent: 80, opacity: 0 }, { yPercent: 0, opacity: 1, duration: 0.8, stagger: 0.05, ease: 'expo.out' }, 0.35);
    } else {
      menuTl = gsap.timeline({ onComplete: () => { menu.hidden = true; } })
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
    const { Engine, Runner, Bodies, Composite, Mouse, MouseConstraint, Events, Body } = Matter;
    chipsBox.classList.add('is-physics');
    const W = chipsBox.clientWidth;
    const H = chipsBox.clientHeight;
    const engine = Engine.create({ gravity: { y: 1 } });
    const wall = { isStatic: true };
    Composite.add(engine.world, [
      Bodies.rectangle(W / 2, H + 50, W * 2, 100, wall),
      Bodies.rectangle(-50, H / 2, 100, H * 3, wall),
      Bodies.rectangle(W + 50, H / 2, 100, H * 3, wall)
    ]);

    const pairs = chips.map((chip, i) => {
      const w = chip.offsetWidth;
      const h = chip.offsetHeight;
      const body = Bodies.rectangle(
        w / 2 + Math.random() * Math.max(1, W - w),
        -h - i * 70,
        w, h,
        { chamfer: { radius: h / 2 }, restitution: 0.35, friction: 0.3, frictionAir: 0.015 }
      );
      Body.setAngle(body, (Math.random() - 0.5) * 0.6);
      return { chip, body, w, h };
    });

    const mouse = Mouse.create(chipsBox);
    // Matter grabs the scroll wheel by default; give it back to the page.
    ['mousewheel', 'DOMMouseScroll', 'wheel'].forEach((ev) => mouse.element.removeEventListener(ev, mouse.mousewheel));
    const mc = MouseConstraint.create(engine, { mouse, constraint: { stiffness: 0.2, render: { visible: false } } });
    Composite.add(engine.world, mc);

    let downAt = null;
    chipsBox.addEventListener('mousedown', (e) => { downAt = { x: e.clientX, y: e.clientY }; dragDistance = 0; });
    window.addEventListener('mousemove', (e) => { if (downAt) dragDistance = Math.hypot(e.clientX - downAt.x, e.clientY - downAt.y); });
    window.addEventListener('mouseup', () => { downAt = null; setTimeout(() => { dragDistance = 0; }, 0); });

    Events.on(engine, 'afterUpdate', () => {
      pairs.forEach(({ chip, body, w, h }) => {
        chip.style.transform = `translate(${body.position.x - w / 2}px, ${body.position.y - h / 2}px) rotate(${body.angle}rad)`;
      });
    });
    // Park the chips above the box until it scrolls into view.
    pairs.forEach(({ chip, w, h }) => { chip.style.transform = `translate(${W / 2 - w / 2}px, ${-h * 2}px)`; });

    let started = false;
    const runner = Runner.create();
    const io = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting && !started) {
        started = true;
        Composite.add(engine.world, pairs.map((p) => p.body));
        Runner.run(runner, engine);
      }
    }, { threshold: 0.4 });
    io.observe(chipsBox);
  }

  /* Form (preview only, not connected yet) */
  const form = document.querySelector('.form');
  const status = form.querySelector('.form-status');
  form.addEventListener('input', (e) => e.target.removeAttribute('aria-invalid'));
  form.addEventListener('submit', (e) => {
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
    status.textContent = 'Thanks! This is a preview, so the form isn\'t connected yet.';
  });
})();
