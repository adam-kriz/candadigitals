# candadigitals

Vlastní značka a budoucí web **C&A Digitals**: Adam (A) a jeho kamarád Chris (C)
dělají weby a další digitální služby pro malé firmy, **hlavně v USA** (Florida).
Web bude **anglicky**.

## Status

**Jen značka (20. 10. 2026)**: název a logo jsou uložené „prozatím“, můžou se ještě
změnit (Adam to ukazuje Chrisovi). Web se zatím nestaví; bude ve **stejném repu**
(tahle složka). Vlastní git, GitHub repo
[adam-kriz/candadigitals](https://github.com/adam-kriz/candadigitals) (založeno
20. 10. 2026, od téhož dne **veřejné**). Náhled: **https://adam-kriz.github.io/candadigitals/**
(GitHub Pages z větve `main`). Pushovat jen s Adamovým výslovným souhlasem.

## Název

**C&A Digitals** — C = Chris, A = Adam. Napsané celé stejně tenkým písmem
(bez tučného „C&A“).
- Doména **candadigitals.com** byla 20. 10. 2026 volná (nekoupená). Volné byly i
  cnadigitals.com; candadigital.com (bez s) je zabraná.
- Vědomá rizika: C&A je i evropský řetězec s oblečením (v USA není); „Digitals“ je
  neobvyklá angličtina. Adam to ví a jméno chce.
- Předtím zvažováno a opuštěno: CA DigitalWorks, CA Works, dva uzly, výloha aj.

## Logo („vrstvy“)

Souměrný znak: horní plný kosočtverec (šedý) + dvě vrstvy z čar pod ním.
Soubory v `brand/` (náhled všeho: `brand/index.html`):

| Soubor | Co to je |
|---|---|
| `logo-on-dark.svg` / `logo-on-light.svg` | znak + název vedle sebe |
| `mark-on-dark.svg` / `mark-on-light.svg` | jen znak, průhledné pozadí |
| `icon-dark.svg` / `icon-light.svg` | znak na zaobleném čtverci (favicon, profilovky) |

- Světlá verze = **barevně invertovaná tmavá** (přání Adama).
- Barvy: pozadí tmavé `#262624`, světlé (krémové) `#F5F4EE`; čáry a text = ta druhá
  z dvojice; horní vrstva vždy šedá `#888780`.
- Písmo názvu zatím nevybrané: v SVG je `text` s Hanken Grotesk / systémovým
  bezpatkovým písmem → před tiskem nebo finálním použitím převést na křivky.
- Claudův návrh (zatím nepřijatý): horní vrstvu udělat barevnou (teplá oranžová
  „západ slunce“ nebo tyrkysová „Gulf“) — víc osobnosti, méně podobné logu Buffer.

## Web — první verze (20. 10. 2026)

Jedna dlouhá stránka, anglicky, ve stylu **awakeagency.dev** (vzor, který Adam vybral):
tmavá, obří nadpisy verzálkami, hodně animací. Statický web bez build stepu.

| Soubor | Co to je |
|---|---|
| `site/` | **jen tahle složka jde na web** (Cloudflare Pages „build output“); `CLAUDE.md`, `functions/` a `wrangler.toml` zůstávají mimo |
| `site/index.html` | celá stránka: Hero → pás služeb → Intro → Work → Services → Packages → How we work → Contact „I need…“ → patička |
| `site/style.css` | vzhled; barvy jako proměnné v `:root` (stejné jako logo) |
| `site/js/main.js` | animace, interakce a odeslání formuláře |
| `site/images/og.jpg` | náhled odkazu (iMessage, WhatsApp, Messenger): screenshot úvodu 1200×630; v `<head>` jako `og:image` s absolutní adresou na github.io — při přesunu na vlastní doménu změnit |
| `site/images/work/` | screenshoty projektů v sekci Work: Aveo Engineering, Key Sailing Sarasota |

| `site/privacy.html` | Privacy Policy (GDPR + US); **obsahuje zástupné údaje** `[Chris's full name]`, `[Postal address]` (červeně) — doplnit před spuštěním |
| `site/404.html` | stránka „Lost a layer.“ (absolutní cesty `/…`) |
| `site/robots.txt`, `site/sitemap.xml`, `site/llms.txt` | pro vyhledávače a AI; JSON-LD (`ProfessionalService`) je v `<head>` index.html — u zakladatele „Chris“ doplnit celé jméno |
| `site/_headers` | bezpečnostní hlavičky + `noindex` pro náhledy na `*.pages.dev` |
| `functions/api/contact.js` | formulář → e-mail přes Resend, ochrana honeypot + Turnstile (převzato z Key Sailing) |
| `wrangler.toml` | nastavení Pages: výstup `site`, proměnné; `FORMS_LIVE = "false"` → vše jde na `TEST_TO` |

Knihovny z CDN: **GSAP 3.12.5 + ScrollTrigger** (animace při scrollu), **Lenis 1.1.13**
(plynulý scroll), **Matter.js 0.19.0** (padající štítky v kontaktu). Písmo Hanken Grotesk.

