'use strict';
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const {chromium} = require('@playwright/test');

// Test suites target only the ephemeral loopback server started by run.cjs.
function settings() {
  assert.ok(process.env.TEST_BASE_URL, 'Use npm test; the runner starts an isolated local server.');
  const baseURL = new URL(process.env.TEST_BASE_URL);
  assert.equal(baseURL.protocol, 'http:');
  assert.equal(baseURL.hostname, '127.0.0.1');
  const outputDir = process.env.TEST_OUTPUT_DIR || path.join(__dirname, '..', 'test-results');
  fs.mkdirSync(outputDir, {recursive:true});
  return {baseURL:baseURL.href, output:name => path.join(outputDir, name)};
}
async function withBrowser(run) {
  const browser = await chromium.launch({headless:true});
  try { await run(browser); } finally { await browser.close(); }
}
module.exports = {settings, withBrowser};
