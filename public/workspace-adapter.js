/* The model never writes application state. Proposals are validated and applied by this adapter. */
(function(root,factory){const api=factory(typeof module==='object'&&module.exports?require('./case-model.js'):root.AdvocacyCase);if(typeof module==='object'&&module.exports)module.exports=api;else root.AdvocacyWorkspace=api;})(typeof globalThis!=='undefined'?globalThis:this,function(Case){
'use strict';
const keys=['schemaVersion','sources','institutions','claims','options','actions','summary','researchQuestions','limitations','metadata'];
function validate(raw){
 if(!raw||typeof raw!=='object'||Array.isArray(raw)||keys.some(k=>!Object.hasOwn(raw,k))||Object.keys(raw).some(k=>!keys.includes(k))||raw.schemaVersion!==1)throw Error('Unsupported research response.');
 if(typeof raw.summary!=='string'||raw.summary.length>60000)throw Error('Invalid research summary.');
 if(!Array.isArray(raw.limitations)||raw.limitations.length>30||raw.limitations.some(x=>typeof x!=='string'||x.length>4000))throw Error('Invalid limitations.');
 if(!raw.metadata||typeof raw.metadata!=='object'||Array.isArray(raw.metadata)||Object.keys(raw.metadata).length>10||Object.entries(raw.metadata).some(([k,v])=>k.length>100||typeof v!=='string'||v.length>1000))throw Error('Invalid research metadata.');
 const staged=Case.create();
 for(const k of ['sources','institutions','claims','options','actions','researchQuestions'])staged[k]=raw[k];
 staged.suggestions.text=raw.summary;
 Case.validate(staged); // Strict nested shape, limits, references, dates, URLs and status enums.
 return JSON.parse(JSON.stringify(raw));
}
function merge(current,raw){
 const patch=validate(raw), next=Case.validate(current);
 const ids=new Map();
 for(const s of patch.sources){
  const duplicate=next.sources.find(x=>x.url&&x.url===s.url);
  if(duplicate){ids.set(s.id,duplicate.id);continue;} // Never replace a user's source notes.
  if(next.sources.some(x=>x.id===s.id))throw Error('Source ID conflict. Existing work preserved.');
  next.sources.push(s);ids.set(s.id,s.id);
 }
 function append(key,records,unique){
  for(const item of records){
   if(next[key].some(x=>unique(x)===unique(item)))continue;
   if(next[key].some(x=>x.id===item.id))item.id=item.id+'-'+(next.revision.number+1)+'-'+next[key].length;
   next[key].push(item);
  }
 }
 append('institutions',patch.institutions.map(i=>({...i,sourceIds:i.sourceIds.map(s=>ids.get(s)||s)})),x=>x.name);
 append('claims',patch.claims.map(c=>({...c,sourceId:ids.get(c.sourceId)||c.sourceId})),x=>x.text);
 append('options',patch.options.map(o=>({...o,dependencies:o.dependencies.map(s=>ids.get(s)||s)})),x=>x.title);
 append('actions',patch.actions,x=>x.title);
 next.researchQuestions=[...new Set([...next.researchQuestions,...patch.researchQuestions])];
 next.suggestions.pending.push({id:'research-review-'+(next.revision.number+1),text:patch.summary,status:'needs-review'});
 next.revision.number++;next.revision.updatedAt=new Date().toISOString();next.revision.needsReview=true;
 // Atomic, detached replacement only after the full result is valid. Notes and drafts are unchanged.
 return Case.validate(next);
}
return {validate,merge};
});
