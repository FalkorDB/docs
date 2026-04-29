/**
 * Cloudflare Worker / Pages Function: Markdown content negotiation for
 * docs.falkordb.com.
 *
 * The Jekyll build emits a clean `.md` version of every documentation
 * page next to its `.html` counterpart (see `_plugins/markdown_pages.rb`).
 * This worker honours the `Accept` header so AI tools that prefer
 * markdown can request the same URL and get markdown back without
 * having to know the `.md` URL pattern.
 *
 * Behaviour
 * ---------
 * - If the request `Accept` header is `text/markdown` (or
 *   `text/x-markdown` / `text/plain`) and the request is not already
 *   for a `.md` URL, the worker rewrites the request internally to the
 *   corresponding `.md` URL on the same origin and returns its body
 *   with `Content-Type: text/markdown; charset=utf-8`.
 * - All other requests are passed through unchanged.
 *
 * Mapping rules (mirroring the Jekyll plugin):
 *   /            -> /index.md
 *   /foo/        -> /foo/index.md
 *   /foo/bar.html -> /foo/bar.md
 *   /foo/bar     -> /foo/bar.md
 *
 * Deployment
 * ----------
 * Bind this worker to the `docs.falkordb.com/*` route in Cloudflare,
 * or use it as a Pages Function placed at `functions/_middleware.js`.
 */

const MARKDOWN_ACCEPT = /(?:^|,\s*)(text\/markdown|text\/x-markdown|text\/plain)\b/i;

function markdownPathFor(pathname) {
  if (pathname === "" || pathname === "/") return "/index.md";
  if (pathname.endsWith("/")) return pathname + "index.md";
  if (pathname.endsWith(".md")) return pathname;
  if (pathname.endsWith(".html")) return pathname.slice(0, -5) + ".md";
  // Skip URLs that already point at a static asset with an extension.
  const lastSegment = pathname.slice(pathname.lastIndexOf("/") + 1);
  if (lastSegment.includes(".")) return null;
  return pathname + ".md";
}

export default {
  async fetch(request) {
    const accept = request.headers.get("accept") || "";
    if (!MARKDOWN_ACCEPT.test(accept)) {
      return fetch(request);
    }

    const url = new URL(request.url);
    const mdPath = markdownPathFor(url.pathname);
    if (!mdPath || mdPath === url.pathname) {
      return fetch(request);
    }

    const mdUrl = new URL(url.toString());
    mdUrl.pathname = mdPath;

    const upstream = await fetch(mdUrl.toString(), {
      headers: { accept: "text/markdown" },
    });
    if (!upstream.ok) {
      // Fall back to the original HTML response if the .md sibling is
      // missing for any reason.
      return fetch(request);
    }

    const headers = new Headers(upstream.headers);
    headers.set("Content-Type", "text/markdown; charset=utf-8");
    headers.set("Vary", "Accept");
    return new Response(upstream.body, {
      status: upstream.status,
      statusText: upstream.statusText,
      headers,
    });
  },
};
