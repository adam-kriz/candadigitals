// Runs before every request on the site (Cloudflare Pages middleware).
// www.candadigitals.com → candadigitals.com with a permanent (301) redirect,
// keeping the path and query, so Google only ever sees one address.

export async function onRequest({ request, next }) {
  const url = new URL(request.url);
  if (url.hostname === "www.candadigitals.com") {
    url.hostname = "candadigitals.com";
    return Response.redirect(url.toString(), 301);
  }
  return next();
}
