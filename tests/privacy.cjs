'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const {settings, withBrowser} = require('./helpers.cjs');
const {baseURL, output} = settings();

withBrowser(async browser => {
  const context = await browser.newContext();
  const page = await context.newPage();
  const errors = [], unexpected = [];
  page.on('pageerror', error => errors.push(error.message));
  // All application requests must be local static GETs. Count GET exfiltration too.
  page.on('request', request => {
    const url = new URL(request.url());
    const allowed = ['/', '/index.html', '/app.js', '/case-model.js', '/workspace-adapter.js', '/research-workspace.js', '/style.css', '/favicon.svg'];
    if (url.origin !== new URL(baseURL).origin || request.method() !== 'GET' || !allowed.includes(url.pathname) || url.search) unexpected.push(request.url());
  });
  await page.goto(baseURL);
  const marker = 'RESET_REGRESSION_SYNTHETIC_7f9b';
  for (const id of ['concern', 'goal', 'location']) await page.locator('#'+id).fill(marker+' '+id);
  await page.locator('#country').selectOption('us');
  await page.locator('#intake-form button[type=submit]').click();
  await page.locator('#authority-notes').fill(marker+' institution notes');
  await page.locator('#strategy-notes').fill(marker+' strategy notes');
  await page.locator('#strategy-list input').first().check();
  await page.locator('#evidence-checklist input').first().check();
  await page.locator('#tab-sources').click();
  await page.locator('#source-title').fill(marker+' source');
  await page.locator('#source-url').fill('https://example.invalid/'+marker);
  await page.locator('#source-notes').fill(marker+' evidence');
  await page.locator('#source-form button[type=submit]').click();
  await page.getByRole('button', {name:/Edit source:/}).click();
  await page.locator('#tab-actions').click();
  await page.locator('#action-title').fill(marker+' action');
  await page.locator('#action-date').fill('2026-11-05');
  await page.locator('#action-basis').fill(marker+' personal target');
  await page.locator('#action-form button[type=submit]').click();
  await page.locator('.action-item input').last().check();
  await page.locator('#followup-notes').fill(marker+' response');
  await page.locator('#make-draft').click();
  await page.locator('#draft-text').fill(marker+' edited draft');
  await page.locator('#action-title').fill(marker+' unsaved action');
  await page.locator('#tab-plan').click();
  const snapshot = () => page.evaluate(() => ({
    state:JSON.parse(JSON.stringify(state)),
    html:document.querySelector('#workspace-view').innerHTML,
    fields:[...document.querySelectorAll('input,textarea,select')].map(node => [node.id,node.value,node.checked])
  }));
  await page.locator('#ai-output').fill(marker+' unverified AI suggestions');
  await page.locator('#ai-prompt-text').evaluate((node, marker) => {node.value=marker;node.hidden=false;}, marker);
  const before = await snapshot();
  page.once('dialog', dialog => dialog.dismiss());
  await page.locator('#clear-workspace').click();
  assert.deepEqual(await snapshot(), before, 'Cancel must preserve every field and rendered entry');
  page.once('dialog', dialog => dialog.accept());
  await page.locator('#clear-workspace').click();
  const cleared = await page.evaluate(marker => ({
    state:JSON.parse(JSON.stringify(state)),
    htmlResidue:document.documentElement.outerHTML.includes(marker),
    fieldResidue:[...document.querySelectorAll('input,textarea,select')].some(node => node.value.includes(marker)),
    summaries:['concern','goal','location'].map(id => document.getElementById('summary-'+id).textContent),
    counts:[document.querySelectorAll('.source-card').length,document.querySelectorAll('.action-item').length,document.getElementById('source-count').textContent],
    notes:['authority-notes','strategy-notes','followup-notes','draft-text'].map(id => document.getElementById(id).value),
    checks:[...document.querySelectorAll('input[type=checkbox]')].some(node => node.checked),
    country:document.getElementById('country').selectedIndex,
    storage:localStorage.length+sessionStorage.length,
    cookies:document.cookie,
    focus:document.activeElement.id,
    selectedTab:document.querySelector('[role=tab][aria-selected=true]').id,
    errors:[...document.querySelectorAll('.field-error')].some(node => node.textContent),
    researchLinks:document.querySelectorAll('#research-links a').length
  }), marker);
  assert.equal(cleared.htmlResidue, false, 'Cleared case remains in hidden DOM/attributes');
  assert.equal(cleared.fieldResidue, false, 'Cleared case remains in form values');
  assert.deepEqual(cleared.state, {story:null,sources:[],actions:[],currentTab:'plan',sourceEditId:null});
  assert.deepEqual(cleared.summaries, ['', '', '']);
  assert.deepEqual(cleared.counts, [0,0,'0']);
  assert.deepEqual(cleared.notes, ['', '', '', '']);
  assert.equal(cleared.checks, false);
  assert.equal(cleared.country, 0);
  assert.equal(cleared.storage, 0);
  assert.equal(cleared.cookies, '');
  assert.equal(cleared.focus, 'concern');
  assert.equal(cleared.selectedTab, 'tab-plan');
  assert.equal(cleared.errors, false);
  assert.equal(cleared.researchLinks, 0);
  await page.locator('#nav-sources').click();
  await page.locator('#intake-view').waitFor({state:'visible'});
  // A new case must not resurrect old notes, sources, actions, draft, or export text.
  for (const id of ['concern','goal','location']) await page.locator('#'+id).fill('Second synthetic case '+id);
  await page.locator('#intake-form button[type=submit]').click();
  assert.equal(await page.locator('.source-card').count(), 0);
  assert.equal(await page.locator('.action-item').count(), 2);
  assert.equal(await page.locator('#draft-text').inputValue(), '');
  const downloadPromise = page.waitForEvent('download');
  await page.locator('#export-markdown').click();
  const download = await downloadPromise;
  const text = fs.readFileSync(await download.path(), 'utf8');
  assert.ok(text.includes('Second synthetic case'));
  assert.ok(!text.includes(marker), 'Export contains cleared case');
  page.once('dialog', dialog => dialog.accept());
  await page.reload();
  assert.equal(await page.locator('#concern').inputValue(), '');
  assert.equal(await page.evaluate(() => state.story), null);
  assert.deepEqual(errors, []);
  assert.deepEqual(unexpected, []);
  fs.writeFileSync(output('privacy.json'), JSON.stringify({result:'PASS',cancelPreservesCase:true,acceptedClearPurgesDOMAndState:true,newCaseAndExportIsolated:true,reloadClearsSession:true,unexpectedRequests:unexpected.length,browserErrors:errors.length},null,2)+'\n');
  console.log('Privacy regression: PASS');
}).catch(error => {console.error(error);process.exitCode=1;});

