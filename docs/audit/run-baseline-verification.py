"""Read-only verification of this baseline using a temporary copy, not the live app."""
import ast
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[2]

def main():
    temp = Path(tempfile.mkdtemp(prefix='advocacy-baseline-'))
    clone = temp / 'app'
    reports = temp / 'reports'
    reports.mkdir()
    shutil.copytree(ROOT, clone, ignore=shutil.ignore_patterns('.git', 'node_modules', '__pycache__'))
    env = {k: v for k, v in os.environ.items() if not k.startswith('PROMPTQL_')}
    env['PORT'] = '18082'
    result = {'scope': 'Temporary copy on same VM; fresh npm ci; no PROMPTQL_* environment; copied tests have URL/output substitutions only. Not independent-machine reproduction.', 'steps': {}, 'reports': str(reports)}
    def run(label, args, timeout=180):
        process = subprocess.run(args, cwd=clone, env=env, capture_output=True, text=True, timeout=timeout)
        result['steps'][label] = {'exit_code': process.returncode, 'stdout': process.stdout, 'stderr': process.stderr}
        print(label, process.returncode, flush=True)
        return process.returncode
    assert run('npm ci', ['npm', 'ci']) == 0
    assert run('Chromium install', ['npx', 'playwright', 'install', 'chromium']) == 0
    assert run('JavaScript syntax', ['node', '--check', 'public/app.js']) == 0
    ast.parse((clone/'server.py').read_text())
    result['python_syntax'] = 'PASS'
    for name in ['smoke.cjs', 'views.cjs']:
        path=clone/'tests'/name
        path.write_text(path.read_text().replace('http://127.0.0.1:8080', 'http://127.0.0.1:18082').replace('/workspace/advocacy/tests', str(reports)))
    server = subprocess.Popen(['python3', str(clone/'server.py')], cwd=clone, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for attempt in range(100):
            try:
                with urllib.request.urlopen('http://127.0.0.1:18082/readyz', timeout=1) as response:
                    assert response.status == 204
                    result['readiness'] = 204
                    break
            except OSError:
                time.sleep(.1)
        else:
            raise RuntimeError('Copy server did not become ready')
        assert run('smoke.cjs', ['node', 'tests/smoke.cjs']) == 0
        assert run('views.cjs', ['node', 'tests/views.cjs']) == 0
        # Known placeholder must be reported rather than silently repaired.
        run('npm test (known placeholder)', ['npm', 'test'])
        for name in ['accessibility.json', 'view-tests.json']:
            result[name] = json.loads((reports/name).read_text())
    finally:
        server.terminate()
        server.wait(timeout=10)
    original = json.loads((ROOT/'docs/audit/preserved-source-manifest.json').read_text())
    result['preserved_sources_match'] = all(hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256'] for x in original)
    assert result['preserved_sources_match']
    (reports/'verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print('Verification report:', reports/'verification.json', flush=True)

if __name__ == '__main__':
    main()
