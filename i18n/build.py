#!/usr/bin/env python3
"""Build the Spanish (site/es/) and Czech (site/cs/) pages from the English ones.

The English pages (site/index.html, site/privacy.html) are the source of truth.
Each translation below is an exact English snippet -> its Spanish and Czech
versions. If an English snippet is not found (because the English page changed),
the script stops and says which one, so nothing silently stays in English.

Run from anywhere:  python3 candadigitals/i18n/build.py
Then check the pages and commit site/es/ and site/cs/ together with the change.
Spanish should be checked by a native speaker before big changes (we promise
that to clients too).
"""

from pathlib import Path
import re
import sys

SITE = Path(__file__).resolve().parent.parent / "site"
LANGS = ("es", "cs")

# ---------------------------------------------------------------- index.html
# (english, spanish, czech)
INDEX = [
    # <head>
    ('<title>C&amp;A Digitals | Websites for small businesses</title>',
     '<title>C&amp;A Digitals | Sitios web para pequeñas empresas</title>',
     '<title>C&amp;A Digitals | Weby pro malé firmy</title>'),
    ('content="C&amp;A Digitals is a two-person web studio. We design, build and look after websites for small businesses across the US: Google profiles, reviews, bookings, other languages and monthly care."',
     'content="C&amp;A Digitals es un estudio web de dos personas. Diseñamos, creamos y cuidamos sitios web para pequeñas empresas en EE. UU.: perfiles de Google, reseñas, reservas, otros idiomas y mantenimiento mensual."',
     'content="C&amp;A Digitals je webové studio dvou lidí. Navrhujeme, stavíme a spravujeme weby pro malé firmy: profily na Googlu, recenze, rezervace, další jazyky a měsíční péče."'),
    ('<meta property="og:title" content="C&amp;A Digitals | Websites for small businesses">',
     '<meta property="og:title" content="C&amp;A Digitals | Sitios web para pequeñas empresas">',
     '<meta property="og:title" content="C&amp;A Digitals | Weby pro malé firmy">'),
    ('content="Chris and Adam, a two-person web studio. We design, build and look after websites for small businesses across the US."',
     'content="Chris y Adam, un estudio web de dos personas. Diseñamos, creamos y cuidamos sitios web para pequeñas empresas en EE. UU."',
     'content="Chris a Adam, webové studio dvou lidí. Navrhujeme, stavíme a spravujeme weby pro malé firmy."'),
    ('<meta property="og:url" content="https://candadigitals.com/">',
     '<meta property="og:url" content="https://candadigitals.com/es/">',
     '<meta property="og:url" content="https://candadigitals.com/cs/">'),
    ('content="C&amp;A Digitals: Websites that bring you customers."',
     'content="C&amp;A Digitals: Sitios web que le traen clientes."',
     'content="C&amp;A Digitals: Weby, které vám přivedou zákazníky."'),
    ('<link rel="canonical" href="https://candadigitals.com/">',
     '<link rel="canonical" href="https://candadigitals.com/es/">',
     '<link rel="canonical" href="https://candadigitals.com/cs/">'),
    ('"inLanguage": "en",', '"inLanguage": "es",', '"inLanguage": "cs",'),
    ('"description": "A two-person web studio. We design, build and look after websites for small businesses across the US, fully remote.",',
     '"description": "Un estudio web de dos personas. Diseñamos, creamos y cuidamos sitios web para pequeñas empresas en EE. UU., totalmente a distancia.",',
     '"description": "Webové studio dvou lidí. Navrhujeme, stavíme a spravujeme weby pro malé firmy, celé na dálku.",'),

    # header and menu
    ('>Skip to content</a>', '>Saltar al contenido</a>', '>Přeskočit na obsah</a>'),
    ('aria-label="C&amp;A Digitals, back to top"', 'aria-label="C&amp;A Digitals, volver arriba"', 'aria-label="C&amp;A Digitals, zpět nahoru"'),
    ('<nav class="lang" aria-label="Language">', '<nav class="lang" aria-label="Idioma">', '<nav class="lang" aria-label="Jazyk">'),
    ('<span class="menu-open">menu.</span><span class="menu-close">close.</span>',
     '<span class="menu-open">menú.</span><span class="menu-close">cerrar.</span>',
     '<span class="menu-open">menu.</span><span class="menu-close">zavřít.</span>'),
    ('<nav class="menu" id="menu" aria-label="Main" hidden>', '<nav class="menu" id="menu" aria-label="Principal" hidden>', '<nav class="menu" id="menu" aria-label="Hlavní" hidden>'),
    ('<small>01</small>Work</a>', '<small>01</small>Trabajos</a>', '<small>01</small>Práce</a>'),
    ('<small>02</small>About</a>', '<small>02</small>Nosotros</a>', '<small>02</small>O nás</a>'),
    ('<small>03</small>Services</a>', '<small>03</small>Servicios</a>', '<small>03</small>Služby</a>'),
    ('<small>04</small>Packages</a>', '<small>04</small>Paquetes</a>', '<small>04</small>Balíčky</a>'),
    ('<small>05</small>How we work</a>', '<small>05</small>Cómo trabajamos</a>', '<small>05</small>Jak pracujeme</a>'),
    ('<small>06</small>Contact</a>', '<small>06</small>Contacto</a>', '<small>06</small>Kontakt</a>'),

    # hero
    ('''    <h1 class="hero-title" aria-label="Websites that bring you customers.">
      <span class="line"><span class="word">Websites</span></span>
      <span class="line"><span class="word">that</span> <span class="word">bring</span></span>
      <span class="line"><span class="word">you</span> <span class="word accent">customers.</span></span>
    </h1>''',
     '''    <h1 class="hero-title" aria-label="Sitios web que le traen clientes.">
      <span class="line"><span class="word">Sitios</span> <span class="word">web</span></span>
      <span class="line"><span class="word">que</span> <span class="word">le</span> <span class="word">traen</span></span>
      <span class="line"><span class="word accent">clientes.</span></span>
    </h1>''',
     '''    <h1 class="hero-title" aria-label="Weby, které vám přivedou zákazníky.">
      <span class="line"><span class="word">Weby,</span> <span class="word">které</span></span>
      <span class="line"><span class="word">vám</span> <span class="word">přivedou</span></span>
      <span class="line"><span class="word accent">zákazníky.</span></span>
    </h1>'''),
    ('A two-person web studio for small businesses. We design, build and look after your website, and help you get found on Google, collect reviews and take bookings.',
     'Un estudio web de dos personas para pequeñas empresas. Diseñamos, creamos y cuidamos su sitio web, y le ayudamos a aparecer en Google, conseguir reseñas y recibir reservas.',
     'Webové studio dvou lidí pro malé firmy. Navrhneme, postavíme a spravujeme váš web a pomůžeme vám být vidět na Googlu, sbírat recenze a přijímat rezervace.'),
    ('<span>Book a free call</span>', '<span>Agende una llamada gratis</span>', '<span>Domluvit hovor zdarma</span>'),
    ('<span>See our work</span>', '<span>Ver nuestro trabajo</span>', '<span>Ukázky práce</span>'),
    ('<dt>Our desk</dt>\n          <dd><span class="clock-place">Florida, US</span>',
     '<dt>Nuestra oficina</dt>\n          <dd><span class="clock-place">Florida, EE. UU.</span>',
     '<dt>Pracujeme z</dt>\n          <dd><span class="clock-place">Florida, USA</span>'),
    ('<dt>Our desk</dt>\n          <dd><span class="clock-place">Prague, CZ</span>',
     '<dt>Nuestra oficina</dt>\n          <dd><span class="clock-place">Praga, CZ</span>',
     '<dt>Pracujeme z</dt>\n          <dd><span class="clock-place">Praha, CZ</span>'),
    ('<dt>Say hello</dt>', '<dt>Escríbanos</dt>', '<dt>Napište nám</dt>'),
    ('data-copy="candadigitals@gmail.com">Copy</button>', 'data-copy="candadigitals@gmail.com">Copiar</button>', 'data-copy="candadigitals@gmail.com">Kopírovat</button>'),

    # proof strip
    ('<p class="proof-label">Recently launched</p>', '<p class="proof-label">Lanzados recientemente</p>', '<p class="proof-label">Nedávno spuštěné</p>'),
    ("<span>Sarasota's #1 sailing charter</span>", '<span>El charter de vela n.º 1 de Sarasota</span>', '<span>Jachtařský charter č. 1 v Sarasotě</span>'),

    # marquee (the line appears twice; both get replaced)
    ('<span>Websites</span><span>Google profiles</span><span>Reviews</span><span>Bookings</span><span>Other languages</span><span>Accessibility</span><span>Monthly care</span>',
     '<span>Sitios web</span><span>Perfiles de Google</span><span>Reseñas</span><span>Reservas</span><span>Otros idiomas</span><span>Accesibilidad</span><span>Mantenimiento mensual</span>',
     '<span>Weby</span><span>Profily na Googlu</span><span>Recenze</span><span>Rezervace</span><span>Další jazyky</span><span>Přístupnost</span><span>Měsíční péče</span>'),

    # intro
    ("Most small businesses don't need a fancy agency. They need a site that loads fast, looks great on a phone, shows up on Google and makes it easy to call, book or pay. You send us what you have, we do the rest, and we stay around after launch.",
     'La mayoría de las pequeñas empresas no necesitan una agencia sofisticada. Necesitan un sitio que cargue rápido, se vea bien en el teléfono, aparezca en Google y facilite llamar, reservar o pagar. Usted nos envía lo que tiene, nosotros hacemos el resto y seguimos a su lado después del lanzamiento.',
     'Většina malých firem nepotřebuje drahou agenturu. Potřebuje web, který se rychle načte, dobře vypadá v telefonu, je vidět na Googlu a usnadní zavolat, objednat se nebo zaplatit. Vy nám pošlete, co máte, my uděláme zbytek a zůstaneme s vámi i po spuštění.'),

    # work
    ('<h2 class="section-title">Work</h2>', '<h2 class="section-title">Trabajos</h2>', '<h2 class="section-title">Práce</h2>'),
    ('Our latest launch. Yours could be next.', 'Nuestro último lanzamiento. El suyo podría ser el siguiente.', 'Náš nejnovější web. Ten váš může být další.'),
    ('Sailing charter · Sarasota, FL', 'Charter de vela · Sarasota, FL', 'Jachtařský charter · Sarasota, Florida'),
    ('alt="Homepage of Key Sailing Sarasota: a sailboat at sunset"',
     'alt="Página principal de Key Sailing Sarasota: un velero al atardecer"',
     'alt="Úvodní stránka Key Sailing Sarasota: plachetnice při západu slunce"'),
    ('<span class="work-name">Your business</span>', '<span class="work-name">Su empresa</span>', '<span class="work-name">Vaše firma</span>'),
    ('<span class="work-tag">Could be next</span>', '<span class="work-tag">Podría ser la siguiente</span>', '<span class="work-tag">Může být další</span>'),

    # about
    ('<h2 class="section-title">About</h2>', '<h2 class="section-title">Nosotros</h2>', '<h2 class="section-title">O nás</h2>'),
    ('Two people, two time zones, one inbox.', 'Dos personas, dos husos horarios, un solo buzón.', 'Dva lidé, dvě časová pásma, jedna schránka.'),
    ("No account managers, no handoffs, no junior team you never meet. We're two friends who do everything together: we talk to you, design and build your site, and look after it long after launch.",
     'Sin gerentes de cuenta, sin intermediarios, sin un equipo junior que nunca conoce. Somos dos amigos que lo hacemos todo juntos: hablamos con usted, diseñamos y creamos su sitio, y lo cuidamos mucho después del lanzamiento.',
     'Žádní account manažeři, žádné předávání, žádný tým juniorů, které nikdy neuvidíte. Jsme dva kamarádi a všechno děláme spolu: mluvíme s vámi, navrhneme a postavíme váš web a staráme se o něj i dlouho po spuštění.'),
    ('<p class="person-role">Co-founder</p>\n        <p>Chris is on your time zone, so a call during your business day is easy to fit in. He\'s part of every project from the first call to launch and beyond.</p>',
     '<p class="person-role">Cofundador</p>\n        <p>Chris está en su misma zona horaria, así que es fácil encontrar un momento para hablar durante su jornada. Participa en cada proyecto desde la primera llamada hasta el lanzamiento y después.</p>',
     '<p class="person-role">Spoluzakladatel</p>\n        <p>Chris žije na Floridě, takže s americkými klienty se snadno domluví v jejich pracovní době. Je u každého projektu od prvního hovoru až po spuštění a dál.</p>'),
    ('<p class="person-place">Prague, Czech Republic</p>', '<p class="person-place">Praga, República Checa</p>', '<p class="person-place">Praha, Česko</p>'),
    ('<p class="person-role">Co-founder</p>\n        <p>Adam is six hours ahead of Florida, so work on your site keeps moving while you sleep. He\'s part of every project from the first call to launch and beyond.</p>',
     '<p class="person-role">Cofundador</p>\n        <p>Adam va seis horas por delante de Florida, así que el trabajo en su sitio avanza mientras usted duerme. Participa en cada proyecto desde la primera llamada hasta el lanzamiento y después.</p>',
     '<p class="person-role">Spoluzakladatel</p>\n        <p>Adam je v Praze, takže je vám po ruce v českém čase. Je u každého projektu od prvního hovoru až po spuštění a dál.</p>'),
    ("Together we rebuilt Key Sailing Sarasota's website, including a Spanish version and a simple editor the owner uses to change texts and photos herself.",
     'Juntos rehicimos el sitio de Key Sailing Sarasota, con una versión en español y un editor sencillo con el que la dueña cambia textos y fotos ella misma.',
     'Společně jsme předělali web Key Sailing Sarasota, včetně španělské verze a jednoduchého editoru, ve kterém si majitelka sama mění texty a fotky.'),
    ('<span>01</span>Real, hand-built sites, not drag-and-drop templates', '<span>01</span>Sitios hechos a mano de verdad, no plantillas de arrastrar y soltar', '<span>01</span>Opravdu ručně stavěné weby, žádné šablony z klikátka'),
    ('<span>02</span>Fast on every phone', '<span>02</span>Rápidos en cualquier teléfono', '<span>02</span>Rychlé v každém telefonu'),
    ('<span>03</span>You own everything: domain, accounts, content', '<span>03</span>Todo es suyo: dominio, cuentas y contenido', '<span>03</span>Všechno patří vám: doména, účty i obsah'),
    ('<span>04</span>A reply within one business day', '<span>04</span>Respuesta en un día hábil', '<span>04</span>Odpověď do jednoho pracovního dne'),

    # services
    ('<h2 class="section-title">Services</h2>', '<h2 class="section-title">Servicios</h2>', '<h2 class="section-title">Služby</h2>'),
    ('Everything is done remotely. You send the photos, texts and logins, we turn them into something that works.',
     'Todo se hace a distancia. Usted nos envía fotos, textos y accesos, y nosotros los convertimos en algo que funciona.',
     'Všechno řešíme na dálku. Vy pošlete fotky, texty a přístupy, my z nich uděláme něco, co funguje.'),
    ('<span class="acc-title">Website design &amp; build</span>', '<span class="acc-title">Diseño y desarrollo web</span>', '<span class="acc-title">Návrh a stavba webu</span>'),
    ('A custom site designed around your business, fast on any phone and launched on your own domain. Moving from an old site? We keep your Google rankings, old links and email working.',
     'Un sitio a medida pensado para su negocio, rápido en cualquier teléfono y publicado en su propio dominio. ¿Viene de un sitio antiguo? Mantenemos su posición en Google, los enlaces antiguos y su correo funcionando.',
     'Web na míru vaší firmě, rychlý v každém telefonu a spuštěný na vaší vlastní doméně. Přecházíte ze starého webu? Zachováme vám pozice v Googlu, staré odkazy i e-mail.'),
    ('<span class="acc-title">Google profile &amp; maps</span>', '<span class="acc-title">Perfil de Google y mapas</span>', '<span class="acc-title">Profil na Googlu a mapy</span>'),
    ('We set up and polish your Google Business Profile, plus Apple Maps, Bing, Yelp and TripAdvisor, with the same details everywhere. You verify the profile with Google, we walk you through it, then we handle the rest as your manager.',
     'Configuramos y pulimos su Perfil de Empresa de Google, además de Apple Maps, Bing, Yelp y TripAdvisor, con los mismos datos en todas partes. Usted verifica el perfil con Google (le guiamos paso a paso) y nosotros nos encargamos del resto como administradores.',
     'Založíme a vyladíme vám Firemní profil Google a k tomu Apple Mapy, Bing, Yelp a TripAdvisor, všude se stejnými údaji. Profil u Googlu ověříte vy (provedeme vás tím) a zbytek už zařídíme jako správci.'),
    ('<span class="acc-title">Reviews</span>', '<span class="acc-title">Reseñas</span>', '<span class="acc-title">Recenze</span>'),
    ('A short review link and QR cards that make it easy for happy customers to leave a Google review. We design print-ready cards and can ship them to you through an online print shop.',
     'Un enlace corto y tarjetas con código QR para que sus clientes satisfechos dejen fácilmente una reseña en Google. Diseñamos tarjetas listas para imprimir y podemos enviárselas a través de una imprenta en línea.',
     'Krátký odkaz a kartičky s QR kódem, aby spokojení zákazníci snadno napsali recenzi na Googlu. Navrhneme kartičky připravené k tisku a můžeme vám je poslat přes online tiskárnu.'),
    ('<span class="acc-title">Bookings, payments &amp; gift cards</span>', '<span class="acc-title">Reservas, pagos y tarjetas de regalo</span>', '<span class="acc-title">Rezervace, platby a dárkové poukazy</span>'),
    ('Call, text and WhatsApp buttons, contact forms that stop spam, online bookings, Stripe payments and gift cards. The accounts stay in your name, we connect them to your site.',
     'Botones para llamar, enviar mensajes y WhatsApp, formularios de contacto sin spam, reservas en línea, pagos con Stripe y tarjetas de regalo. Las cuentas quedan a su nombre; nosotros las conectamos a su sitio.',
     'Tlačítka pro volání, SMS a WhatsApp, kontaktní formuláře bez spamu, online rezervace, platby přes Stripe a dárkové poukazy. Účty zůstávají na vaše jméno, my je jen napojíme na web.'),
    ('<span class="acc-title">Other language versions</span>', '<span class="acc-title">Versiones en otros idiomas</span>', '<span class="acc-title">Další jazykové verze</span>'),
    ('Your site in the languages your customers speak: Spanish, Portuguese, French and more. We translate, and a native speaker always checks it before it goes live.',
     'Su sitio en los idiomas de sus clientes: inglés, portugués, francés y más. Nosotros traducimos y un hablante nativo siempre lo revisa antes de publicarlo.',
     'Váš web v jazycích vašich zákazníků: angličtina, němčina, španělština a další. Přeložíme ho my a před spuštěním ho vždy zkontroluje rodilý mluvčí.'),
    ('<span class="acc-title">Accessibility (ADA)</span>', '<span class="acc-title">Accesibilidad (ADA)</span>', '<span class="acc-title">Přístupnost</span>'),
    ('We check and fix your site so people using screen readers, keyboards or large text can use it too. Good for your customers, and it lowers the risk of ADA complaints.',
     'Revisamos y corregimos su sitio para que también puedan usarlo personas con lectores de pantalla, teclado o texto grande. Es bueno para sus clientes y reduce el riesgo de reclamaciones por la ADA.',
     'Zkontrolujeme a opravíme web tak, aby ho mohli používat i lidé se čtečkou obrazovky, klávesnicí nebo zvětšeným písmem. Pomůže to vašim zákazníkům i tomu, jak web hodnotí Google.'),
    ('<span class="acc-title">Monthly care</span>', '<span class="acc-title">Mantenimiento mensual</span>', '<span class="acc-title">Měsíční péče</span>'),
    ('Hosting, backups, small edits whenever you need them, and a short monthly report: how many people visited, called, texted or booked.',
     'Alojamiento, copias de seguridad, pequeños cambios cuando los necesite y un breve informe mensual: cuántas personas visitaron, llamaron, escribieron o reservaron.',
     'Hosting, zálohy, drobné úpravy, kdykoli je potřebujete, a krátký měsíční přehled: kolik lidí web navštívilo, zavolalo, napsalo nebo se objednalo.'),
    ('<h3 class="extras-title">Also on the menu</h3>', '<h3 class="extras-title">También ofrecemos</h3>', '<h3 class="extras-title">Dále nabízíme</h3>'),
    ('<span>08</span>Edit it yourself: change texts and photos without us', '<span>08</span>Edítelo usted mismo: cambie textos y fotos sin depender de nosotros', '<span>08</span>Úpravy svépomocí: texty a fotky si změníte sami'),
    ('<span>09</span>AI search visibility: get recommended by ChatGPT and friends', '<span>09</span>Visibilidad en búsquedas con IA: que ChatGPT y compañía le recomienden', '<span>09</span>Viditelnost v AI vyhledávání: ať vás doporučí ChatGPT a spol.'),
    ('<span>10</span>Photo &amp; video polish: we make your phone photos shine', '<span>10</span>Retoque de fotos y video: hacemos brillar las fotos de su teléfono', '<span>10</span>Úprava fotek a videa: z fotek z telefonu uděláme parádu'),
    ('<span>11</span>Logo &amp; brand basics: logo, colors, business cards', '<span>11</span>Logo e identidad básica: logo, colores, tarjetas de presentación', '<span>11</span>Logo a základ značky: logo, barvy, vizitky'),
    ('<span>12</span>Domain &amp; business email: always in your name', '<span>12</span>Dominio y correo profesional: siempre a su nombre', '<span>12</span>Doména a firemní e-mail: vždy na vaše jméno'),

    # packages
    ('<h2 class="section-title">Packages</h2>', '<h2 class="section-title">Paquetes</h2>', '<h2 class="section-title">Balíčky</h2>'),
    ("Three simple starting points. Every business is different, so we'll tailor it on a call.",
     'Tres puntos de partida sencillos. Cada negocio es diferente, así que lo ajustamos en una llamada.',
     'Tři jednoduché výchozí body. Každá firma je jiná, takže to doladíme v hovoru.'),
    ('<h3>Starter</h3>', '<h3>Básico</h3>', '<h3>Start</h3>'),
    ('<p class="pkg-sub">Get online, get found.</p>', '<p class="pkg-sub">Esté en línea y que le encuentren.</p>', '<p class="pkg-sub">Buďte online a k nalezení.</p>'),
    ('<li>Custom website</li>', '<li>Sitio web a medida</li>', '<li>Web na míru</li>'),
    ('<li>Google Business Profile</li>', '<li>Perfil de Empresa de Google</li>', '<li>Firemní profil Google</li>'),
    ('<li>Call, text and contact form</li>', '<li>Llamadas, mensajes y formulario</li>', '<li>Volání, SMS a kontaktní formulář</li>'),
    ('<h3>Growth</h3>', '<h3>Crecimiento</h3>', '<h3>Růst</h3>'),
    ('<p class="pkg-sub">Everything in Starter, plus:</p>', '<p class="pkg-sub">Todo lo de Básico, más:</p>', '<p class="pkg-sub">Vše ze Startu a navíc:</p>'),
    ('<li>Reviews kit with QR cards</li>', '<li>Kit de reseñas con tarjetas QR</li>', '<li>Sada pro recenze s QR kartičkami</li>'),
    ('<li>Bookings and payments</li>', '<li>Reservas y pagos</li>', '<li>Rezervace a platby</li>'),
    ('<li>One extra language</li>', '<li>Un idioma adicional</li>', '<li>Jeden jazyk navíc</li>'),
    ('<h3>Care</h3>', '<h3>Cuidado</h3>', '<h3>Péče</h3>'),
    ('<p class="pkg-sub">Add to either package.</p>', '<p class="pkg-sub">Se añade a cualquier paquete.</p>', '<p class="pkg-sub">Dá se přidat k oběma balíčkům.</p>'),
    ('<li>Hosting and backups</li>', '<li>Alojamiento y copias de seguridad</li>', '<li>Hosting a zálohy</li>'),
    ('<li>Small edits on request</li>', '<li>Pequeños cambios cuando los pida</li>', '<li>Drobné úpravy na požádání</li>'),
    ('<li>Monthly report</li>', '<li>Informe mensual</li>', '<li>Měsíční přehled</li>'),
    ('You own everything: domain, accounts and content stay in your name.',
     'Todo es suyo: dominio, cuentas y contenido quedan a su nombre.',
     'Všechno patří vám: doména, účty i obsah zůstávají na vaše jméno.'),

    # process
    ('<h2 class="section-title">How we work</h2>', '<h2 class="section-title">Cómo trabajamos</h2>', '<h2 class="section-title">Jak pracujeme</h2>'),
    ('Prague is six hours ahead of Florida, so your site gets built while you sleep.',
     'Praga va seis horas por delante de Florida: su sitio avanza mientras usted duerme.',
     'Jsme dva na dvou kontinentech, takže se na vašem webu pracuje skoro nepřetržitě.'),
    ('<h3>Intro call</h3><p>A 20-minute phone call about your business and what you need.</p>',
     '<h3>Llamada inicial</h3><p>Una llamada de 20 minutos sobre su negocio y lo que necesita.</p>',
     '<h3>Úvodní hovor</h3><p>Dvacetiminutový telefonát o vaší firmě a o tom, co potřebujete.</p>'),
    ('<h3>Send us your stuff</h3><p>A short questionnaire and a shared folder for texts, photos, logo and logins.</p>',
     '<h3>Envíenos su material</h3><p>Un breve cuestionario y una carpeta compartida para textos, fotos, logo y accesos.</p>',
     '<h3>Pošlete nám podklady</h3><p>Krátký dotazník a sdílená složka na texty, fotky, logo a přístupy.</p>'),
    ('<h3>We build</h3><p>You get a private preview link to click through on your phone.</p>',
     '<h3>Construimos</h3><p>Recibe un enlace privado para revisarlo en su teléfono.</p>',
     '<h3>Stavíme</h3><p>Dostanete soukromý odkaz na náhled, který si proklikáte v telefonu.</p>'),
    ('<h3>Feedback</h3><p>Two or three rounds of changes by email or on a call.</p>',
     '<h3>Comentarios</h3><p>Dos o tres rondas de cambios por correo o por teléfono.</p>',
     '<h3>Připomínky</h3><p>Dvě až tři kola úprav e-mailem nebo po telefonu.</p>'),
    ('<h3>Launch &amp; care</h3><p>We go live, record a short how-to video and keep an eye on things.</p>',
     '<h3>Lanzamiento y cuidado</h3><p>Publicamos el sitio, grabamos un video corto de uso y seguimos pendientes.</p>',
     '<h3>Spuštění a péče</h3><p>Web spustíme, natočíme krátké video, jak ho používat, a dál na něj dohlížíme.</p>'),

    # contact
    ('<h2 class="contact-title">I need<span aria-hidden="true">…</span></h2>',
     '<h2 class="contact-title">Necesito<span aria-hidden="true">…</span></h2>',
     '<h2 class="contact-title">Potřebuji<span aria-hidden="true">…</span></h2>'),
    ('Pick what you need (drag them around if you like), then tell us about your business.',
     'Elija lo que necesita (puede arrastrar las etiquetas) y cuéntenos sobre su negocio.',
     'Vyberte, co potřebujete (štítky můžete i přetahovat), a napište nám něco o své firmě.'),
    ('aria-label="What do you need?"', 'aria-label="¿Qué necesita?"', 'aria-label="Co potřebujete?"'),
    ('aria-pressed="false">a website</button>', 'aria-pressed="false">un sitio web</button>', 'aria-pressed="false">web</button>'),
    ('aria-pressed="false">a new website</button>', 'aria-pressed="false">un sitio nuevo</button>', 'aria-pressed="false">nový web</button>'),
    ('aria-pressed="false">Google profile</button>', 'aria-pressed="false">perfil de Google</button>', 'aria-pressed="false">profil na Googlu</button>'),
    ('aria-pressed="false">more reviews</button>', 'aria-pressed="false">más reseñas</button>', 'aria-pressed="false">víc recenzí</button>'),
    ('aria-pressed="false">online bookings</button>', 'aria-pressed="false">reservas en línea</button>', 'aria-pressed="false">online rezervace</button>'),
    ('aria-pressed="false">payments</button>', 'aria-pressed="false">pagos</button>', 'aria-pressed="false">platby</button>'),
    ('aria-pressed="false">another language</button>', 'aria-pressed="false">otro idioma</button>', 'aria-pressed="false">další jazyk</button>'),
    ('aria-pressed="false">accessibility</button>', 'aria-pressed="false">accesibilidad</button>', 'aria-pressed="false">přístupnost</button>'),
    ('aria-pressed="false">monthly care</button>', 'aria-pressed="false">mantenimiento</button>', 'aria-pressed="false">měsíční péče</button>'),
    ('aria-pressed="false">a logo</button>', 'aria-pressed="false">un logo</button>', 'aria-pressed="false">logo</button>'),
    ('<label for="f-name">Your name</label>', '<label for="f-name">Su nombre</label>', '<label for="f-name">Vaše jméno</label>'),
    ('<label for="f-biz">Business</label>', '<label for="f-biz">Empresa</label>', '<label for="f-biz">Firma</label>'),
    ('<label for="f-email">Email</label>', '<label for="f-email">Correo electrónico</label>', '<label for="f-email">E-mail</label>'),
    ('<label for="f-msg">Tell us a bit about it</label>', '<label for="f-msg">Cuéntenos un poco</label>', '<label for="f-msg">Napište nám pár slov</label>'),
    ('<input type="hidden" name="lang" value="en">', '<input type="hidden" name="lang" value="es">', '<input type="hidden" name="lang" value="cs">'),
    ('data-theme="dark"></div>', 'data-theme="dark" data-language="es"></div>', 'data-theme="dark" data-language="cs"></div>'),
    ('<span>Send</span>', '<span>Enviar</span>', '<span>Odeslat</span>'),
    ('We only use your details to reply to you. See our <a href="privacy.html">Privacy Policy</a>.',
     'Solo usamos sus datos para responderle. Consulte nuestra <a href="privacy.html">Política de privacidad</a>.',
     'Vaše údaje použijeme jen k odpovědi. Více v <a href="privacy.html">zásadách ochrany osobních údajů</a>.'),

    # footer
    ('<span>Websites for small businesses · Remote from Prague and Florida</span>',
     '<span>Sitios web para pequeñas empresas · Desde Praga y Florida</span>',
     '<span>Weby pro malé firmy · Z Prahy a Floridy</span>'),
    ('<a href="privacy.html">Privacy</a></span>', '<a href="privacy.html">Privacidad</a></span>', '<a href="privacy.html">Soukromí</a></span>'),
    ('<span>Back to top ↑</span>', '<span>Volver arriba ↑</span>', '<span>Nahoru ↑</span>'),
]

