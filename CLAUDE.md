# candadigitals

Vlastní značka a budoucí web **C&A Digitals**: Adam (A) a jeho kamarád Chris (C)
dělají weby a další digitální služby pro malé firmy, **hlavně v USA** (Florida).
Web bude **anglicky**.

## Status

**Spuštěno na https://candadigitals.com (22. 10. 2026).** Původně: **Jen značka (20. 10. 2026)**: název a logo jsou uložené „prozatím“, můžou se ještě
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
| `site/index.html` | celá stránka: **Hero „tři vrstvy“** (od 25. 10. 2026: vlevo nadpis „We build your website. Then we take care of it.“, hned pod ním tlačítka Book a free call / See our work, pak krátký text a 3 odznaky důvěry — štítek „Web studio in Florida and Prague“ nad nadpisem Adam nechtěl, odebrán; vpravo SVG s rozloženými vrstvami loga v izometrii — modrá Found on Google, krémová Your website, tmavá Care and updates, ikony na horních plochách přes matici `matrix(1.5,-0.75,1.5,0.75,-150,0)`, popisky vpravo, na mobilu jako seznam; vrstvy při načtení spadnou, jemně se vznáší, při scrollu se rozestoupí) → pás „Recently launched“ → pás služeb → Intro → Work → **About** (Chris a Adam bez fotek; od 25. 10. 2026 **jen křestní jména** i v JSON-LD a texty, že **všechno děláme oba společně** — žádné dělení rolí, oba „Co-founder“) → Services → Packages → How we work → Contact „I need…“ → patička |
| `site/style.css` | vzhled; barvy jako proměnné v `:root` (stejné jako logo) |
| `site/js/main.js` | animace, interakce a odeslání formuláře |
| `site/images/og.jpg` | náhled odkazu (iMessage, WhatsApp, Messenger): screenshot úvodu 1200×630; v `<head>` jako `og:image` s absolutní adresou na github.io — při přesunu na vlastní doménu změnit |
| `site/images/work/` | screenshot projektu v sekci Work: Key Sailing Sarasota |

| `site/privacy.html` | Privacy Policy (GDPR + US); **obsahuje zástupné údaje** `[Chris's full name]`, `[Postal address]` (červeně) — doplnit před spuštěním |
| `site/404.html` | stránka „Lost a layer.“ (absolutní cesty `/…`) |
| `site/robots.txt`, `site/sitemap.xml`, `site/llms.txt` | pro vyhledávače a AI; JSON-LD (`ProfessionalService`) je v `<head>` index.html — u zakladatele „Chris“ doplnit celé jméno |
| `site/_headers` | bezpečnostní hlavičky + `noindex` pro náhledy na `*.pages.dev` |
| `functions/_middleware.js` | přesměrování www.candadigitals.com → candadigitals.com (301) |
| `functions/api/contact.js` | formulář → e-mail přes Resend, ochrana honeypot + Turnstile (převzato z Key Sailing) |
| `wrangler.toml` | nastavení Pages: výstup `site`, proměnné; `FORMS_LIVE = "false"` → vše jde na `TEST_TO` |

Knihovny (od 21. 10. 2026 v `site/js/vendor/`, ne z CDN): **GSAP 3.12.5 + ScrollTrigger** (animace při scrollu), **Lenis 1.1.13**
(plynulý scroll), **Matter.js 0.19.0** (padající štítky v kontaktu). Písmo Hanken Grotesk ze `site/fonts/`.

Animace: úvod viz výše (vrstvy loga při scrollu rozestoupí — Adamovi se to líbí, nechat); intro text se při scrollu „rozsvěcuje“ po slovech; u projektů jede za
myší náhled; služby = rozbalovací seznam (otevřená jen jedna); čára „How we work“ se
kreslí při scrollu; štítky „I need…“ padají a jdou přetahovat (jen počítač s myší, na
mobilu obyčejná tlačítka; vlastní smyčka s pevným krokem 1/120 s, spaní těl proti chvění,
štítky padají „z neznáma“ až ~420 px nad rámečkem z náhodných míst, náhodně
nakloněné a postrčené; jakmile jsou všechny uvnitř (nejpozději po 4 s), zavře se strop, menší štítky, rámeček 340 px na
celou šířku (jako v první verzi), limit rychlosti hodu, tažení slyší celé okno, stěny se přepočítají při změně
velikosti; žádné poskakování — Adam nechce, aby štítky vylétávaly); magnetická tlačítka. Hodiny „Our desk“ Florida a Praha (bez počasí, Adam ho 20. 10. 2026 nechtěl). **Omezené animace v systému → klidná verze** bez
animací a plynulého scrollu (ověřeno).

Zatím **náhled**: `noindex`, e-mail `hello@candadigitals.com` je **jen zástupný**
(doména není koupená), formulář nic neposílá (jen hláška „preview“). Projekty v sekci Work: od 25. 10. 2026 **jen Key Sailing Sarasota** (Aveo Adam odebral). Texty jsou Claudův návrh
— Adam a Chris je upraví. „Our desk“ = Florida a Praha (Adam 20. 10. 2026).

