import json
import os
import urllib.request
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent
BASE=os.environ['PROMPTQL_PLATFORM_API_URL']+'/v1'
BOT=os.environ['PROMPTQL_THREAD_ID']

def put(identifier, data, kind, content_type, title, file_name=None):
    headers={'Authorization':'Bearer '+os.environ['PROMPTQL_USER_JWT'], 'Content-Type':content_type, 'X-PromptQL-Artifact-Type':kind,'X-PromptQL-Artifact-Title':title.replace('—','-'),'X-PromptQL-Artifact-Hidden':'false'}
    if file_name:headers['X-PromptQL-Artifact-File-Name']=file_name
    req=urllib.request.Request(f'{BASE}/artifacts/threads/{BOT}/{identifier}',data=data,method='PUT',headers=headers)
    with urllib.request.urlopen(req,timeout=60) as resp:
        print(identifier,resp.status,resp.read().decode())

config={'version':2,'host':'vm','sandbox_id':os.environ['PROMPTQL_SANDBOX_ID'],'kind':'web','port':8080,'protocol':'http','readiness':{'path':'/readyz'}}
with urllib.request.urlopen('http://127.0.0.1:8080/readyz') as resp:
    assert resp.status==204
put('ai-for-advocacy',json.dumps(config).encode(),'app','application/json','AI for Advocacy — Working Prototype')
archive=ROOT/'ai-for-advocacy-source.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for name in ['README.md','server.py','package.json','package-lock.json']:
        z.write(ROOT/name,'ai-for-advocacy/'+name)
    for folder in ['public','tests']:
        for path in (ROOT/folder).iterdir():
            if path.suffix in ['.html','.css','.js','.svg','.cjs','.json','.py']:
                z.write(path,'ai-for-advocacy/'+str(path.relative_to(ROOT)))
put('ai-for-advocacy-source',archive.read_bytes(),'file','application/zip','AI for Advocacy — Source Code & Tests','ai-for-advocacy-source.zip')