# ---------------------------------------------------------------- privacy.html
PRIVACY_HEAD = [
    ('<title>Privacy Policy | C&amp;A Digitals</title>', '<title>Política de privacidad | C&amp;A Digitals</title>', '<title>Ochrana osobních údajů | C&amp;A Digitals</title>'),
    ('content="How C&amp;A Digitals handles the personal data you send us through this website."',
     'content="Cómo trata C&amp;A Digitals los datos personales que nos envía a través de este sitio web."',
     'content="Jak C&amp;A Digitals zachází s osobními údaji, které nám pošlete přes tento web."'),
    ('<link rel="canonical" href="https://candadigitals.com/privacy">',
     '<link rel="canonical" href="https://candadigitals.com/es/privacy">',
     '<link rel="canonical" href="https://candadigitals.com/cs/privacy">'),
    ('>Skip to content</a>', '>Saltar al contenido</a>', '>Přeskočit na obsah</a>'),
    ('aria-label="C&amp;A Digitals, home"', 'aria-label="C&amp;A Digitals, inicio"', 'aria-label="C&amp;A Digitals, úvod"'),
    ('<a class="header-link" href="./">Back to home</a>', '<a class="header-link" href="./">Volver al inicio</a>', '<a class="header-link" href="./">Zpět na úvod</a>'),
]

