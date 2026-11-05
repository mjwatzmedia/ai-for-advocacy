'use strict';
const assert=require('node:assert/strict');const fs=require('node:fs');const {settings,withBrowser}=require('./helpers.cjs');const {baseURL,output}=settings();
withBrowser(async browser=>{
 const context=await browser.newContext();const page=await context.newPage();const errors=[],unexpected=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('request',r=>{const u=new URL(r.url());if(r.method()!=='GET'||u.origin!==new URL(baseURL).origin||u.search)unexpected.push(r.url());});
 await page.goto(baseURL);
 for(const [id,value] of Object.entries({concern:'Fictional water review <img src=x onerror=alert(1)> café',goal:'Understand a published proposal',location:'Fictional Pima County neighborhood'}))await page.locator('#'+id).fill(value);
 await page.locator('#country').selectOption('us');await page.locator('#intake-form button[type=submit]').click();
 for(const [id,value] of Object.entries({'authority-notes':'User institutional notes','strategy-notes':'User strategy edits','ai-output':'User-edited unverified suggestion'}))await page.locator('#'+id).fill(value);
 await page.locator('#evidence-checklist input').first().check();await page.locator('#strategy-list input').first().check();
 await page.locator('#tab-sources').click();await page.locator('#source-title').fill('Fictional lead');await page.locator('#source-url').fill('https://example.invalid/proposal');await page.locator('#source-notes').fill('No retrieval performed');await page.locator('#source-form button[type=submit]').click();
 await page.getByRole('button',{name:/Edit source:/}).click();await page.locator('#source-title').fill('Unsubmitted source edit');
 await page.locator('#tab-actions').click();await page.locator('#followup-notes').fill('User response notes');await page.locator('#draft-text').fill('User correspondence');await page.locator('.action-item input').first().check();await page.locator('#action-title').fill('Unsubmitted action');await page.locator('#action-date').fill('2026-11-08');await page.locator('#action-basis').fill('Personal target');
 // Model-only structured fields must also be retained/exported, not silently dropped.
 await page.evaluate(()=>{caseData.sources[0].documentHash='synthetic-document-hash';caseData.sources[0].passages=[{id:'passage-1',text:'Synthetic quoted passage',locator:'Fictional section'}];caseData.claims=[{id:'claim-1',text:'Claim awaiting evidence review',sourceId:caseData.sources[0].id,documentHash:'synthetic-document-hash',passage:'Synthetic quoted passage',locator:'Fictional section',jurisdiction:'unresolved',checkedAt:'',status:'unverified',limitation:'Fictional fixture'}];caseData.preferences.notes='One hour available';caseData.userReports=[{id:'report-1',text:'Synthetic user report',origin:'user'}];caseData.openQuestions=['Find original publisher'];caseData.suggestions.pending=[{id:'pending-1',text:'A suggestion awaiting review',status:'unverified'}];});
 await page.locator('#ai-consent').check();
 async function download(){const p=page.waitForEvent('download');await page.locator('#export-case').click();const d=await p;assert.equal(d.suggestedFilename(),'my-advocacy-case.json');return JSON.parse(fs.readFileSync(await d.path(),'utf8'));}
 const original=await download();assert.equal(original.actions[0].done,true);assert.equal(original.buffers.source.title,'Unsubmitted source edit');assert.equal(original.buffers.action.title,'Unsubmitted action');assert.equal(original.suggestions.text,'User-edited unverified suggestion');assert.ok(!JSON.stringify(original).includes('ai-consent'));
 // Reload discards application state; restoration must not depend on its prior in-page memory.
 page.once('dialog',d=>d.accept());await page.reload();assert.equal(await page.evaluate(()=>state.story),null);
 async function upload(data,accept=true){page.once('dialog',d=>accept?d.accept():d.dismiss());await page.locator('#case-file-input').setInputFiles({name:'case.json',mimeType:'application/json',buffer:Buffer.from(typeof data==='string'?data:JSON.stringify(data))});}
 await upload(original);await page.waitForFunction(()=>state.story!==null);
 assert.equal(await page.locator('#ai-consent').isChecked(),false);assert.equal(await page.locator('#source-title').inputValue(),'Unsubmitted source edit');assert.equal(await page.locator('#action-title').inputValue(),'Unsubmitted action');
 assert.deepEqual(await download(),original,'Lossless restore of canonical case, progress and unsaved buffers');
 assert.equal(await page.locator('#authority-list img').count(),0);
 const snapshot=()=>page.evaluate(()=>JSON.stringify(captureCase()));const before=await snapshot();
 const other=structuredClone(original);other.story.goal='A different goal';
 await upload(other,false);assert.equal(await snapshot(),before,'Cancelled replacement preserves current work');
 // Invalid input must never reach the confirmation step or alter current work.
 async function invalid(raw,expected){await page.locator('#case-file-input').setInputFiles({name:'invalid.json',mimeType:'application/json',buffer:Buffer.from(raw)});await page.waitForFunction(expected=>document.getElementById('case-file-status').textContent.includes(expected),expected);assert.equal(await snapshot(),before);}
 await invalid('{invalid','invalid JSON');await invalid(JSON.stringify({...original,schemaVersion:99}),'schema version');
 const unsafe=structuredClone(original);unsafe.sources[0].url='javascript:alert(1)';await invalid(JSON.stringify(unsafe),'http(s)');
 await invalid('{"__proto__":{"polluted":true}}','unsupported');await invalid('x'.repeat(1000001),'maximum file size');assert.equal(await page.evaluate(()=>({}).polluted),undefined);
 await page.locator('#tab-plan').click();await page.locator('#edit-story').click();await page.locator('#goal').fill('Corrected user goal');await page.locator('#location').fill('Unknown changed location');await page.locator('#intake-form button[type=submit]').click();
 assert.equal(await page.locator('#ai-output').inputValue(),'User-edited unverified suggestion');assert.equal(await page.locator('#draft-text').inputValue(),'User correspondence');assert.equal(await page.evaluate(()=>state.actions[0].done),true);assert.equal(await page.evaluate(()=>caseData.revision.needsReview),true);
 const p=page.waitForEvent('download');await page.locator('#export-markdown').click();const md=fs.readFileSync(await (await p).path(),'utf8');for(const term of ['Corrected user goal','Synthetic user report','Find original publisher','One hour available','A suggestion awaiting review','Synthetic quoted passage','synthetic-document-hash','review affected'])assert.ok(md.includes(term),term);
 // Removing a source must not erase user claim text or strand an unexportable reference.
 await page.locator('#tab-sources').click();page.once('dialog',d=>d.accept());await page.getByRole('button',{name:/Remove source:/}).click();
 const afterRemoval=await download();assert.equal(afterRemoval.claims[0].sourceId,'');assert.equal(afterRemoval.claims[0].status,'needs-review');assert.equal(afterRemoval.claims[0].text,'Claim awaiting evidence review');
 // A separate page/context has no access to this in-memory case.
 const otherContext=await browser.newContext();const otherPage=await otherContext.newPage();await otherPage.goto(baseURL);assert.equal(await otherPage.evaluate(()=>state.story),null);await otherContext.close();
 // Reset purges canonical fields too, not just the legacy facade and DOM.
 await page.locator('#tab-plan').click();
 page.once('dialog',d=>d.accept());await page.locator('#clear-workspace').click();assert.equal(await page.evaluate(()=>caseData.openQuestions.length+caseData.userReports.length),0);
 assert.equal(await page.evaluate(()=>localStorage.length+sessionStorage.length),0);assert.deepEqual(unexpected,[]);assert.deepEqual(errors,[]);
 fs.writeFileSync(output('casefile.json'),JSON.stringify({result:'PASS',roundtrip:true,invalidAtomic:true,consentNotRestored:true,goalCorrectionPreservesEdits:true,noNetworkOrStorage:true,browserErrors:errors.length},null,2));await context.close();console.log('Case-file return and preservation: PASS');
}).catch(e=>{console.error(e);process.exitCode=1;});
