'use strict';
const assert=require('node:assert/strict'),{spawn}=require('node:child_process'),{chromium}=require('@playwright/test'),net=require('node:net'),path=require('node:path');
(async()=>{
 const root=path.resolve(__dirname,'..'),listener=net.createServer();
 await new Promise(r=>listener.listen(0,'127.0.0.1',r));const port=listener.address().port;await new Promise(r=>listener.close(r));
 const env=Object.fromEntries(Object.entries(process.env).filter(([k])=>!k.startsWith('PROMPTQL_')&&!k.startsWith('ADVOCACY_')&&!/^(OPENAI|GEMINI)_/.test(k)));
 const server=spawn(path.join(root,'backend/.venv/bin/python'),['-m','tests.browser_fixture',String(port)],{cwd:path.join(root,'backend'),env,stdio:['ignore','ignore','pipe']});
 let errors='';server.stderr.on('data',x=>errors+=x);
 let browser;
 try{
  const url=`http://127.0.0.1:${port}`;
  for(let i=0;;i++){try{if((await fetch(url+'/health')).ok)break;}catch{}if(i>100||server.exitCode!==null)throw Error('Fixture failed: '+errors);await new Promise(r=>setTimeout(r,100));}
  browser=await chromium.launch({headless:true});const page=await browser.newPage();const browserErrors=[];page.on('pageerror',e=>browserErrors.push(e.message));
  await page.goto(url);await page.locator('#concern').fill('Fictional residents want safer street crossings.');
  await page.locator('#goal').fill('Learn public input options.');await page.locator('#location').fill('Tucson, Arizona');await page.locator('#country').selectOption('us');
  await page.locator('#intake-form button[type=submit]').click();
  await page.locator('#authority-notes').fill('MY CONFIRMED NOTES');
  await page.locator('#tab-actions').click();await page.locator('#draft-text').fill('MY EXISTING DRAFT');
  await page.locator('#action-list input').first().check();await page.locator('#tab-plan').click();
  await page.locator('#research-run').click();
  assert.match(await page.locator('#research-status').textContent(),/consent/);
  await page.locator('#research-consent').check();await page.locator('#research-run').click();await page.waitForFunction(()=>!document.getElementById('research-apply').disabled);
  assert.equal(await page.locator('.source-card').count(),0,'Nothing applied automatically');
  await page.locator('#research-apply').click();
  assert.equal(await page.locator('#authority-notes').inputValue(),'MY CONFIRMED NOTES');
  assert.equal(await page.locator('#draft-text').inputValue(),'MY EXISTING DRAFT');
  assert.equal(await page.locator('#action-list input').first().isChecked(),true);
  assert.equal(await page.locator('.source-card').count(),1);
  assert.ok((await page.locator('#research-options').textContent()).includes('petition'));
  const downloadEvent=page.waitForEvent('download');await page.locator('#export-case').click();const download=await downloadEvent;
  const fs=require('node:fs'),caseData=JSON.parse(fs.readFileSync(await download.path(),'utf8'));assert.equal(caseData.options.length,5);
  await page.locator('#research-run').click();await page.waitForFunction(()=>!document.getElementById('research-apply').disabled);
  await page.locator('#authority-notes').fill('NEW EDIT DURING REVIEW');await page.locator('#research-apply').click();
  assert.match(await page.locator('#research-status').textContent(),/Workspace changed/);
  assert.equal(await page.locator('#authority-notes').inputValue(),'NEW EDIT DURING REVIEW');
  await page.route('**/api/workspace',r=>r.fulfill({json:{schemaVersion:1,correspondence:'MALICIOUS OVERWRITE'}}));
  await page.locator('#research-run').click();await page.waitForFunction(()=>document.getElementById('research-status').textContent.includes('Unsupported'));
  assert.equal(await page.locator('#draft-text').inputValue(),'MY EXISTING DRAFT');
  await page.unroute('**/api/workspace');
  await page.locator('#campaign-kind').selectOption('call');page.once('dialog',d=>d.accept());await page.locator('#campaign-draft').click();
  await page.waitForFunction(()=>document.getElementById('draft-text').value.includes('DRAFT: call'));
  assert.match(await page.locator('#draft-text').inputValue(),/Nothing has been sent/);
  await page.locator('#tab-plan').click();page.once('dialog',d=>d.accept());await page.locator('#clear-workspace').click();
  assert.equal(await page.locator('#research-authorities').textContent(),'');assert.equal(await page.locator('#research-options').textContent(),'');
  assert.equal(await page.locator('#research-preview').textContent(),'');assert.equal(await page.locator('#research-consent').isChecked(),false);
  assert.deepEqual(browserErrors,[]);
  console.log('Real backend/browser mapping, review, stale edit guards, malicious response, campaign draft, export, privacy reset: PASS (synthetic retrieval; no live AI)');
 }finally{await browser?.close();server.kill('SIGTERM');}
})().catch(e=>{console.error(e);process.exitCode=1});