PRIVACY_MAIN = {
    "es": '''<main id="main" class="legal">
  <h1 class="legal-title">Política de privacidad</h1>
  <p class="legal-updated">Última actualización: 22 de octubre de 2026</p>

  <section>
    <h2>Quiénes somos</h2>
    <p>C&amp;A Digitals es un estudio web de dos personas dirigido por Adam Kříž y Christian Robert Nielsen. Somos los responsables de los datos personales descritos aquí.</p>
    <p>Contacto: <a href="mailto:candadigitals@gmail.com">candadigitals@gmail.com</a><br>Palm Coast, Florida, EE. UU.</p>
  </section>

  <section>
    <h2>En resumen</h2>
    <ul>
      <li>Solo recopilamos lo que nos envía a través del formulario de contacto y lo usamos únicamente para responderle.</li>
      <li>Este sitio web no usa cookies, publicidad ni rastreo.</li>
      <li>Nunca vendemos sus datos.</li>
    </ul>
  </section>

  <section>
    <h2>Qué recopilamos y por qué</h2>
    <p><strong>Formulario de contacto.</strong> Cuando envía el formulario, recibimos su nombre, su correo electrónico, el nombre de su empresa y su mensaje si los añade, y los servicios que eligió. Los usamos para responder a su consulta y, si lo desea, preparar una propuesta. La base legal es la aplicación de medidas precontractuales a petición suya (RGPD, art.&nbsp;6(1)(b)).</p>
    <p><strong>Datos técnicos.</strong> Como cualquier sitio web, nuestro proveedor de alojamiento procesa su dirección IP y datos básicos del navegador para mostrar las páginas y mantener el sitio seguro. El formulario usa Cloudflare Turnstile para distinguir a las personas de los bots de spam. La base legal es nuestro interés legítimo en un sitio web seguro (RGPD, art.&nbsp;6(1)(f)).</p>
    <p><strong>Estadísticas de visitas.</strong> Podemos usar Cloudflare Web Analytics, que cuenta las visitas de forma agregada, sin cookies y sin identificarle.</p>
  </section>

  <section>
    <h2>Quién nos ayuda</h2>
    <p>Usamos algunos proveedores que procesan datos en nuestro nombre:</p>
    <ul>
      <li><strong>Cloudflare, Inc.</strong>: alojamiento web, protección contra spam (Turnstile) y estadísticas de visitas.</li>
      <li><strong>Resend, Inc.</strong>: entrega el mensaje del formulario a nuestro buzón.</li>
      <li><strong>Google LLC</strong>: nuestro buzón de correo (Gmail).</li>
    </ul>
    <p>Estas empresas tienen su sede en Estados Unidos. Cuando se aplica el RGPD, las transferencias se basan en el Marco de Privacidad de Datos UE-EE.&nbsp;UU. o en las cláusulas contractuales tipo de la Comisión Europea.</p>
  </section>

  <section>
    <h2>Cuánto tiempo los conservamos</h2>
    <p>Conservamos los mensajes del formulario y nuestra conversación por correo mientras estemos en contacto o trabajando juntos y, después, hasta 2 años, salvo que la ley nos obligue a conservarlos más tiempo (por ejemplo, las facturas). Los registros técnicos de nuestro proveedor de alojamiento se guardan solo durante poco tiempo.</p>
  </section>

  <section>
    <h2>Sus derechos</h2>
    <p>Puede pedirnos en cualquier momento ver, corregir o eliminar sus datos, limitar su uso, oponerse a su uso o recibirlos en un formato portátil. Solo tiene que escribir a <a href="mailto:candadigitals@gmail.com">candadigitals@gmail.com</a>.</p>
    <p>Si está en la UE, también puede presentar una reclamación ante una autoridad de protección de datos. La nuestra es la Oficina Checa de Protección de Datos Personales (<a href="https://uoou.gov.cz/en" rel="noopener">uoou.gov.cz</a>).</p>
    <p>Si está en California o en otro estado de EE.&nbsp;UU. con una ley de privacidad, tiene derechos similares a saber, corregir y eliminar su información. No vendemos ni compartimos información personal con fines publicitarios.</p>
  </section>

  <section>
    <h2>Menores</h2>
    <p>Este sitio web está dirigido a empresas y no a menores de 16 años.</p>
  </section>

  <section>
    <h2>Cambios</h2>
    <p>Si cambiamos la forma en que tratamos sus datos, actualizaremos esta página y la fecha de arriba. La versión en inglés es la versión de referencia.</p>
  </section>
</main>''',
    "cs": '''<main id="main" class="legal">
  <h1 class="legal-title">Ochrana osobních údajů</h1>
  <p class="legal-updated">Poslední aktualizace: 22. října 2026</p>

  <section>
    <h2>Kdo jsme</h2>
    <p>C&amp;A Digitals je webové studio dvou lidí, které vedou Adam Kříž a Christian Robert Nielsen. Jsme správci osobních údajů popsaných na této stránce.</p>
    <p>Kontakt: <a href="mailto:candadigitals@gmail.com">candadigitals@gmail.com</a><br>Palm Coast, Florida, USA</p>
  </section>

  <section>
    <h2>Ve zkratce</h2>
    <ul>
      <li>Získáváme jen to, co nám pošlete přes kontaktní formulář, a používáme to jen k tomu, abychom vám odpověděli.</li>
      <li>Tento web nepoužívá cookies, reklamu ani sledování.</li>
      <li>Vaše údaje nikdy neprodáváme.</li>
    </ul>
  </section>

  <section>
    <h2>Co zpracováváme a proč</h2>
    <p><strong>Kontaktní formulář.</strong> Když formulář odešlete, dostaneme vaše jméno, e-mail, název firmy a zprávu (pokud je vyplníte) a služby, které jste vybrali. Použijeme je, abychom odpověděli na váš dotaz a případně připravili nabídku. Právním základem je jednání o smlouvě na vaši žádost (čl.&nbsp;6 odst.&nbsp;1 písm.&nbsp;b GDPR).</p>
    <p><strong>Technické údaje.</strong> Jako každý web zpracovává náš poskytovatel hostingu vaši IP adresu a základní údaje o prohlížeči, aby mohl stránky zobrazit a udržet web v bezpečí. Formulář používá Cloudflare Turnstile, který odliší lidi od spamových robotů. Právním základem je náš oprávněný zájem na bezpečném webu (čl.&nbsp;6 odst.&nbsp;1 písm.&nbsp;f GDPR).</p>
    <p><strong>Statistiky návštěvnosti.</strong> Můžeme používat Cloudflare Web Analytics, které počítá návštěvy souhrnně, bez cookies a bez toho, aby vás identifikovalo.</p>
  </section>

  <section>
    <h2>Kdo nám pomáhá</h2>
    <p>Používáme několik dodavatelů, kteří pro nás údaje zpracovávají:</p>
    <ul>
      <li><strong>Cloudflare, Inc.</strong>: hosting webu, ochrana proti spamu (Turnstile) a statistiky návštěvnosti.</li>
      <li><strong>Resend, Inc.</strong>: doručuje zprávu z formuláře do naší schránky.</li>
      <li><strong>Google LLC</strong>: naše e-mailová schránka (Gmail).</li>
    </ul>
    <p>Tyto firmy sídlí ve Spojených státech. Kde se uplatní GDPR, předávání údajů se opírá o rámec EU–USA pro ochranu osobních údajů (Data Privacy Framework) nebo o standardní smluvní doložky Evropské komise.</p>
  </section>

  <section>
    <h2>Jak dlouho údaje uchováváme</h2>
    <p>Zprávy z formuláře a naši e-mailovou komunikaci uchováváme po dobu, kdy spolu jednáme nebo spolupracujeme, a pak nejvýše 2 roky, pokud nám zákon neukládá uchovávat je déle (například faktury). Technické záznamy u poskytovatele hostingu se uchovávají jen krátce.</p>
  </section>

  <section>
    <h2>Vaše práva</h2>
    <p>Kdykoli nás můžete požádat o přístup ke svým údajům, jejich opravu nebo výmaz, omezení zpracování, můžete vznést námitku nebo požádat o jejich předání v přenositelném formátu. Stačí napsat na <a href="mailto:candadigitals@gmail.com">candadigitals@gmail.com</a>.</p>
    <p>Máte také právo podat stížnost u Úřadu pro ochranu osobních údajů (<a href="https://uoou.gov.cz" rel="noopener">uoou.gov.cz</a>).</p>
  </section>

  <section>
    <h2>Děti</h2>
    <p>Tento web je určený firmám a není zaměřený na děti mladší 16 let.</p>
  </section>

  <section>
    <h2>Změny</h2>
    <p>Pokud změníme způsob, jak s údaji zacházíme, upravíme tuto stránku a datum nahoře. Rozhodující je anglická verze.</p>
  </section>
</main>''',
}