Animace: nadpis naskakuje po slovech; tři vrstvy loga v úvodu se při scrollu rozjedou
(Adamovi se to líbí, nechat) a natáčejí se za myší; intro text se při scrollu „rozsvěcuje“ po slovech; u projektů jede za
myší náhled; služby = rozbalovací seznam (otevřená jen jedna); čára „How we work“ se
kreslí při scrollu; štítky „I need…“ padají a jdou přetahovat (jen počítač s myší, na
mobilu obyčejná tlačítka; vlastní smyčka s pevným krokem 1/120 s, spaní těl proti chvění,
štítky padají „z neznáma“ až ~420 px nad rámečkem z náhodných míst, náhodně
nakloněné a postrčené; jakmile jsou všechny uvnitř (nejpozději po 4 s), zavře se strop, menší štítky, rámeček 340 px na
celou šířku (jako v první verzi), limit rychlosti hodu, tažení slyší celé okno, stěny se přepočítají při změně
velikosti; žádné poskakování — Adam nechce, aby štítky vylétávaly); magnetická tlačítka. Hodiny „Our desk“ Florida a Praha (bez počasí, Adam ho 20. 10. 2026 nechtěl). **Omezené animace v systému → klidná verze** bez
animací a plynulého scrollu (ověřeno).

Zatím **náhled**: `noindex`, e-mail `hello@candadigitals.com` je **jen zástupný**
(doména není koupená), formulář nic neposílá (jen hláška „preview“). Projekty v sekci Work (Adam 20. 10. 2026): 1. **Aveo Engineering**
(aveoengineering.com, dělal Chris), 2. **Key Sailing Sarasota** (siestakeysailing.com). Texty jsou Claudův návrh
— Adam a Chris je upraví. „Our desk“ = Florida a Praha (Adam 20. 10. 2026).

Rozmazání pod hlavičkou po scrollu = **jen 2 vrstvy** `backdrop-filter` (silná nahoře, slabá níž) +
slábnoucí tónování. Se 4 vrstvami se scroll trhal (změřeno 21. 10. 2026) — vrstvy nepřidávat.

Lokální náhled: konfigurace `candadigitals` v kořenovém `.claude/launch.json`
(Python `http.server`, port 8130, složka `candadigitals/site`) → http://localhost:8130.
Lokálně formulář ukáže „Sorry, that didn't send“ (Python server neumí funkci) — to je v pořádku.

## Nasazení na candadigitals.com (plán z 21. 10. 2026)

Rozhodnuto: firemní Gmail → účet Cloudflare → doména **candadigitals.com** přes Cloudflare
Registrar; hosting **Cloudflare Pages** (Adam povolil propojení s GitHubem); e-mail **zdarma**
přes Cloudflare Email Routing (přeposílání do Gmailu); Resend = existující účet (přidat doménu);
obsah webu zatím beze změny. Účty a platby dělá Adam sám, Claude dává návod.

Hotovo v kódu (21. 10. 2026, commitnuté, **nepushnuté**, protože přesun do `site/` vypne
náhled na github.io — pushnout až při propojení s Cloudflare Pages): přesun do `site/`,
formulář, Privacy Policy, 404, robots/sitemap/llms.txt/JSON-LD, `_headers`.

Zbývá **při spuštění**:
- Turnstile widget pro candadigitals.com → nahradit testovací `data-sitekey` v `site/index.html`
  (`1x00000000000000000000AA` = vždy projde) a dát secret do Pages
- secrets `RESEND_API_KEY`, `TURNSTILE_SECRET_KEY`, `TEST_TO`; ověřit doménu v Resendu
- odebrat `noindex` z `site/index.html`; `og:url` / `og:image` přepsat z github.io na
  candadigitals.com
- doplnit zástupné údaje v `site/privacy.html` a jméno v JSON-LD
- test formuláře naostro → pak `FORMS_LIVE = "true"`; Email Routing hello@ → Gmail
- vypnout GitHub Pages

Právní věci (rozhodnout s Chrisem, Claude není právník): živnost/firma + na web jméno, IČO a sídlo
(§ 435 OZ) dřív, než se začnou brát peníze; souhlas Key Sailing a Aveo s ukázkou na webu;
Google Fonts a knihovny z CDN přesunout přímo na web (GDPR — Mnichov 2022), čeká na Adamův
souhlas se stažením souborů; cookies se nepoužívají → lišta není potřeba.

Další verze: formulář přes Cloudflare Pages Function + Resend (jako Key Sailing),
3D logo v úvodu, ceny, hosting na Cloudflare Pages, vlastní doména a e-mail.

## Služby (pro budoucí web)

Vychází z práce pro Key Sailing (`../key-sailing-site/`). Jádro: **web + Google
Business Profile a recenze + měsíční péče**. Odlišení pro USA: **další jazykové verze** (nejčastěji španělština)
a **přístupnost (ADA)**. Dál: mapy a katalogy (Apple, Bing, Yelp, TripAdvisor),
viditelnost v AI (JSON-LD, `llms.txt`), rezervace a platby / dárkové poukazy
(Stripe), fotky a video, sociální sítě, chatbot a automatizace, logo a tiskoviny,
doména a firemní e-mail.

Ještě vyřešit: fakturace a daně za zakázky z USA (z Česka, nejspíš živnost).