Rozmazání pod hlavičkou po scrollu = **jen 2 vrstvy** `backdrop-filter` (silná nahoře, slabá níž) +
slábnoucí tónování. Se 4 vrstvami se scroll trhal (změřeno 21. 10. 2026) — vrstvy nepřidávat.

Lokální náhled: konfigurace `candadigitals` v kořenovém `.claude/launch.json`
(Python `http.server`, port 8130, složka `candadigitals/site`) → http://localhost:8130.
Lokálně formulář ukáže „Sorry, that didn't send“ (Python server neumí funkci) — to je v pořádku.

## Nasazení na candadigitals.com (plán z 21. 10. 2026)

Firemní Gmail: **candadigitals@gmail.com** (založen 22. 10. 2026, Adam). Účet **Cloudflare** na tenhle
Gmail (přihlášení přes Google, 2FA hlídá Google); doména **candadigitals.com koupená 22. 10. 2026** přes
Cloudflare Registrar (auto-renew). **Cloudflare Pages** projekt `candadigitals` napojený na GitHub
(jen tohle repo), výstup `site`, běží na **https://candadigitals.pages.dev** (22. 10. 2026; náhled má
`X-Robots-Tag: noindex`, `CLAUDE.md`/`wrangler.toml`/`functions` vrací 404, `/api/contact` čeká na secrets).
Pozor: nový Cloudflare nabízí při „Create“ nejdřív **Workers** — Pages je odkaz „Looking to deploy Pages?“. Rozhodnuto: firemní Gmail → účet Cloudflare → doména **candadigitals.com** přes Cloudflare
Registrar; hosting **Cloudflare Pages** (Adam povolil propojení s GitHubem); e-mail **zdarma**
přes Cloudflare Email Routing (přeposílání do Gmailu); Resend = existující účet (přidat doménu);
obsah webu zatím beze změny. Účty a platby dělá Adam sám, Claude dává návod.

Hotovo v kódu (21. 10. 2026, commitnuté, **nepushnuté**, protože přesun do `site/` vypne
náhled na github.io — pushnout až při propojení s Cloudflare Pages): přesun do `site/`,
formulář, Privacy Policy, 404, robots/sitemap/llms.txt/JSON-LD, `_headers`.

Kontaktní e-mail na webu = **candadigitals@gmail.com** (Adam 22. 10. 2026; dřív zástupný
hello@candadigitals.com). Formulář chodí na `LIVE_TO` = tentýž Gmail. Email Routing hello@ zatím
neřešíme — kdyby se zavedl, vrátit adresu na webu (index, privacy, llms.txt, main.js, wrangler.toml).

**Další kroky (pořadí domluvené s Adamem 22. 10. 2026):**
1. ~~Custom domains~~ candadigitals.com + www **Active** (22. 10. 2026; https od Google Trust Services,
   http → https 301). www → bez www řeší `functions/_middleware.js` (301, zachová cestu i parametry) —
   Redirect Rules v novém dashboardu Adam nenašel
2. Turnstile widget „C&A Digitals“ (hostnames candadigitals.com + candadigitals.pages.dev, Managed) —
   site key `0x4AAAAAAFgp_X2hEJ11RfCa` je v `site/index.html` (22. 10. 2026); secret je v Pages jako
   `TURNSTILE_SECRET_KEY` (Adam, 22. 10. 2026; funkce ho vidí). Lokálně (localhost) widget hlásí chybu — to je v pořádku
3. ~~Resend~~ doména candadigitals.com ověřená (DKIM `resend._domainkey`, `send` MX/SPF), klíč
   `RESEND_API_KEY` v Pages — hotovo 22. 10. 2026
4. ~~Test formuláře~~ prošel 22. 10. 2026 (Adam, zpráva dorazila do Gmailu) → `FORMS_LIVE = "true"`.
   Secrets `RESEND_API_KEY`, `TURNSTILE_SECRET_KEY` v Pages (typ **Secret**, prostředí **Production**;
   textové proměnné z dashboardu Pages ignoruje, protože existuje `wrangler.toml` → `TEST_TO` je v něm) → test formuláře →
   `FORMS_LIVE = "true"`
5. Chris = **Christian Robert Nielsen** (doplněno v privacy.html i JSON-LD 22. 10. 2026);
   místo adresy jen „Palm Coast, Florida, USA“ (kde bydlí Chris; Adam 22. 10. 2026 — podle GDPR
   stačí jména + e-mail). **Povinné před první placenou zakázkou:** živnost → na web (patička +
   privacy) jméno, celou adresu místa podnikání a IČO (§ 435 OZ)
