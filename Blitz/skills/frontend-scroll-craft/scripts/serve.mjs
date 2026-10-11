#!/usr/bin/env node
/**
 * Local scrollcraft preview. Modified by EauDoon for the v2.1 audit repair.
 * node serve.mjs --root builds/example --port 4500
 * Serve only a trusted preview directory on loopback. This is not production
 * hosting or a sandbox against a local process that can replace its files.
 */
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";

const TYPES = {
  ".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8", ".json": "application/json",
  ".mp4": "video/mp4", ".webm": "video/webm",
  ".webp": "image/webp", ".png": "image/png", ".jpg": "image/jpeg",
  ".svg": "image/svg+xml", ".woff2": "font/woff2",
};

function contained(root, candidate) {
  const relative = path.relative(root, candidate);
  return relative === "" || (!path.isAbsolute(relative) && relative !== ".." &&
    !relative.startsWith(".." + path.sep));
}

function reply(res, status, body, headers = {}) {
  if (res.destroyed || res.writableEnded) return;
  if (res.headersSent) { res.destroy(); return; }
  res.writeHead(status, { "Content-Type": "text/plain; charset=utf-8",
    "Cache-Control": "no-store", "X-Content-Type-Options": "nosniff", ...headers });
  res.end(body);
}

async function serve(root, req, res) {
  if (req.method !== "GET" && req.method !== "HEAD") {
    reply(res, 405, "method not allowed", { Allow: "GET, HEAD" }); return;
  }
  let decoded;
  try {
    if (typeof req.url !== "string" || req.url.length > 8192 || !req.url.startsWith("/")) throw Error();
    decoded = decodeURIComponent(req.url.split("?", 1)[0]);
    if (/[\\\0:]/.test(decoded)) throw Error();
  } catch { reply(res, 400, "bad request"); return; }
  const requested = path.resolve(root, "." + decoded);
  if (!contained(root, requested)) { reply(res, 403, "forbidden"); return; }
  let handle;
  try {
    let canonical = await fs.promises.realpath(requested);
    if (!contained(root, canonical)) { reply(res, 403, "forbidden"); return; }
    if ((await fs.promises.stat(canonical)).isDirectory()) {
      canonical = await fs.promises.realpath(path.join(canonical, "index.html"));
      if (!contained(root, canonical)) { reply(res, 403, "forbidden"); return; }
    }
    if (!(await fs.promises.stat(canonical)).isFile()) { reply(res, 403, "forbidden"); return; }
    // Stream the canonical descriptor, never reopen the user-supplied path.
    // O_NOFOLLOW also rejects a final symlink introduced before open on POSIX.
    handle = await fs.promises.open(canonical, fs.constants.O_RDONLY | (fs.constants.O_NOFOLLOW || 0));
    const stat = await handle.stat();
    const current = await fs.promises.stat(canonical);
    if (!stat.isFile() || stat.dev !== current.dev || stat.ino !== current.ino ||
        !contained(root, await fs.promises.realpath(canonical))) {
      reply(res, 403, "forbidden"); return;
    }
    if (res.destroyed) return;
    res.writeHead(200, {
      "Content-Type": TYPES[path.extname(canonical).toLowerCase()] || "application/octet-stream",
      "Content-Length": stat.size, "Cache-Control": "no-store",
      "X-Content-Type-Options": "nosniff",
    });
    if (req.method === "HEAD") { res.end(); return; }
    const stream = handle.createReadStream();
    handle = undefined; // The stream owns and closes the descriptor.
    stream.on("error", () => reply(res, 500, "read failed"));
    res.on("close", () => stream.destroy());
    stream.pipe(res);
  } catch (error) {
    const status = ["ENOENT", "ENOTDIR"].includes(error.code) ? 404 :
      ["EACCES", "EPERM", "ELOOP"].includes(error.code) ? 403 : 500;
    reply(res, status, status === 404 ? "not found" : status === 403 ? "forbidden" : "read failed");
  } finally { if (handle) await handle.close().catch(() => {}); }
}

export async function createPreviewServer(root) {
  const canonicalRoot = await fs.promises.realpath(path.resolve(root));
  if (!(await fs.promises.stat(canonicalRoot)).isDirectory()) throw new Error("Preview root must be a directory");
  return http.createServer((req, res) => { serve(canonicalRoot, req, res).catch(() => reply(res, 500, "read failed")); });
}

export async function startPreview(root, port = 4500) {
  const server = await createPreviewServer(root);
  await new Promise((resolve, reject) => {
    server.once("error", reject);
    server.listen(port, "127.0.0.1", () => { server.removeListener("error", reject); resolve(); });
  });
  return server;
}

async function main() {
  const argv = process.argv.slice(2);
  let root = ".", port = 4500;
  for (let i = 0; i < argv.length; i += 2) {
    if (!["--root", "--port"].includes(argv[i]) || !argv[i + 1]) throw Error("Usage: serve.mjs --root DIRECTORY --port PORT");
    if (argv[i] === "--root") root = argv[i + 1];
    else {
      if (!/^\d+$/.test(argv[i + 1])) throw Error("Port must be an integer from 0 to 65535");
      port = Number(argv[i + 1]);
    }
  }
  if (!Number.isInteger(port) || port < 0 || port > 65535) throw Error("Port must be an integer from 0 to 65535");
  const server = await startPreview(root, port);
  server.on("error", () => { console.error("Preview server could not listen"); process.exitCode = 1; });
  console.log(`scrollcraft: http://127.0.0.1:${server.address().port}`);
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  main().catch(() => { console.error("Preview setup failed; check root, port and local permissions"); process.exitCode = 1; });
}
