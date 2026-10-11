import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import http from "node:http";
import { Readable } from "node:stream";
import { startPreview } from "../../Blitz/skills/frontend-scroll-craft/scripts/serve.mjs";

test("preview serves only its canonical root on loopback and survives bad requests", async t => {
  const base = await fs.promises.mkdtemp(path.join(os.tmpdir(), "blitz-preview-test-"));
  const root = path.join(base, "site"), sibling = path.join(base, "site-private");
  await fs.promises.mkdir(root); await fs.promises.mkdir(sibling);
  await fs.promises.mkdir(path.join(root, "nested")); await fs.promises.mkdir(path.join(root, "empty"));
  await fs.promises.writeFile(path.join(root, "index.html"), "SYNTHETIC INSIDE");
  await fs.promises.writeFile(path.join(root, "nested/index.html"), "SYNTHETIC NESTED");
  await fs.promises.writeFile(path.join(root, "style.css"), "body{color:black}");
  await fs.promises.writeFile(path.join(root, "broken.txt"), "SYNTHETIC STREAM");
  await fs.promises.writeFile(path.join(sibling, "outside.txt"), "SYNTHETIC OUTSIDE");
  const server = await startPreview(root, 0);
  const address = server.address(); assert.equal(address.address, "127.0.0.1");
  t.after(async () => {
    server.closeAllConnections(); await new Promise(resolve => server.close(resolve));
    await fs.promises.rm(base, { recursive: true, force: true });
  });
  const request = (url, method = "GET") => new Promise((resolve, reject) => {
    const req = http.request({ host: "127.0.0.1", port: address.port, path: url, method }, res => {
      const chunks = []; res.on("data", b => chunks.push(b)); res.on("error", reject);
      res.on("end", () => resolve({ status: res.statusCode, headers: res.headers, body: Buffer.concat(chunks).toString() }));
    });
    req.on("error", reject); req.setTimeout(3000, () => req.destroy(Error("timeout"))); req.end();
  });
  for (const [url, status, body] of [
    ["/", 200, "SYNTHETIC INSIDE"], ["/?cache=1", 200, "SYNTHETIC INSIDE"],
    ["/nested/", 200, "SYNTHETIC NESTED"], ["/missing.txt", 404, "not found"], ["/empty/", 404, "not found"],
    ["/%2e%2e/site-private/outside.txt", 403, "forbidden"], ["/../site-private/outside.txt", 403, "forbidden"],
    ["/nested/../../site-private/outside.txt", 403, "forbidden"], ["/%", 400, "bad request"],
    ["/%E0%A4%A", 400, "bad request"], ["/%00", 400, "bad request"], ["/..%5csite-private/outside.txt", 400, "bad request"],
  ]) await t.test(url, async () => {
    const result = await request(url); assert.equal(result.status, status); assert.equal(result.body, body);
    assert.equal(result.headers["cache-control"], "no-store");
  });
  await t.test("HEAD and method restriction", async () => {
    const head = await request("/", "HEAD"); assert.equal(head.status, 200); assert.equal(head.body, "");
    assert.equal(Number(head.headers["content-length"]), "SYNTHETIC INSIDE".length);
    assert.equal((await request("/", "POST")).status, 405);
    assert.match((await request("/style.css")).headers["content-type"], /^text\/css/);
  });
  for (const [name, target, type, url] of [
    ["escaped.txt", path.join(sibling, "outside.txt"), "file", "/escaped.txt"],
    ["escaped-dir", sibling, process.platform === "win32" ? "junction" : "dir", "/escaped-dir/outside.txt"],
    ["nested/index.html", path.join(sibling, "outside.txt"), "file", "/nested/"],
  ]) await t.test("symlink escape " + name, async sub => {
    const link = path.join(root, name);
    if (name === "nested/index.html") await fs.promises.unlink(link);
    try { await fs.promises.symlink(target, link, type); }
    catch (error) {
      if (process.platform === "win32" && ["EPERM", "EACCES"].includes(error.code)) { sub.skip("Windows symlink privilege unavailable; Linux must execute this case"); return; }
      throw error;
    }
    const result = await request(url); assert.equal(result.status, 403); assert.equal(result.body, "forbidden");
  });
  await t.test("filesystem errors are controlled and omit exception details", async () => {
    const realpath = fs.promises.realpath;
    fs.promises.realpath = async p => {
      if (p.endsWith("denied")) throw Object.assign(Error("SYNTHETIC DIAGNOSTIC"), { code: "EACCES" });
      if (p.endsWith("io-error")) throw Object.assign(Error("SYNTHETIC DIAGNOSTIC"), { code: "EIO" });
      return realpath(p);
    };
    try {
      for (const [url, expected] of [["/denied", 403], ["/io-error", 500]]) {
        const result = await request(url); assert.equal(result.status, expected); assert.ok(!result.body.includes("DIAGNOSTIC"));
      }
    } finally { fs.promises.realpath = realpath; }
    assert.equal((await request("/")).status, 200);
  });
  await t.test("stream errors do not crash the server", async () => {
    const open = fs.promises.open;
    fs.promises.open = async (...args) => {
      const handle = await open(...args);
      if (args[0].endsWith("broken.txt")) handle.createReadStream = () => {
        const stream = new Readable({ read() { this.destroy(Error("synthetic read failure")); } });
        stream.on("close", () => handle.close()); return stream;
      };
      return handle;
    };
    try { await assert.rejects(request("/broken.txt")); }
    finally { fs.promises.open = open; }
    assert.equal((await request("/")).status, 200);
  });
});
