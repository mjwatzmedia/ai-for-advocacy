'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const {execFileSync} = require('node:child_process');
const {settings, withBrowser} = require('./helpers.cjs');
const {baseURL, output} = settings();
withBrowser(async browser => {
  const context = await browser.newContext();
  const page = await context.newPage();
  const requests = [];
  page.on('request', r => {if(r.method()==='POST')requests.push(r.url());});
  await page.goto(baseURL);
  await page.locator('#concern').fill('Fictional water review <script>alert(1)</script> & café');
  await page.locator('#goal').fill('Understand the proposal');
  await page.locator('#location').fill('Example City');
  await page.locator('#intake-form button[type=submit]').click();
  await page.locator('#authority-notes').fill('Contact still needs confirmation.');
  await page.locator('#strategy-notes').fill('Ask for information first.');
  await page.locator('#strategy-list input').first().check();
  await page.locator('#ai-output').fill('Unverified AI idea: investigate the original notice.');
  // Merely viewing/editing/exporting a roadmap must not send any case data.
  const downloadPromise=page.waitForEvent('download');
  await page.locator('#export-plan').click();
  const download=await downloadPromise;
  assert.equal(download.suggestedFilename(),'my-advocacy-roadmap.docx');
  const target=output('synthetic-roadmap.docx');
  await download.saveAs(target);
  const text=execFileSync(process.env.PYTHON||'python3',['-c',`import sys,zipfile,xml.etree.ElementTree as E
with zipfile.ZipFile(sys.argv[1]) as z:
 assert z.testzip() is None
 for name in z.namelist(): E.fromstring(z.read(name))
 root=E.fromstring(z.read('word/document.xml'))
 print('\\n'.join(root.itertext()))`,target],{encoding:'utf8'});
  for(const value of ['café','<script>alert(1)</script> &','Contact still needs confirmation.','Ask for information first.','Unverified AI idea','AI-generated and unverified'])assert.ok(text.includes(value),value);
  assert.deepEqual(requests,[]);
  await page.locator('#ai-generate').click();
  assert.deepEqual(requests,[],'No provider request without consent');
  await page.locator('#ai-consent').check();
  await page.locator('#ai-generate').click();
  await page.waitForFunction(()=>document.getElementById('ai-status').textContent.includes('not configured'));
  assert.equal(await page.locator('#ai-output').inputValue(),'Unverified AI idea: investigate the original notice.');
  // Mock response exercises browser integration without a live provider or costs.
  await page.route('**/api/plan', route=>route.fulfill({json:{text:'<img src=x onerror=alert(1)> Synthetic AI advice',provider:'openai'}}));
  await page.locator('#ai-generate').click();
  await page.waitForFunction(()=>document.getElementById('ai-output').value.startsWith('<img'));
  assert.equal(await page.locator('#ai-output img').count(),0);
  // A delayed completion must not resurrect cleared case content.
  let finish;
  const delayed=new Promise(resolve=>{finish=resolve;});
  await page.unroute('**/api/plan');
  await page.route('**/api/plan',async route=>{await delayed;try{await route.fulfill({json:{text:'CLEARED_CASE_RESIDUE'}});}catch{}});
  await page.locator('#ai-generate').click();
  await page.waitForFunction(()=>document.getElementById('ai-generate').disabled);
  page.once('dialog', d=>d.accept());
  await page.locator('#clear-workspace').click();
  finish();
  assert.equal(await page.locator('#ai-output').inputValue(),'');
  assert.equal(await page.locator('#ai-consent').isChecked(),false);
  assert.equal(await page.evaluate(()=>localStorage.length+sessionStorage.length),0);
  await context.close();
  console.log('Word export and AI browser integration: PASS');
}).catch(error=>{console.error(error);process.exitCode=1;});
