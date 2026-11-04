"""Synthetic tests: no live providers, credentials, or case data."""
import io
import json
import os
from pathlib import Path
import sys
import threading
import unittest
from unittest.mock import patch
import urllib.request
import urllib.error
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import server

class ProviderTests(unittest.TestCase):
    def test_provider_payloads_and_parsing(self):
        for provider, response in [('openai', {'status':'completed','output':[{'type':'message','content':[{'type':'output_text','text':'Synthetic answer'}]}]}), ('gemini', {'candidates':[{'finishReason':'STOP','content':{'parts':[{'text':'Synthetic answer'}]}}]})]:
            with self.subTest(provider=provider), patch.dict(os.environ, {provider.upper()+'_API_KEY':'synthetic-key',provider.upper()+'_MODEL':'synthetic-model'}, clear=True), patch('server.urllib.request.urlopen') as send:
                send.return_value.__enter__.return_value.read.return_value=json.dumps(response).encode()
                self.assertEqual(server.provider_plan(provider,'Synthetic concern'),'Synthetic answer')
                request=send.call_args.args[0]
                self.assertNotIn('synthetic-key',request.full_url)
                payload=json.loads(request.data)
                if provider=='openai': self.assertIs(payload['store'],False)
                else: self.assertIn('systemInstruction',payload)

    def test_unconfigured_and_incomplete(self):
        with patch.dict(os.environ,{},clear=True):
            with self.assertRaisesRegex(ValueError,'not configured'): server.provider_plan('openai','Synthetic')
        with patch.dict(os.environ,{'OPENAI_API_KEY':'synthetic','OPENAI_MODEL':'synthetic'},clear=True), patch('server.urllib.request.urlopen') as send:
            send.return_value.__enter__.return_value.read.return_value=b'{"status":"incomplete","output":[]}'
            with self.assertRaisesRegex(ValueError,'did not finish'): server.provider_plan('openai','Synthetic')

class HTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.http=server.ThreadingHTTPServer(('127.0.0.1',0),server.Handler)
        cls.thread=threading.Thread(target=cls.http.serve_forever,daemon=True);cls.thread.start()
        cls.base='http://127.0.0.1:'+str(cls.http.server_port)
    @classmethod
    def tearDownClass(cls): cls.http.shutdown();cls.http.server_close();cls.thread.join()
    def post(self, data, extra=None):
        headers={'Content-Type':'application/json','Origin':self.base,'X-Advocacy-Request':'1'}
        if extra: headers.update(extra)
        req=urllib.request.Request(self.base+'/api/plan',data=json.dumps(data).encode(),headers=headers)
        try:
            with urllib.request.urlopen(req) as resp:return resp.status,json.load(resp)
        except urllib.error.HTTPError as resp:return resp.code,json.load(resp)
    def test_guards_and_errors(self):
        data={'provider':'openai','prompt':'Synthetic concern','consent':True}
        with patch('server.provider_plan',return_value='Synthetic answer') as run:
            self.assertEqual(self.post(data)[0],200)
            self.assertEqual(self.post(data,{'Origin':'https://other.invalid'})[0],403)
            self.assertEqual(self.post(data,{'Host':'attacker.invalid'})[0],403)
            self.assertEqual(run.call_count,1)
            self.assertEqual(self.post({**data,'consent':False})[0],400)
            self.assertEqual(self.post({**data,'prompt':'x'*60001})[0],413)
        with patch('server.provider_plan',side_effect=RuntimeError('SECRET_AND_CASE_DATA')):
            code,result=self.post(data)
            self.assertEqual(code,502);self.assertNotIn('SECRET',json.dumps(result))
        self.assertTrue(server.AI_LOCK.acquire(blocking=False))
        try:self.assertEqual(self.post(data)[0],429)
        finally:server.AI_LOCK.release()

if __name__=='__main__':unittest.main()
