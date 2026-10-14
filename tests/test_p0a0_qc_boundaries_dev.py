"""Bounded amendment DEV checks. Never import/execute registered case modules."""
import ast
import importlib.util
import math
import os
from pathlib import Path
import subprocess
import sys

import pytest
from meru_geometry.p0a0.boundaries import require, parse_pi_bounds

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT/'scripts/p0a0_registered_pilot.py'


def load_runner():
    spec = importlib.util.spec_from_file_location('p0a0_dev_qc_runner', RUNNER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_dev_registered_conditions_are_explicit_source_only():
    # AST inspection does not import, compile for execution, or call any case.
    tree = ast.parse((ROOT/'registered_pilots/p0a0/cases.py').read_text())
    assert not any(isinstance(n, ast.Assert) for n in ast.walk(tree))
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)
             and isinstance(n.func, ast.Name) and n.func.id == 'require']
    assert len(calls) == 22
    assert all(len(n.args) == 2 and isinstance(n.args[1], ast.Constant) for n in calls)
    bounds = [n for n in ast.walk(tree) if isinstance(n, ast.Call)
              and isinstance(n.func, ast.Attribute) and n.func.attr == 'local_planar_search']
    assert len(bounds) == 1
    assert ast.dump(bounds[0].args[0]) == ast.dump(ast.parse("parse_pi_bounds(f['local_bounds'])",mode='eval').body)


def test_dev_invariant_true_and_false():
    require(17 > 9, 'DEV true')
    with pytest.raises(AssertionError,match='DEV false'):
        require(17 < 9, 'DEV false')


@pytest.mark.parametrize('flag',['-O','-OO'])
@pytest.mark.parametrize('condition',['17 > 9','17 < 9'])
def test_dev_invariants_survive_optimization(flag, condition):
    code = ('from meru_geometry.p0a0.boundaries import require; '
            f'require({condition}, "DEV invariant sentinel")')
    result = subprocess.run([sys.executable,flag,'-c',code],cwd=ROOT,
                            capture_output=True,text=True)
    if condition == '17 < 9':
        assert result.returncode != 0
        assert 'AssertionError: DEV invariant sentinel' in result.stderr
    else:
        assert result.returncode == 0, result.stderr


@pytest.mark.parametrize('mode',['-O','-OO','PYTHONOPTIMIZE'])
def test_dev_runner_rejects_optimization_before_arguments_or_io(mode, tmp_path):
    env = os.environ.copy()
    env.pop('PYTHONOPTIMIZE',None)
    flags = [mode] if mode != 'PYTHONOPTIMIZE' else []
    if mode == 'PYTHONOPTIMIZE': env['PYTHONOPTIMIZE'] = '1'
    target = tmp_path/'must_not_exist.jsonl'
    result = subprocess.run([sys.executable,*flags,str(RUNNER),'--output',str(target)],
                            cwd=ROOT,env=env,capture_output=True,text=True)
    assert result.returncode != 0
    assert 'optimized Python mode is prohibited' in result.stderr
    assert 'arguments are required' not in result.stderr
    assert not target.exists()


def test_dev_pi_bounds_unrelated_values():
    # Deliberately not the registered interval, weight or objective.
    assert parse_pi_bounds('[pi-2/7,pi+3/8]') == [math.pi-2/7,math.pi+3/8]
    assert parse_pi_bounds('[ pi + 1/9 , pi + 4/9 ]') == [math.pi+1/9,math.pi+4/9]


@pytest.mark.parametrize('value',[
    None, [1,3], '[-2,3]', '[pi-2/0,pi+3/8]', '[pi+3/8,pi-2/7]',
    '[pi+2/7,pi+2/7]', '[pi-NaN,pi+Infinity]',
    '[pi-2/7,pi+3/8] trailing', '[pi-2/7,pi+3/8+1]',
    "[__import__('os').getcwd(),pi+3/8]", '[pi-2/7,pi+3/8' , 'x'*129,
])
def test_dev_pi_bounds_reject_unsupported_or_inverted_inputs(value):
    with pytest.raises(ValueError): parse_pi_bounds(value)


def valid_status(signer, primary=None):
    fields = f'[GNUPG:] VALIDSIG {signer} 2026-01-01 1 0 4 0 1 10 00'
    return (fields + ('' if primary is None else ' '+primary) + '\n').encode()


@pytest.mark.parametrize('include_primary',[False,True])
def test_dev_expected_fingerprint_accepted(include_primary):
    runner=load_runner()
    runner.verify_expected_signer(valid_status(runner.EXPECTED_SIGNER,
                                              runner.EXPECTED_SIGNER if include_primary else None))


@pytest.mark.parametrize('kind',['wrong','wrong_primary','missing','malformed','multiple'])
def test_dev_signer_status_fails_closed(kind):
    runner=load_runner(); expected=runner.EXPECTED_SIGNER
    value={'wrong':valid_status('A'*40),
           'wrong_primary':valid_status(expected,'B'*40),
           'missing':b'[GNUPG:] GOODSIG DEV\n',
           'malformed':b'[GNUPG:] VALIDSIG short\n',
           'multiple':valid_status(expected)*2}[kind]
    with pytest.raises(ValueError): runner.verify_expected_signer(value)


def test_dev_runner_connects_verified_signature_to_exact_signer(monkeypatch):
    runner=load_runner(); commit='c'*40; calls=[]
    def fake_git(*args):
        calls.append(args)
        if args==('rev-parse','HEAD'): return (commit+'\n').encode()
        if args==('branch','--show-current'): return b'hebrew-projection-capacity-v0.9\n'
        if args==('merge-base','--is-ancestor',runner.BASE,commit): return b''
        if args==('verify-commit','--raw',commit): return valid_status('E'*40)
        raise AssertionError('DEV guard crossed signature gate')
    monkeypatch.setattr(runner,'git',fake_git)
    with pytest.raises(ValueError,match='expected freeze-signer fingerprint'):
        runner.verify_boundary(commit)
    assert calls[-1]==('verify-commit','--raw',commit)


def test_dev_invalid_signature_exit_propagates(monkeypatch):
    runner=load_runner(); commit='d'*40
    def fake_git(*args):
        if args==('rev-parse','HEAD'): return commit.encode()
        if args==('branch','--show-current'): return b'hebrew-projection-capacity-v0.9'
        if args[0]=='merge-base': return b''
        raise subprocess.CalledProcessError(1,['git',*args])
    monkeypatch.setattr(runner,'git',fake_git)
    with pytest.raises(subprocess.CalledProcessError): runner.verify_boundary(commit)