6. Ostré spuštění — kód připravený 22. 10. 2026: pryč `noindex` z index.html (privacy.html a 404
   ho mají dál schválně), `og:url`/`og:image` na candadigitals.com, canonical privacy → `/privacy`
   (odkazy v HTML zůstávají `privacy.html` kvůli lokálnímu náhledu; Pages je přesměruje 308),
   Turnstile pod 360 px šířky v režimu `compact`.
   **SPUŠTĚNO 22. 10. 2026** — web na https://candadigitals.com je otevřený vyhledávačům (pages.dev
   dál `noindex`), GitHub Pages vypnuté (github.io/candadigitals vrací 404)
7. Po spuštění: Search Console + Bing (sitemap), Cloudflare Web Analytics

Zbývá **při spuštění**:
- Turnstile widget pro candadigitals.com → nahradit testovací `data-sitekey` v `site/index.html`
  (`1x00000000000000000000AA` = vždy projde) a dát secret do Pages
- secrets `RESEND_API_KEY`, `TURNSTILE_SECRET_KEY`, `TEST_TO`; ověřit doménu v Resendu
- odebrat `noindex` z `site/index.html`; `og:url` / `og:image` přepsat z github.io na
  candadigitals.com
- doplnit zástupné údaje v `site/privacy.html` a jméno v JSON-LD
- test formuláře naostro → pak `FORMS_LIVE = "true"`; Email Routing hello@ → Gmail
- vypnout GitHub Pages

**Adam (22. 10. 2026): živnost, IČO na webu, fakturace/daně a souhlasy Jan a Aveo Claude sám
nepřipomíná — řeší je Adam, až sám začne.**

Právní věci (rozhodnout s Chrisem, Claude není právník): živnost/firma + na web jméno, IČO a sídlo
(§ 435 OZ) dřív, než se začnou brát peníze; souhlas Key Sailing a Aveo s ukázkou na webu;
Google Fonts a knihovny z CDN jsou **přímo na webu** (21. 10. 2026, kvůli GDPR — Mnichov 2022):
`site/fonts/` (Hanken Grotesk latin + latin-ext, licence `OFL.txt`) a `site/js/vendor/` (GSAP 3.12.5,
ScrollTrigger, Lenis 1.1.13, Matter.js 0.19.0; kontrolní součty ověřené proti cdnjs). Jediná cizí
adresa je Cloudflare Turnstile (nutné pro ochranu formuláře, uvedené v Privacy Policy); cookies se nepoužívají → lišta není potřeba.

Další verze: formulář přes Cloudflare Pages Function + Resend (jako Key Sailing),
3D logo v úvodu, ceny, hosting na Cloudflare Pages, vlastní doména a e-mail.

## Jazyky a barva (od 22. 10. 2026)

- **Akcent: elektrická modrá** `--accent: #5B87FF` (Adam vybral „elektrickou modrou“ #4F7DFF, ta ale
  nesplnila kontrast 4,5 : 1 na tmavém pozadí → o odstín světlejší). Text na modré = `--accent-ink`
  `#121721`; na světlých plochách (menu, karta Growth) `--accent-deep` `#2F5EEB`. Modrá je: horní
  vrstva loga na webu (soubory v `brand/` zůstaly šedé), poslední slovo nadpisu, tlačítka, čísla,
  vybrané štítky, čára „How we work“.
- **Úvod:** cílí na kohokoli (Adam: „prakticky na kohokoliv“), tlačítka **Book a free call** (→ #contact,
  Calendly zatím není) a **See our work**, pod úvodem pás „Recently launched“ (Key Sailing).
- **Překlady:** angličtina je zdroj (`site/index.html`, `site/privacy.html`). Španělština (`site/es/`,
  vykání „usted“) a čeština (`site/cs/`, vykání) se **generují** skriptem `i18n/build.py`
  (`python3 candadigitals/i18n/build.py`) — **ručně je neupravovat**. Po změně anglického textu
  doplnit překlad do skriptu a spustit ho; když anglický text v HTML nenajde, skončí chybou.
  Přepínač EN · ES · CS v hlavičce, `hreflang` v `<head>`, sitemap se všemi jazyky. Hlášky
  skriptu (formulář, kopírování) jsou v `MESSAGES` v `js/main.js`. Formulář posílá i `lang`.
  Španělštinu by měl časem zkontrolovat rodilý mluvčí. Adam chce časem i další jazyky.

## Služby (pro budoucí web)

Vychází z práce pro Key Sailing (`../key-sailing-site/`). Jádro: **web + Google
Business Profile a recenze + měsíční péče**. Odlišení pro USA: **další jazykové verze** (nejčastěji španělština)
a **přístupnost (ADA)**. Dál: mapy a katalogy (Apple, Bing, Yelp, TripAdvisor),
viditelnost v AI (JSON-LD, `llms.txt`), rezervace a platby / dárkové poukazy
(Stripe), fotky a video, sociální sítě, chatbot a automatizace, logo a tiskoviny,
doména a firemní e-mail.

Ještě vyřešit: fakturace a daně za zakázky z USA (z Česka, nejspíš živnost).
