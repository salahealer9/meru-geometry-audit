#!/usr/bin/env python3
"""Future named S00-S12 invocation ONLY after human freeze and authorization.

Registered execution is prohibited before freeze. Normal-mode --help is safe.
An explicit flag is an acknowledgement, not a substitute for human authority.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import traceback

BASE = 'd15865167b4e3c454e398bd498d9d681103096f7'
EXPECTED_SIGNER = 'D4EC014EEFCC90E619D2AA59A91239ABCF512130'
ROOT = Path(__file__).resolve().parents[1]


def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT,stderr=subprocess.STDOUT)


def reject_optimized_mode():
    if sys.flags.optimize != 0:
        raise RuntimeError('optimized Python mode is prohibited for the registered runner')


def verify_expected_signer(status):
    """Require one valid signature by the exact named signing key.

    Called only after git verify-commit --raw succeeds. No human UID matching or
    acceptance of arbitrary valid keys; a different signing subkey is rejected.
    """
    rows = [line.split() for line in status.decode('utf-8', errors='strict').splitlines()
            if line.startswith('[GNUPG:] VALIDSIG ')]
    if len(rows) != 1 or len(rows[0]) not in (11, 12):
        raise ValueError('missing, malformed or multiple VALIDSIG signer records')
    row = rows[0]
    if row[2] != EXPECTED_SIGNER or (len(row) == 12 and row[11] != EXPECTED_SIGNER):
        raise ValueError('signature does not match expected freeze-signer fingerprint')


def verify_boundary(commit):
    reject_optimized_mode()
    if len(commit)!=40 or any(c not in '0123456789abcdef' for c in commit) or commit==BASE:
        raise ValueError('a distinct full implementation-freeze commit is required')
    if git('rev-parse','HEAD').decode().strip()!=commit:
        raise ValueError('HEAD does not equal named implementation freeze')
    if git('branch','--show-current').decode().strip()!='hebrew-projection-capacity-v0.9':
        raise ValueError('wrong branch')
    git('merge-base','--is-ancestor',BASE,commit)
    verify_expected_signer(git('verify-commit','--raw',commit))
    if git('status','--porcelain'):
        raise ValueError('require clean freeze worktree before run')
    manifest_path='registered_pilots/p0a0/implementation_manifest.json'
    data=git('show',commit+':'+manifest_path)
    if data!=(ROOT/manifest_path).read_bytes():
        raise ValueError('manifest differs from frozen commit')
    manifest=json.loads(data)
    for row in manifest['artifacts']:
        p=row['path']
        if Path(p).is_absolute() or '..' in Path(p).parts:
            raise ValueError('unsafe artifact path')
        content=(ROOT/p).read_bytes()
        if len(content)!=row['bytes'] or hashlib.sha256(content).hexdigest()!=row['sha256']:
            raise ValueError('worktree artifact mismatch: '+p)
        if content!=git('show',commit+':'+p):
            raise ValueError('artifact not frozen in named commit: '+p)
    return hashlib.sha256(data).hexdigest()


def main():
    reject_optimized_mode()
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--freeze-commit',required=True)
    parser.add_argument('--authorized-synthetic-run',action='store_true',required=True)
    parser.add_argument('--output',type=Path,required=True,help='new JSONL path outside repository')
    args=parser.parse_args()
    if not args.authorized_synthetic_run:
        parser.error('separate authorization required')
    manifest_hash=verify_boundary(args.freeze_commit)
    output=args.output.resolve()
    if output.is_relative_to(ROOT):
        raise ValueError('output must be outside protected repository')
    # Never overwrite an earlier run. Reserve the output before loading fixtures.
    fd=os.open(output,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    sys.path[:0]=[str(ROOT/'src'),str(ROOT/'registered_pilots/p0a0')]
    from fixtures import configuration
    from cases import evaluate
    config=configuration()
    failed=False
    with os.fdopen(fd,'w') as stream:
        header={'type':'run_boundary','freeze_commit':args.freeze_commit,
                'implementation_manifest_sha256':manifest_hash,
                'scope':'SYNTHETIC_ONLY','no_hebrew_inputs':True}
        stream.write(json.dumps(header,sort_keys=True,allow_nan=False)+'\n'); stream.flush()
        for case in sorted(config['cases']):
            try:
                record=evaluate(case,config)
            except Exception as exc:
                failed=True
                record={'case':case,'state':'FAIL','exception':type(exc).__name__,
                        'explanation':str(exc),'traceback':traceback.format_exc(),
                        'raw':{'state':'INCOMPLETE'},'normalized':{'state':'INCOMPLETE'}}
            stream.write(json.dumps(record,sort_keys=True,allow_nan=False)+'\n'); stream.flush()
    return 1 if failed else 0


if __name__=='__main__':
    raise SystemExit(main())
