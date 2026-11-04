// Compile and render the actual export helper in an isolated local browser.
import {test} from 'node:test';
import assert from 'node:assert/strict';
import {spawn} from 'node:child_process';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';

test('DOM export preserves nested SVG, page styles and internal dependencies', {timeout: 45000}, async t => {
  const chrome = process.env.CHROME_BIN || (process.platform === 'win32'
    ? 'C:/Program Files/Google/Chrome/Application/chrome.exe' : '/usr/bin/google-chrome');
  await fs.access(chrome); // A missing renderer is a failed gate, never a silent skip.
  const root = await fs.mkdtemp(path.join(os.tmpdir(), 'blitz-svg-test-'));
  const profile = path.join(root, 'browser');
  await fs.mkdir(profile);
  const source = path.join(root, 'source.html');
  await fs.writeFile(source, `<!doctype html><style>
    body{margin:0;font-family:Arial;color:#225577;--ink:#225577}
    .caption{font-size:24px;fill:var(--ink)} .icon{fill:currentColor}
    .css-geometry{x:360px;y:30px;width:80px;height:80px;fill:#225577}
    main>svg{display:block;width:480px;height:240px}
    </style><main><svg id="diagram" viewBox="0 0 480 240" xmlns="http://www.w3.org/2000/svg">
    <defs><linearGradient id="tone"><stop stop-color="#ee6633"/><stop offset="1" stop-color="#ffdd99"/></linearGradient>
    <clipPath id="window"><rect x="20" y="20" width="180" height="100"/></clipPath></defs>
    <rect width="480" height="240" fill="white"/>
    <rect x="20" y="20" width="220" height="120" fill="url(#tone)" clip-path="url(#window)"/>
    <svg x="260" y="30" width="80" height="80" viewBox="0 0 40 40"><circle class="icon" cx="20" cy="20" r="16"/></svg>
    <rect class="css-geometry"/>
    <text class="caption" x="24" y="190">Nested icon and inherited style</text></svg>
    <svg id="sibling" viewBox="0 0 20 20"><text>EXCLUDED SIBLING</text></svg></main>`);
  const proc = spawn(chrome, ['--headless', '--disable-gpu', '--disable-background-networking', '--no-first-run',
    '--no-default-browser-check', '--remote-debugging-port=0', '--user-data-dir=' + profile, 'about:blank'],
    {windowsHide: true, stdio: 'ignore'});
  let socket, call;
  t.after(async () => {
    if (call && socket?.readyState === 1) await call('Browser.close').catch(() => {});
    socket?.close(); proc.kill();
    // Delete only the exact disposable fixture directory created by this test.
    assert.equal(path.dirname(root), path.resolve(os.tmpdir()));
    await fs.rm(root, {recursive: true, force: true, maxRetries: 10, retryDelay: 100}).catch(() => {});
  });
  const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
  // A cold CI runner can take over 10 s to create a fresh profile; allow 30 s, but stop
  // at once if the browser exits, so a crash still fails fast and names its exit code.
  let port, exited = null;
  proc.once('exit', code => { exited = code; });
  for (let i = 0; i < 300 && exited === null; i++) {
    try {port = (await fs.readFile(path.join(profile, 'DevToolsActivePort'), 'utf8')).split('\n')[0]; break;}
    catch {await delay(100);}
  }
  assert.ok(port, exited === null ? 'Browser did not expose its isolated endpoint within 30 s'
    : 'Browser exited with code ' + exited + ' before exposing its endpoint');
  const tabs = await (await fetch('http://127.0.0.1:' + port + '/json/list')).json();
  socket = new WebSocket(tabs.find(tab => tab.type === 'page').webSocketDebuggerUrl);
  await new Promise((resolve, reject) => {socket.onopen = resolve; socket.onerror = reject;});
  let sequence = 0; const pending = new Map();
  socket.onmessage = event => {
    const message = JSON.parse(event.data); const waiter = pending.get(message.id);
    if (!waiter) return;
    pending.delete(message.id); clearTimeout(waiter.timer);
    const error = message.error || message.result?.exceptionDetails;
    error ? waiter.reject(Error(JSON.stringify(error))) : waiter.resolve(message.result);
  };
  call = (method, params = {}) => new Promise((resolve, reject) => {
    const id = ++sequence;
    const timer = setTimeout(() => {pending.delete(id); reject(Error('Browser command timeout: ' + method));}, 7000);
    pending.set(id, {resolve, reject, timer}); socket.send(JSON.stringify({id, method, params}));
  });
  const evaluate = async expression => (await call('Runtime.evaluate', {expression, returnByValue: true, awaitPromise: true})).result.value;
  await call('Page.enable'); await call('Network.enable');
  await call('Network.setBlockedURLs', {urls: ['http://*', 'https://*']});
  await call('Emulation.setDeviceMetricsOverride', {width: 640, height: 480, deviceScaleFactor: 1, mobile: false});
  await call('Page.navigate', {url: pathToFileURL(source).href}); await delay(200);
  await evaluate('document.fonts.ready');
  const shot = async () => (await call('Page.captureScreenshot', {format: 'png', clip: {x: 0, y: 0, width: 480, height: 240, scale: 1}})).data;
  const before = await shot();
  const helper = await fs.readFile(fileURLToPath(new URL('../../Blitz/skills/diagram-design/scripts/export-svg.js', import.meta.url)), 'utf8');
  await evaluate(helper);
  await assert.rejects(evaluate('blitzExportSvg("main > svg")'), /exactly one/);
  const xml = await evaluate('blitzExportSvg("#diagram")');
  assert.equal((xml.match(/<svg\b/g) || []).length, 2);
  assert.ok(!xml.includes('EXCLUDED SIBLING'));
  assert.ok(xml.includes('rgb(34, 85, 119)'));
  assert.ok(xml.includes('xmlns="http://www.w3.org/2000/svg"'));
  await evaluate('document.querySelector("#diagram").insertAdjacentHTML("beforeend", \'<use href="#missing"/>\')');
  await assert.rejects(evaluate('blitzExportSvg("#diagram")'), /use-instance inheritance/);
  await evaluate('document.querySelector("#diagram use").remove(); document.querySelector("#diagram rect").style.fill="url(#missing)"');
  await assert.rejects(evaluate('blitzExportSvg("#diagram")'), /missing SVG dependency/);
  const output = path.join(root, 'exported.svg'); await fs.writeFile(output, xml);
  await call('Page.navigate', {url: pathToFileURL(output).href}); await delay(200);
  await evaluate('document.fonts.ready'); const after = await shot();
  const pixels = await evaluate(`(async()=>{const canvas=document.createElementNS('http://www.w3.org/1999/xhtml','canvas');canvas.width=480;canvas.height=240;
    const context=canvas.getContext('2d');const arrays=[];for(const value of ${JSON.stringify([before, after])}){
      const image=new Image();image.src='data:image/png;base64,'+value;await image.decode();context.clearRect(0,0,480,240);context.drawImage(image,0,0);arrays.push(context.getImageData(0,0,480,240).data);}
    let changed=0;for(let i=0;i<arrays[0].length;i++)if(arrays[0][i]!==arrays[1][i])changed++;return changed;})()`);
  assert.equal(pixels, 0, 'Standalone styled/nested SVG pixels differ from the selected source');
  if (process.env.BLITZ_VISUAL_EVIDENCE) {
    const evidence = path.resolve(process.env.BLITZ_VISUAL_EVIDENCE); await fs.mkdir(evidence, {recursive: true});
    await fs.writeFile(path.join(evidence, 'source.png'), Buffer.from(before, 'base64'));
    await fs.writeFile(path.join(evidence, 'exported.png'), Buffer.from(after, 'base64'));
    await fs.writeFile(path.join(evidence, 'exported.svg'), xml);
  }
});
