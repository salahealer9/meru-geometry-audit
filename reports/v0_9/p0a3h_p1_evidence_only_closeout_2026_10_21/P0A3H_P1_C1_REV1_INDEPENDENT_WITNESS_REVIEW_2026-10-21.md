# P0A3H-P1-C1-REV1 — Independent static review and execution-witness decision

**Date:** 2026-10-21 (UTC review lane). **Reviewer role:** separate read-only artifact/source reviewer; not the author of Claude's portable derivative or driver. This is a static witness assessment, **not** a human release, code attestation, P01–P06 execution, or third-party host observation.

## Disposition

**`P0A3H_P1_C1_REV1_INDEPENDENT_ARCHIVE_SOURCE_QC_PASS`** and **`P0A3H_P1_C1_REV1_PREEXECUTION_WITNESS_WITHHELD_W01`**.

The checksum/source archive is independently qualified *within static scope*. **Do not issue the SHA-specific human execution release.** The signed P1 protocol retains an enforceable **16,777,216-byte whole-attempt disk cap** and states that if mandatory Linux containment cannot enforce a limit, the result must be `ENVIRONMENT_UNQUALIFIED`, not PASS. The REV1 driver's periodic directory sampling does not prove compliance with this cap at all instants. The portable mathematical derivative and experimental fixtures remain unchanged, so the blocker is restricted to execution-harness control and host qualification.

## Original identities, checked from uploaded bytes

| Artifact | Observed fact |
|---|---|
| Original C1 | 308,794 B; SHA-256 `0ab255773debd5a68c21fa2555c954b347971d28902ee345beb1f254d02013d4`; ZIP CRC, SHA256SUMS and inventory valid |
| Proposed C1-REV1 | 376,773 B; SHA-256 `733352e73b23f97423965407b39121fc7baae47332a7fa7386aa46fca7c2bbeb`; 158 unique ZIP entries, 157 sums, 156 inventory entries; CRC PASS |
| REV1 base64 | SHA-256 `cc18c51cad19694296050bee2a8166f17564783d3e15c348b36df7162ce206cc`; decodes byte-identically to original REV1 ZIP |
| Reference 51-file source | Identical to original `SOURCE_LOCK.json` SHA-256 `abff7aa8df19f73e070d9f06ebd23334f8d98b45c1736d38399b845c69835902` |
| Derivative 51-file candidate | `P1_CANDIDATE_LOCK.json` SHA-256 `18c7d153e236560e0e99738f50137f46bb1dae94beaf125340835dadacaf106e`; exact three A1-permitted source modifications |
| Mathematical kernels | 3/3 preserved: `algebra.py` SHA-256 `44206584…e6d2d`; `core.py` `37701d03…dd420`; reference `arithmetic.py` `72b3c37f…e6d2` |
| External tools | 23/23 locked; new `P1_EXTERNAL_LOCK.json` SHA-256 `b1ea930862758c32dea23932b8114de043e4a93b97ca4401c7e53efacdfab2c5` |
| Unchanged from original C1 | Both candidate trees; P1 candidate/source locks; C0/authority files; derivative ledger/diff; test fixtures; P05 comparator bytes |
| Original withheld review | Preserved byte-identically inside REV1 `history/original_C1_witness_review/`; original C1 receipt preserved byte-identically |
| Independent read-only audit | **56/56 static checks PASS**; Python source AST-parsed, no candidate/driver/verifier/test imported or invoked |

The machine-readable P01–P06 expected-outcome lock retains every original case field and value (all six), adding extra checks only, and preserves the original scientific case order.

Comparison of archived content found **12 changed payload members**, **9 added payload members**, and **no removals**. The provided change-ledger enumerates changed and added ordinary payload members but necessarily omits its own JSON and diff under `ledger/`; the independent audit accounts for this self-reference exception. Signed P1 and A1 texts in the archive are treated as authenticated historical source documents by previously recorded signatures; the present review did not re-perform local GPG key-ownertrust validation.

## W01 — Aggregate storage constraint: BLOCKING

Source: signed `authority/P1_SIGNED_PROTOCOL_4c1634e6.md`, resource contract §3 (line containing `whole attempt disk ≤16 MiB`) and environment rule (`If Linux containment cannot enforce a mandatory limit, report ENVIRONMENT_UNQUALIFIED, not PASS`). The following are observed from **`p1_external/P1_DRIVER.py` in the uploaded REV1 original**, numbered from line 1:

