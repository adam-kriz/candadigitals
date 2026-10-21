// POST /api/contact — the "I need..." form → email through Resend.
// (Same approach as key-sailing-site/functions/api/contact.js.)
//
// Safety: until FORMS_LIVE is "true" (wrangler.toml), every message goes to
// TEST_TO and never to the live inbox.
//
// Settings: wrangler.toml [vars] SITE_NAME, MAIL_FROM, LIVE_TO, FORMS_LIVE.
// Secrets (Cloudflare dashboard, never in the repo): RESEND_API_KEY,
// TURNSTILE_SECRET_KEY, TEST_TO.

const FIELDS = [
  ["needs", "Needs"],
  ["name", "Name"],
  ["business", "Business"],
  ["email", "Email"],
  ["message", "Message"],
];
const REQUIRED = ["name", "email"];
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export async function onRequestPost({ request, env }) {
  let data;
  try {
    data = await request.formData();
  } catch {
    return json({ ok: false, error: "bad-request" }, 400);
  }

  // Honeypot: people never see this field, bots fill it in. Pretend it worked, send nothing.
  if (String(data.get("website") || "").trim() !== "") return json({ ok: true });

  const live = env.FORMS_LIVE === "true";
  const to = live ? env.LIVE_TO : env.TEST_TO;
  // Names only (never values), so a missing setting is easy to spot.
  const missing = [live ? "LIVE_TO" : "TEST_TO", "RESEND_API_KEY", "TURNSTILE_SECRET_KEY"].filter(
    (name) => !(name === "LIVE_TO" || name === "TEST_TO" ? to : env[name])
  );
  if (missing.length) return json({ ok: false, error: "not-configured", missing }, 500);

  if (!(await turnstileOk(data.get("cf-turnstile-response"), env, request))) {
    return json({ ok: false, error: "turnstile" }, 403);
  }

  const values = {};
  for (const [key] of FIELDS) {
    const v = String(data.get(key) || "").trim();
    if (v) values[key] = v.slice(0, 4000);
  }
  for (const key of REQUIRED) {
    if (!values[key]) return json({ ok: false, error: "missing", field: key }, 400);
  }
  if (!EMAIL_RE.test(values.email)) return json({ ok: false, error: "email" }, 400);

  const who = values.name.replace(/[\r\n]+/g, " ").slice(0, 80);
  const subject = `${live ? "" : "[TEST] "}${env.SITE_NAME || "Website"}: new enquiry from ${who}`;
  const text =
    FIELDS.filter(([key]) => values[key]).map(([key, label]) => `${label}: ${values[key]}`).join("\n\n") +
    `\n\n--\nSent from the form at ${new URL(request.url).host}${live ? "" : " (test mode)"}`;

  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify({ from: env.MAIL_FROM, to: [to], subject, text, reply_to: values.email }),
  });
  if (!res.ok) {
    console.log("Resend error", res.status, await res.text());
    return json({ ok: false, error: "send" }, 502);
  }
  return json({ ok: true });
}

async function turnstileOk(token, env, request) {
  if (!token) return false;
  const body = new FormData();
  body.append("secret", env.TURNSTILE_SECRET_KEY);
  body.append("response", String(token));
  const ip = request.headers.get("CF-Connecting-IP");
  if (ip) body.append("remoteip", ip);
  try {
    const r = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", { method: "POST", body });
    const out = await r.json();
    return out.success === true;
  } catch {
    return false;
  }
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "Content-Type": "application/json", "Cache-Control": "no-store" },
  });
}