# Asset paths that need "../" in the subfolders (pages and privacy links stay relative).
ASSET_RE = re.compile(r'((?:href|src|data-img)=")((?:style\.css|js/|images/|brand/|fonts/)[^"]*")')


def localize(html, pairs, lang, name):
    idx = LANGS.index(lang) + 1
    for pair in pairs:
        en = pair[0]
        if en not in html:
            sys.exit(f"[{name}] English text not found, update i18n/build.py:\n  {en[:100]}")
        html = html.replace(en, pair[idx])
    return html


def common(html, lang):
    html = html.replace('<html lang="en">', f'<html lang="{lang}">', 1)
    html = ASSET_RE.sub(r'\1../\2', html)
    # Language switcher: mark this language as the current page.
    html = html.replace(' aria-current="page">EN</a>', '>EN</a>')
    code = lang.upper()
    html = html.replace(f'lang="{lang}">{code}</a>', f'lang="{lang}" aria-current="page">{code}</a>')
    return html


def main():
    index = (SITE / "index.html").read_text(encoding="utf-8")
    privacy = (SITE / "privacy.html").read_text(encoding="utf-8")
    main_en = re.search(r'<main id="main" class="legal">.*?</main>', privacy, re.S)
    if not main_en:
        sys.exit("[privacy] <main> block not found")
    for lang in LANGS:
        out = SITE / lang
        out.mkdir(exist_ok=True)
        page = common(localize(index, INDEX, lang, "index"), lang)
        (out / "index.html").write_text(page, encoding="utf-8")
        p = localize(privacy, PRIVACY_HEAD, lang, "privacy")
        p = p.replace(main_en.group(0), PRIVACY_MAIN[lang])
        p = common(p, lang)
        (out / "privacy.html").write_text(p, encoding="utf-8")
        print(f"wrote site/{lang}/index.html and site/{lang}/privacy.html")


if __name__ == "__main__":
    main()
