'use strict';
(function(){
 let pending=null,active=null;
 const preview=$('research-preview'), status=$('research-status'), run=$('research-run'), apply=$('research-apply');
 function reset(){
  if(active)active.abort();active=null;pending=null;preview.replaceChildren();apply.disabled=true;run.disabled=false;
  $('research-consent').checked=false;$('research-ai-consent').checked=false;status.textContent='';
 }
 function render(){
  const target=$('researched-results'),authorities=$('research-authorities'),options=$('research-options');target.replaceChildren();authorities.replaceChildren();options.replaceChildren();
  if(!caseData.institutions.length&&!caseData.options.length&&!caseData.claims.length)return;
  target.append(el('h3','','Research additions — review before relying on them'));
  for(const i of caseData.institutions)authorities.append(el('h4','',i.name),el('p','',i.responsibility),el('span','badge','Candidate institution · needs review'));
  for(const c of caseData.claims)target.append(el('p','',c.text),el('p','tiny',c.limitation));
  for(const o of caseData.options)options.append(el('h4','',o.title),el('p','',o.evidence),el('p','tiny',o.limitations));
  for(const p of caseData.suggestions.pending)target.append(el('p','research-summary',p.text));
 }
 async function research(){
  if(!state.story){toast('Tell us your concern, goal and location first.');return;}
  if(!$('research-consent').checked){status.textContent='Please consent to fetching public sources first.';return;}
  if(active)return;
  const snapshot=JSON.stringify(captureCase()),controller=new AbortController();active=controller;
  const timer=setTimeout(()=>controller.abort(),120000);
  run.disabled=true;pending=null;apply.disabled=true;preview.replaceChildren();status.textContent='Fetching source pages and preparing structured suggestions…';
  try{
   const urls=$('research-urls').value.split('\n').map(x=>x.trim()).filter(Boolean);
   const body={concern:state.story.concern,outcome:state.story.goal,location:state.story.location,country:state.story.country,
    consent_retrieval:true,consent_ai:$('research-ai-consent').checked,urls};
   const response=await fetch('/api/workspace',{method:'POST',headers:{'Content-Type':'application/json','X-Advocacy-Request':'1'},body:JSON.stringify(body),signal:controller.signal});
   const data=await response.json();
   if(!response.ok)throw Error(typeof data.error==='string'?data.error:(data.error?.message||'Research API unavailable. Run the documented research server.'));
   if(active!==controller)return;
   if(JSON.stringify(captureCase())!==snapshot){status.textContent='Workspace changed while researching. Nothing applied; research again when ready.';return;}
   const validated=AdvocacyWorkspace.validate(data);
   pending={data:validated,snapshot};
   preview.append(el('p','research-summary',validated.summary));
   preview.append(el('p','',`${validated.sources.length} source records · ${validated.institutions.length} candidate institutions · ${validated.options.length} options`));
   for(const s of validated.sources){const a=el('a','',s.title+' ↗');a.href=s.url;a.target='_blank';a.rel='noopener noreferrer';const card=el('div','card');card.append(a,el('p','',s.notes));preview.append(card);}
   for(const o of validated.options)preview.append(el('h4','',o.title),el('p','',o.evidence));
   apply.disabled=false;status.textContent='Ready to review. Retrieved sources are not proof that an avenue applies or is open. No edits have been replaced.';
  }catch(error){if(active===controller)status.textContent=error.name==='AbortError'?'Research timed out or was cancelled. Your work is intact.':error.message;}
  finally{clearTimeout(timer);if(active===controller){active=null;run.disabled=false;}}
 }
 apply.onclick=()=>{
  if(!pending)return;
  if(JSON.stringify(captureCase())!==pending.snapshot){pending=null;apply.disabled=true;status.textContent='Workspace changed since preview. Research again; existing work is intact.';return;}
  try{
   const next=AdvocacyWorkspace.merge(captureCase(),pending.data);
   // No hydration: avoid resetting the current tab, input drafts, or explicit research consent.
   caseData=next;renderSources();renderActions();render();pending=null;apply.disabled=true;
   status.textContent='Added reviewed proposals to their boxes. Your notes, draft, selected approach and completed actions were preserved.';
  }catch(error){status.textContent='Not applied: '+error.message;}
 };
 run.onclick=research;
 $('campaign-draft').onclick=async()=>{
  if(!state.story)return;
  const before=$('draft-text').value, story=JSON.stringify(state.story), kind=$('campaign-kind').value;
  if(before.trim()&&!confirm('Replace the existing correspondence draft? Download or copy it first.'))return;
  try{
   const response=await fetch('/api/drafts',{method:'POST',headers:{'Content-Type':'application/json','X-Advocacy-Request':'1'},
    body:JSON.stringify({concern:state.story.concern,outcome:state.story.goal,kind,notes:$('strategy-notes').value})});
   const data=await response.json();if(!response.ok||typeof data.text!=='string'||data.text.length>60000)throw Error('Draft API unavailable.');
   if($('draft-text').value!==before||JSON.stringify(state.story)!==story){status.textContent='Draft or story changed; generated text not applied.';return;}
   $('draft-text').value=data.text;noteChange();setTab('actions');status.textContent='Editable campaign template created. Nothing was submitted, signed or called.';
  }catch(error){status.textContent=error.message;}
 };
 // Imports, reset and intake edits must not resurrect a stale response.
 $('clear-workspace').addEventListener('click',()=>{if(!state.story)reset();render();});
 $('intake-form').addEventListener('submit',()=>{reset();render();});
 $('case-file-input').addEventListener('change',()=>{reset();});
 const priorHydrate=hydrateCase;hydrateCase=function(next){reset();priorHydrate(next);render();};
 document.addEventListener('click',event=>{if(event.target.closest('[data-tab],#nav-roadmap'))render();});
})();
