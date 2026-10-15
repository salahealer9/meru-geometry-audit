# Execution transcript and command inventory

All paths are from the execution host. Full command observations and checks are
in preflight.json, signature_setup.json, runner_attempt.json,
runner_completion.json and postrun_checks.json. No scientific module is invoked
by the preflight/postprocessing checks. Commands below are a record, not a rerun
instruction. The raw designated JSONL path now exists and must not be reused.

## Initial read and workspace inspection

Working directory `/workspace/scratch/255e4cd6766b`:

```bash
cat 'upload/P0A0_REGISTERED_SYNTHETIC_EXECUTION_AGENT_HANDOFF(2).txt'
```

In the earlier `/workspace/scratch/255e4cd6766b/meru-geometry-audit` checkout:

```bash
git status --porcelain
git branch --show-current
git rev-parse HEAD
git remote -v
```

Observed preregistration HEAD and prior untracked implementation work. No reset,
checkout switch, commit or removal was applied there. A separate checkout was
established with the handoff-authorized command:

```bash
test ! -e p0a0_registered_pilot_once.jsonl && test ! -e meru-geometry-audit-pilot && git clone --branch hebrew-projection-capacity-v0.9 --single-branch https://github.com/salahealer9/meru-geometry-audit.git meru-geometry-audit-pilot
```

Clone exit 0; exact expected implementation HEAD and branch, no checkout change
needed. Complete protocol and implementation specification/source were read
with `cat` from this GitHub checkout. Required paths and hashes are in the ledger.

## Signature setup and non-evaluating preflight

The initial `git verify-commit --raw HEAD` reported NO_PUBKEY. Public-key setup
used the previously retrieved file and checked its primary fingerprint first:

```bash
gpg --show-keys --with-colons salahealer9-public.gpg
gpg --import salahealer9-public.gpg
```

Then, in the clean execution checkout:

```bash
git verify-commit --raw d15865167b4e3c454e398bd498d9d681103096f7
git verify-commit --raw 24c00fc44e4d9d57adacd1e636e9e2d20d86a954
```

Both verification commands returned 0 with the exact required signing/primary
fingerprint. The machine status record omits human UID/email lines.

A read-only Python preflight script invoked the Git commands listed with actual
outputs in preflight.json: status, branch, HEAD, both parents, upstream, ancestry,
protocol hash-object and unchanged-protocol diff, tracked and staged diffs and
tracked-path inventory. For every manifest entry it read the local file, computed
`hashlib.sha256`, checked the byte count, and compared the bytes with
`git show FREEZE_COMMIT:PATH`; `git rev-parse FREEZE_COMMIT:PATH` supplied blob IDs.
It parsed the two A09 CSV rows as text, recorded absence of the raw file, checked
output-path nonexistence, and inspected Python flags/package versions. Only NumPy,
SciPy and scipy.optimize.minimize_scalar were imported to confirm numerical
runtime availability. No registered fixture or case module was imported.

Formal preflight status: PASS. No registered evaluations before the run.

## Single registered invocation

Working directory `/workspace/scratch/255e4cd6766b/meru-geometry-audit-pilot`:

```bash
python scripts/p0a0_registered_pilot.py \
  --freeze-commit 24c00fc44e4d9d57adacd1e636e9e2d20d86a954 \
  --authorized-synthetic-run \
  --output ../p0a0_registered_pilot_once.jsonl
```

The unchanged runner was invoked as a subprocess once. An external exclusive
attempt record was created before invocation; stdout/stderr were captured to
separate files without filtering. Return code 0; zero bytes in both streams.
Start/end UTC and exact argv are in runner_completion.json. Attempts 1; retries 0.

## Read-only postprocessing

The original JSONL was read as bytes, SHA-256 hashed and parsed; case IDs,
order, count, fields and states were checked. Git status/diffs, HEAD, protocol
blob and all manifest artifact hashes were checked again. No registered function
was called after the runner exited. The original JSONL was not rewritten.
Case-matrix values were copied/formatted from existing JSON records. Report prose
interprets these bounded observations and the frozen code, not a second numerical
experiment. No historical test suite was repeated.

The ZIP includes the original raw JSONL byte-for-byte and only generated textual
QC evidence plus reference metadata. SHA256SUMS lists each payload file. The
outer ZIP checksum is supplied separately, avoiding a self-checksum cycle.