1. **Sampling rather than reservation:** `sample()` and `measure()` enumerate current directory entries at lines **87–122**; the runner loop samples approximately once every **0.2 seconds** at lines **303–337**. A process can write enough data to exceed 16 MiB and delete it between observations. The next sample then sees no excess. Therefore the source-comment statement that *any* transient overrun is *always* caught at the next sample (lines **34–35**) is **not justified**. The design can detect sustained observed overages, not guarantee the whole-attempt high-water limit.
2. **Per-file limit is not aggregate containment:** line **46** sets `RLIMIT_FSIZE=16 MiB`. Multiple smaller files can cumulatively exceed 16 MiB; periodic tree measurement remains the only aggregate check. A 32 MiB free-space prerequisite (lines **67–69**) is a free-capacity gate, not a 16 MiB quota.
3. **Out-of-tree transient files:** the driver declares signature temporary directories under `/tmp` (lines **25–37**) and `sig_residue()` only lists names before and after each case (lines **125–132**, **361**, **376**). It does not account for temporary file sizes or high-water storage while those files exist. A `--work`-only limit is not a proven bound for **all attempt-created bytes**.
4. **Post-final unmeasured writes:** `finish()` samples at line **151**, then writes `P1_ATTEMPT_SUMMARY.json`, the final journal and `P1_ATTEMPT_FILE_MANIFEST.json` at lines **155–159**. It does not remeasure afterward. Thus even the final on-disk state is not strictly covered by the last success-contingent sample.
5. **Process termination after detection:** `kill_tree()` at lines **273–300** is a best-effort enumeration of currently visible PIDs. It does not preempt filesystem writes or provide a kernel-enforced quota. This is a further limitation, not an allegation of malicious execution.

Consequently, **W01 is not closed under the exact registered interpretation**. No evidence is present of a dedicated, securely bounded 16 MiB storage container or quota on the operator's host. Merely calling observed sampling “enforcement” would alter the practical acceptance standard after registration.

### Distinct options (no authorization yet)

**Preferred:** qualify an operator-host storage mechanism that imposes a genuine aggregate allocation ceiling prospectively (for *all* process-created attempt files, including temporary files). Do a **read-only host feasibility assessment** first; do not assume that the operator has mount, quota, namespace or cgroup privileges. If a genuinely bounded layout is feasible, document host setup, exact permitted filesystem roots, hard failure semantics, independent recording of resource usage and source-lock ramifications in a **new separately named C1 revision**, still without candidate or case execution. Confirm that the host profile and source change are prospectively witnessed before any release.

**Alternative:** if a genuine containment mechanism is unavailable, the human may draft a **separately signed prospective amendment** explicitly changing the claim to monitored, sampled disk use (with stated unobserved high-water and `/tmp` exclusions). Such an amendment would **weaken** the old hard-cap assurance and must not be portrayed as satisfying the original absolute limit. No automatic approval is implied; the strict P1 protocol currently remains operative.

## W02 — Human release chronology: PARTIAL STATIC CONTROL IMPLEMENTED

`P1_DRIVER.py` lines **163–195** require the original C0 receipt, supplied REV1 receipt and human release text before archive extraction or first candidate launch; they preserve exact supplied bytes under `upstream/` and create `PRELAUNCH_RELEASE_RECEIPT.json`. The journal marks first candidate invocation only later (lines **361–365**). `P1_C2_PACKAGER.py` lines **35–61** checks matching copies and relative journal order and includes upstream originals in future C2. This materially addresses the original timing/inclusion issue.

**Residual:** the release-check logic uses substring membership `(RELEASE_FMT % REL) in cert_text` (driver line **177**, packager line **43**), not unambiguous exclusive parsing of an original signed human-authority document. The code itself candidly says it does **not** authenticate human origin. A separate actually human-issued and reviewer-relayed SHA-specific release remains mandatory; neither the received REV1 nor its receipt constitutes that release. The C2 provenance chronology is internally logged, not a third-party observation of host processes.

## W03 — New schema: ADDITIVE STATIC CHECKS PRESENT

`p1_external/p1_verifier.py` lines **147–191** provide a dedicated envelope conformance check with exact field set, canonical encoding, P1 lineage constants, SHA shapes and derivative file map. The verifier adds schema predicates for positive envelopes and checks that the historical N3 envelope *fails* the new lineage schema (later case-evaluation logic). The external validation schema and updated expected-outcome lock are source-locked. This supports the claimed structural addition **as static code inspection only**. Actual runtime interoperability has not been tested or validated.

## Other prospective limitations

- P02/P03/P04/P05/P06 have not executed. CPython 3.11/OpenSSL signature behaviour, 256 MiB worker memory, exact historical certificate equality, timeout evidence and live host isolation remain unresolved engineering questions.
- Claude prepared the original candidate and subsequent derivative/external machinery. Its own assertions of zero candidate/test runs and durable external register state are attestations; this review cannot independently prove no undisclosed execution.
- Release text, operator filesystem and `/proc` observations rely on the recorded **cooperative-host** model. No hostile-host or continuous loaded-code integrity is claimed.

## Required next action

Preserve the received original C1 and REV1 unchanged, along with this report. Request **static operator-host disk containment feasibility** and then a separately named prospective proposal, not a silent edit to REV1. Until the mandatory hard-limit question is resolved by valid registered authority, **do not issue `P0A3H-P1-C1 LOCK WITNESSED` for REV1 and do not run `P0A3H_P1_DEV_01`.** No Git modification or P0A4/H01–H07 action is authorized by this review.
