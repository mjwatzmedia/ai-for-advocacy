'use strict';
const {spawn} = require('node:child_process');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const assert = require('node:assert/strict');

async function main() {
  const unit = require('node:child_process').spawnSync(process.execPath,[require('node:path').join(__dirname,'case-model.cjs')],{stdio:'inherit'});
  if(unit.status!==0)throw Error('Case model validation failed');
  const requested = process.argv.slice(2);
  const allowed = ['smoke', 'views', 'privacy', 'roadmap', 'casefile'];
  const suites = requested.length ? requested : allowed;
  assert.ok(suites.every(name => allowed.includes(name)), 'Unknown test suite');
  const root = path.resolve(__dirname, '..');
  const output = path.resolve(process.env.TEST_OUTPUT_DIR || path.join(root, 'test-results'));
  fs.mkdirSync(output, {recursive:true});
  const env = Object.fromEntries(Object.entries(process.env).filter(([key]) => !key.startsWith('PROMPTQL_') && !/^(OPENAI|GEMINI)_/.test(key)));
  const scratch = fs.mkdtempSync(path.join(os.tmpdir(), 'advocacy-test-'));
  fs.cpSync(path.join(root, 'public'), path.join(scratch, 'public'), {recursive:true});
  const readyFile = path.join(scratch, 'ready.json');
  const harness = `import importlib.util, json, os
from pathlib import Path
spec = importlib.util.spec_from_file_location('advocacy_server', os.environ['TEST_SERVER_PATH'])
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)
app.ROOT = Path(os.environ['TEST_PUBLIC_PATH'])
server = app.ThreadingHTTPServer(('127.0.0.1', 0), app.Handler)
ready = Path(os.environ['TEST_READY_FILE'])
ready.with_suffix('.tmp').write_text(json.dumps({'port': server.server_port}))
ready.with_suffix('.tmp').replace(ready)
server.serve_forever()
`;
  // Test the real handler with copied assets, not the live service on port 8080.
  const server = spawn(env.PYTHON || 'python3', ['-B', '-u', '-c', harness], {
    cwd:scratch,
    env:{...env, TEST_SERVER_PATH:path.join(root, 'server.py'), TEST_PUBLIC_PATH:path.join(scratch, 'public'), TEST_READY_FILE:readyFile},
    stdio:['ignore', 'ignore', 'pipe']
  });
  let stderr = '', serverError, activeChild, interrupted = false;
  server.stderr.on('data', data => {stderr += data;});
  server.on('error', error => {serverError = error;});
  const interrupt = () => {
    interrupted = true;
    activeChild?.kill('SIGTERM');
    server.kill('SIGTERM');
    process.exitCode = 130;
  };
  process.on('SIGINT', interrupt);
  process.on('SIGTERM', interrupt);
  try {
    for (let tries=0; !fs.existsSync(readyFile); tries++) {
      if (serverError) throw serverError;
      if (interrupted || server.exitCode !== null || tries >= 100) throw Error('Isolated test server failed: '+stderr);
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    const {port} = JSON.parse(fs.readFileSync(readyFile, 'utf8'));
    const baseURL = `http://127.0.0.1:${port}/`;
    const response = await fetch(baseURL+'readyz', {signal:AbortSignal.timeout(5000)});
    assert.equal(response.status, 204);
    const results = [];
    for (const suite of suites) {
      if (interrupted) break;
      const code = await new Promise((resolve, reject) => {
        const child = spawn(process.execPath, [path.join(root, 'tests', suite+'.cjs')], {
          cwd:root, env:{...env, TEST_BASE_URL:baseURL, TEST_OUTPUT_DIR:output}, stdio:'inherit', timeout:120000
        });
        activeChild = child;
        child.on('error', reject);
        child.on('exit', (code, signal) => {activeChild = null; resolve(signal ? 1 : code);});
      });
      results.push({suite, exitCode:code});
    }
    fs.writeFileSync(path.join(output, 'summary.json'), JSON.stringify({server:'isolated loopback ephemeral port', suites:results}, null, 2)+'\n');
    if (!interrupted && results.some(result => result.exitCode !== 0)) process.exitCode = 1;
  } finally {
    process.removeListener('SIGINT', interrupt);
    process.removeListener('SIGTERM', interrupt);
    activeChild?.kill('SIGTERM');
    server.kill('SIGTERM');
    if (server.exitCode === null && server.signalCode === null && !serverError) await new Promise(resolve => server.once('exit', resolve));
    fs.rmSync(scratch, {recursive:true, force:true});
  }
}
main().catch(error => {console.error(error); process.exitCode = 1;});

