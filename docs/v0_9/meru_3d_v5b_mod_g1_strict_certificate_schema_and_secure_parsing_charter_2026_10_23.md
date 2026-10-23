# Meru v0.9 / 3D-V5B — MOD-G1 Strict Certificate Schema and Secure Parsing Qualification Charter

**Document date:** 23 October 2026  
**Charter:** `MERU_V5B_MOD_G1_C0_2026_10_23`  
**Document status before owner signature:** HUMAN-APPROVED SIGNING CANDIDATE — NO EXECUTION AUTHORISED  
**Effect only after exact one-file signed publication:** prospective MOD-G1 authority; execution still requires distinct owner authorisation  
**Repository / branch:** `salahealer9/meru-geometry-audit` / `hebrew-projection-capacity-v0.9`  
**Exact proposed file:** `docs/v0_9/meru_3d_v5b_mod_g1_strict_certificate_schema_and_secure_parsing_charter_2026_10_23.md`  
**Required *direct* signed parent:** `4bbfe8bb5302aa33f2a44ad3220e05ed6d69fdb0`, the MOD-G0 scoped evidence seal and administrative F01 closeout  
**Expected human GPG fingerprint:** `D4EC014EEFCC90E619D2AA59A91239ABCF512130`

## 0. Authority, independence and exact question

This charter is the first MOD-G1-specific instrument under the signed modular qualification framework `5de3a2bac49e4cacbe49512f5674ead036c16091` and the signed original MOD-G0 charter `e8fb37660b78065537be06f561ad7208cd0fb0f6`. The exact new parent `4bbfe8bb5302aa33f2a44ad3220e05ed6d69fdb0` seals *only* the tested 17-archive G0/F01 verifier/provenance subclaim; broader MOD-G0 is `MOD_G0_INCOMPLETE` where historical archive bytes or other evidence are absent. This charter **does not reinterpret that as a whole-gate G0 PASS**. MOD-G1 may inspect already authenticated DEV-R1 and QC-R2 inputs within that sealed scope; if it actually depends on an unobserved CP_R1_0–5 byte object, that subtest is `INCOMPLETE` until original bytes are authenticated, never assumed PASS.

**Single G1 question:** Does a versioned, synthetic/generic V5B certificate validation and symbolic-input parsing boundary reject malformed, nonfinite, omitted, cross-inconsistent, resealed or potentially unsafe input **without producing a positive certification outcome**, while continuing to accept genuinely valid canonical generic certificate records? Specifically address the historical **R2-F02 confirmed forged-record acceptance** and **R2-F06 unresolved static `eval` parser concern**. A secure parser means an explicit finite, declarative accepted grammar, not reliance on empty `__builtins__` to make Python `eval` safe.

**Roles from the outset:** **Astra is the sole developer** of a new versioned G1 candidate and cannot independently approve its own implementation. **ChatGPT (GPT-6) is the independent technical reviewer**, required to construct and seal an independent oracle and expectation register before seeing Astra's G1 candidate changes. The human owner approves, signs, separately authorises each execution and alone decides any scoped gate seal. No other agent is required or authorised. The reviewer cannot modify candidate source or sign on the owner's behalf. Any prior exposure to original/historical code and findings must be disclosed; prospective independence concerns the **new candidate and reviewer oracle**.

Neither signing nor publishing this charter authorises Astra execution, ChatGPT review execution, a MOD-G1 seal, MOD-G2–G6, implementation freeze, or scientific `RUN_01`.

## 1. Immutable signed ancestry and source inputs

| Historical authority | Signed commit | Scope |
|---|---|---|
| V5B scientific protocol | `006b12e6800b29e41dc8e1854acdee528b822e22` | Unchanged science/budgets |
| DEV-R1 correction protocol | `54bdb1f6baab62fbf7be8b6057d2761a3286053d` | Historical generic implementation |
| DEV-R1/QC-R2 negative closeout | `e1da15b18ecaa4da2a0d15eed3d2864f1d6ea11b` | 29 scoped PASS, 8 FAIL, 5 INCOMPLETE |
| Modular framework | `5de3a2bac49e4cacbe49512f5674ead036c16091` | Gate/reviewer/seal rules |
| MOD-G0 charter | `e8fb37660b78065537be06f561ad7208cd0fb0f6` | Provenance/host reports |
| G0-C original negative closeout | `8d8eb31c7f3f4f6e9b1a603bbfa8e87b6d88c52f` | Historical `MOD_G0_FAIL` |
| F01 corrective preregistration | `a72a9515830aed6ab9b162b55cd421a51d953224` | Corrected G0 archive verifier |
| R01 reviewer amendment | `dc281f366d3d92d6e73bc90f0c695c0a20055cf3` | Astra developer / ChatGPT reviewer prospective allocation |
| G0-F01 scoped evidence seal | **`4bbfe8bb5302aa33f2a44ad3220e05ed6d69fdb0`** | **Exact required parent; narrow seal only** |

The **primary G1 developer baseline** is the immutable `MERU_3D_V5B_DEV_R1_GENERIC_CORRECTIONS_2026-10-23.zip`, **32,785,685 bytes**, SHA-256 **`2748cf262adda4d8fca8930056ebfe68be61cd33b20cbd8f7ddbb8f10a8912b6`**. The independent historical QC-R2 container is `MERU_V5B_DEV_R1_QC_PREFLIGHT_R2_INCOMPLETE_2026-10-23.zip`, **198,501,765 bytes**, SHA-256 **`64b48bd1b68f2a0ca9fa29247ec353009af521dcfc0b6e9b58820560070a4ef9`**. It contains the DEV-R1 bytes but must not be treated as a positive historical certificate.

The following verified **relative paths within the DEV-R1 ZIP** refer to the archived `source_DEV_R1/` tree (which itself resides below the ZIP's versioned root). Every execution must authenticate exact members before use:

| Source preimage | SHA-256 | Observed bytes |
|---|---|---:|
| `source_DEV_R1/src/v5b_generic/validate.py` | `8fb2483baf8a74d8c80f21ab2cd4e72c3112c39b69b1f4ef8f94cf7cb619026f` | 34,937 |
| `source_DEV_R1/src/v5b_generic/engine.py` | `02d50d96399ebacd5184f61cf297d98d55a80214458ac40fba5eaf23a709e364` | 43,441 |
| `source_DEV_R1/src/v5b_generic/records.py` | `c277f7710307eb8c057d2328b234e645fcc70cce4be22b084c08e77a31e1bd03` | 3,570 |
| `source_DEV_R1/src/v5b_generic/serialize.py` | `94d9d52de75f262fdc568685a7f31058b190df8407f592fd2f35dd56a54bd939` | 3,379 |
| `r1/replay_checker/v5b_r1_replay_check.py` | `b30c4675ba58f8cada491f52d5b6a07961d331d3347a895aaa1cb5d6a83cb1d2` | 51,677 |

The historical QC-R2 report `QC_R2_FINAL_REPORT.md` in the QC-R2 ZIP is **10,407 bytes**, SHA-256 `aa83be144274b936d2bb16d63ae5a6226a9744e84a9c96f531b845d7c05fe58b`. The independent `QC_R2_FINDINGS.json` is **1,736 bytes**, SHA-256 `b6046c655825443e58a58fa9126a7dc4d7b7e867223240979cf6a0fee6e9e5b7`. Two actual historical resealed-forgery fixture objects, relative to the QC-R2 ZIP, are pinned:

| Immutable hostile input | SHA-256 | Bytes |
|---|---|---:|
| `results/forged_nan_cpu.json` | `5af02ceaa7c2aaf6b5ffef49af61eb59394d748599cff2f8e6cb051447f87034` | 670,649 |
| `results/forged_missing_exec.json` | `140de05a726e48fd2e9c0587dd09f831cf2db76082fa2d12c257f58e0705d994` | 670,339 |

**Source fact versus inference:** Historical `R2-F02` was **CONFIRMED** by the independent reviewer: the production ledger validator accepted a NaN CPU string and a removed pair execution list, each with resealed root hashes. `R2-F06` was a **static concern**, not an observed exploit: `engine.py` around line 196 and the standalone replay checker around line 290 use `eval` with empty builtins and an explicit namespace, without an AST grammar allowlist. Do **not** claim an exploitation event occurred. The prior `R2-F01` unsigned +0.25 CPU ceiling allowance is a separate **MOD-G2** finding, not fixed or accepted by G1; G1 nevertheless must reject *nonfinite or malformed accounting fields* as a schema property.

Independently authenticate Git objects, direct parents, exact blobs, ZIP outer hashes/lengths, safety of archive members, relevant member hashes, and accessible prerequisite evidence. Differentiate GitHub signature attestations, locally verified cryptographic signatures and the owner's *separately observed* `[ultimate]` trust. Original QC negatives and absent R2-F05 logs remain immutable.

## 2. Exact G1 source surface and limits

**Permitted new derivative candidate only:** narrowly modify or version the production *certificate input validation* and *expression parsing* entry points corresponding to the pinned `validate.py`, `records.py`, `serialize.py` and `engine.eval_srepr`, plus the isolated replay checker parser for **syntax acceptance consistency**, as necessary to eliminate G1 vulnerabilities. Astra must provide an exact diff against the authenticated preimages, SHA-256 for every derived file, and a machine-readable source/dependency map. No mutation of frozen source ZIPs, historical manifests, evidence logs, protocol files or the signed scientific branch is authorised. All candidate work occurs in a separate scratch tree; **NO GIT COMMIT / PUSH by agents**.

The schema contract must define, version and reject on ambiguous record representations: typed finite nonnegative CPU and budget quantities; required view/pair/execution/attempt/worker identities; consistency of attempt references and mandatory execution arrays; valid object/camera/branch/precision binding and hash-chain crosslinks; required fields with no implicit safe defaults; and canonical interpretation of JSON (including duplicates, noncanonical numbers and unapproved extra fields). A valid root hash alone is not sufficient for acceptance. Treat JSON bool, null, `NaN`, infinities, negative values, numeric strings masquerading as typed numbers and overflow as adversaries under an explicit canonical-number policy. For existing legitimate string representations, define a strict, versioned decimal/rational grammar first, and reject nonfinite or syntactically inconsistent instances; do not silently break genuine records without a compatibility report.

**Symbolic parser:** specify a *closed, positively enumerated* `ast.parse(..., mode='eval')` grammar before implementing it, permitting only exact constructor calls and literal atoms actually required by the authenticated generic record language. A source-anchored grammar may include approved arithmetic/SymPy constructors and exact rational/symbol representations; these must be enumerated and type-/arity-checked in a `G1_PARSER_GRAMMAR.json`. Reject attribute access, subscripting, comprehensions, lambdas, f-strings, arbitrary binary Python evaluation, dunder names, dynamic attribute traversal, arbitrary calls/keywords, unsafe literals, unsupported constructors and oversized/deep inputs. Neither an empty-builtin `eval` nor a generic `sympify` on attacker-controlled strings is an acceptable replacement. Use explicit recursive evaluation of the validated constructor AST or an equivalent audited finite interpreter; never execute hostile user text as Python.

Keep the signed scientific 30 CPU-second view, 45 CPU-second pair, 6,000 CPU-second total, 4 GiB RSS and 2-hour registered-run limits exactly unchanged. G1 may check field finiteness, type and identity but **must not declare exact cumulative charged-CPU enforcement or provenance qualification**; those are MOD-G2/G5. G1 may test consistency of mandatory event *structure*, but not claim complete success/failure trace reconstruction (MOD-G3), exact symbolic theorem soundness (MOD-G4), or integrated production qualification (MOD-G6).

## 3. Frozen negative/positive acceptance matrix

The following signed *classes* and required outcomes are fixed now. Developer must make a content-hashed, independently retrievable **exact fixture/expectation register at D-CP0 before editing code**; any discovered cases after that freeze are explicitly exploratory. Reviewer separately seals its own oracle and expected outcomes at Q-CP0 **before inspecting Astra's new G1 source changes or developer test details**. Fixtures must be inert: no malicious command execution is necessary to verify parser refusal.

| ID | Required independent adversary/positive class | Required behavioural result |
|---|---|---|
| G1-N01 | Exact historic resealed `forged_nan_cpu.json` | Refuse certification; explicit finite/accounting reason |
| G1-N02 | Exact historic resealed `forged_missing_exec.json` | Refuse certification; explicit missing execution evidence reason |
| G1-N03 | `NaN`, ±`Infinity`, malformed decimal/rational, numeric-type confusion, negative and overflow cases in view and pair budgets | Refuse under typed finite schema; no silent zero/default coercion |
| G1-N04 | Entire pair `executions` array absent, null, wrong-type, empty where attempts require it, or one required worker attempt omitted; recompute/reseal hashes | Refuse with missing/inconsistent execution reason |
| G1-N05 | Duplicate attempt/worker identifiers, unbound attempt-to-event links, contradictory status/precision/branch/camera and missing required attempt references | Refuse false crosslinks; no synthetic missing histories |
| G1-N06 | Duplicate JSON keys, trailing non-JSON tokens, malformed nesting, noncanonical numeric encodings or unsupported extra keys | Reject ambiguous/noncanonical input or explicitly versioned noncanonical representation before hashing; never silently choose one duplicate field |
| G1-N07 | Wrong object/source/camera/branch/precision binding, inconsistent nested hash, resealed outer/root hash with invalid inner references | Reject despite resealing |
| G1-N08 | Python parser AST constructs: attribute/subscript/dunder, lambda, comprehension, f-string, import-like or unconstrained calls, keyword/splat, arbitrary expression operators | Reject before interpretation; no executable effect |
| G1-N09 | Unknown symbolic constructors; incorrect arg count/type; excessive AST nesting, input length or coefficient size | Fail closed / `UNKNOWN` or explicit unsupported, not positive proof; bounded execution |
| G1-N10 | Equivalent hostile strings submitted to both available parsing entry points | Both fail closed; no unsafe legacy `eval` fallback |
| G1-N11 | Missing expected worker list in a valid-looking record; selected execution with invalid/nonfinite budget but valid matching hashes | Refuse; do not infer provenance from hashes |
| G1-P01 | Authentic canonical generic view/pair/object certificate records selected by exact hash from the DEV-R1 archive and frozen in D-CP0 | Preserve correct parsing and acceptance for records whose *G1 schema premises* are valid |
| G1-P02 | Real source-anchored valid symbolic serialized forms and approved exact constructors, including nested ones within the agreed grammar | Parse into correct exact typed symbols/expressions; no value drift |
| G1-P03 | Valid complete execution lists, declared typed finite values, consistent links and correct signed record hashes | G1 schema accepts, without claiming G2/G3/G4/G5 completion |
| G1-P04 | Missing/badly formed inputs have reproducible, explicit error classifications, not uncaught tracebacks, truncated log loss or acceptance | Fail-closed diagnostics and raw run evidence |

Additional adversarial variations on the same fixed classes are allowed if identified as **exploratory**. Require at least one independently resealed hostile fixture per relevant negative class where root hashes are relevant; the reviewer may add novel inert attacks. Keep accepted genuine records and rejected hostile examples as *distinct semantic cohorts*, not a single percentage score. No unauthorised threshold relaxation to make an existing example pass. If the legacy record syntax and desired strict policy conflict, report a **blocking compatibility question**, not a silent schema rewrite or deletion of valid records.

### Specific boundary checks

1. The historical NaN fixture must no longer be accepted, irrespective of whether the parser receives JSON numeric nonfinite tokens or strings subsequently converted to floats.
2. Every required unsuccessful, unresolved or pre-empted attempt must have a structurally checkable worker/execution reference **if the signed record class requires one**; the G1 validator must refuse missing structure. Whether all historical *full contents* of those attempts were actually preserved is reserved to G3.
3. A syntactically well-formed malicious Python-looking symbolic string may not be interpreted via Python `eval`. Retain a static code-path audit of production and standalone checkers; the absence of an observed exploit in old R2 cannot be presented as a demonstrated bypass of their sandbox.
4. Exact 30/45 CPU ceiling comparisons and removal of the historical `+0.25` allowance are **G2**, not a reason to call G1 failed merely because those thresholds are not yet qualified. A G1 PASS must still refuse NaN or structurally forged CPU fields.
5. Maintain every old F01/G0 evidence boundary: no change to authenticated archive checker, no reopening the G0-C failure record, no inference that all historical checkpoints are available.

## 4. Two-role qualification procedure; independently reviewable evidence

**Developer (Astra; a future distinct owner-authorised execution):** authenticate complete signed G1/G0/V5B ancestry and original input bytes; create D-CP0 with original-source pinning, full **sealed grammar**, expectation/fixture register, development boundary and lossless receipt before editing; derive narrowly scoped G1 versioned source and exact diff; execute bounded benign/generic suites with raw stdout/stderr/exit codes, including failed attempts; preserve D-CP1 after changed source and initial tests; preserve D-CP2 final package, complete audit, source and dependency maps and independently retrievable original raw evidence. Developer may deliver `MOD_G1_DEVELOPER_CANDIDATE_READY_FOR_INDEPENDENT_QC` with explicit deviations, but cannot issue PASS/SEALED.

**Independent reviewer (ChatGPT; a later separate owner-authorised execution):** verify exact candidate/root/ancestry and historical bytes; before seeing candidate changes, seal own Q-CP0 oracle and expectation register with distinct test recipes and hash; independently audit parser semantics and candidate source diff; run isolated inert hostile inputs and legitimate bounded fixtures; preserve exact results, exceptions and attempted failures; rerun the precise historic two forged-record examples; verify code-path closure including the standalone checker; produce Q-CP1, Q-CP2 and exact dependency/status matrix. Reviewer may report `MOD_G1_PASS_SCOPE_LIMITED`, `MOD_G1_FAIL`, `MOD_G1_INCOMPLETE`, `MOD_G1_BLOCKED`, or `MOD_G1_EVIDENCE_LOSS_STOP`. Reviewer's PASS is **not** a human-signed seal. Any reviewer-discovered *substantive* defect remains a finding; reviewer does not fix producer source or silently change its expectations.

**Admission criterion for scope-limited G1 PASS:** all applicable historical R2-F02 forged inputs and all mandatory G1-N01–N11 fail closed for the *version-pinned actual candidate*; all applicable G1-P01–P04 legitimate cases work under a documented finite grammar; no old unrestricted string-evaluation path remains reachable for the claimed input boundary; full raw evidence, independently reproducible oracle and checkpoints are authenticated; and any unsupported record types or missing evidence are separately labelled. Refusal behaviour and type/schema safety are the only admitted claims. No majority vote can override a critical negative acceptance failure, but first-error-message order is **not** binding unless a signed test explicitly says so: preserve all causal required reasons.

Review dependence on G0 is **exact-ID limited**. New reviewer environmental facts do not magically qualify any production host. Missing original DEV-R1 CP_R1_0–5 and unrecoverable R2-F05 logs do not automatically fail an independently exercised, version-pinned G1 parser claim when no required G1 input depends on them; the gaps must remain visible and block any claim that does depend on those original bytes.

## 5. Resources, preservation, interruption and stop guards

**New prospective maximum only, effective solely on separate authorisations:** one **90-minute wall-clock Astra developer slice** and one **60-minute wall-clock ChatGPT independent review slice**; no automatic rollover, extra agent, unbounded retries or grant of G2/G3/G4/G5/G6 authority. The longer single slices are deliberate to minimise repeated handoffs and lost-work interruptions. Each agent records observed UTC start/stop, actual duration, and limitations in stopwatch or CPU measurement. If a session cannot reliably enforce the administrative wall-clock bound, it must report that fact and stop conservatively; it must not falsely claim a hard host timer. No expensive scientific computations, resource-exhaustion attacks, or 30/45/4-GiB enforcement stress are permitted. Test input-size/depth refusal with small bounded synthetic samples, not denial-of-service payloads.

**Durable storage first.** Before substantive work, verify access to a separately persistent, retrievable artifact destination; independently upload/download/read back D-CP0 or Q-CP0 **before** changing or viewing candidate source respectively. **D-CP0 → D-CP1 → D-CP2** and **Q-CP0 → Q-CP1 → Q-CP2** are append-only with exact SHA-256 and byte count, all member hashes, predecessor identity, UTC timestamp, output version, original raw attempts/logs, exit codes and separate fresh readback receipts. A final release must be freshly recovered from that destination and completely verified (not just reported uploaded). No hidden in-memory-only checkpoint counts. If durable storage, underlying bytes, credits, tool access or time fails, preserve an explicit early-stop checkpoint and report `BLOCKED`/`INCOMPLETE`/`EVIDENCE_LOSS_STOP` truthfully. Never fabricate missing stdout/stderr, unsuccessful trials or hashes.

Scientific repository baseline remains immutable. Agents may write only scratch derivatives and evidence packages, **NO COMMIT / NO PUSH**, no changes to the `g0a_verify_f01.py` sealed archive verifier or its contract, and no alterations to G0 historical statuses. Do not install packages into the production checkout; document actual Python, SymPy, FLINT/Arb and environment identities where material. No external code fetching without input-authentication and owner authority. Any host supports only the claims actually checked there.

## 6. Exact exclusions and human seal decision

**NOT AUTHORISED:** changes to V5B scientific protocol or the 30/45/6,000 CPU, 4 GiB, two-hour limits; treating R2-F01, R2-F03, R2-F04, R2-F05 or G0 missing originals as resolved; mathematical kernel proofs (G4); hard process containment (G5); integrated validation (G6); registered six spherical surrogates, Hebrew/glyph/image/ribbon/target tests, historical FIRST HAND reconstruction, implementation freeze, or `RUN_01`. Signing a MOD-G1 PASS does not qualify science or bridge these outstanding modules.

After the independent review, the owner may inspect the complete evidence and choose whether to sign an additional **one-file MOD-G1 scope-limited gate-seal**. The exact input hashes, accepted/rejected record language, independent test coverage, environment assumptions, remaining negative evidence and unsealed dependencies must be enumerated. Signing any future G1 seal creates no automatic authority to execute G2 or any other gate. If a critical security/schema acceptance requirement fails or a required original is unavailable, no whole critical G1 subclaim seal may be issued; preserve a limited positive inventory or incomplete status instead.

## 7. Human signing guard — no agent publication

This charter is approved in substance by the owner in the conversation; its **exact bytes** become binding only after the owner obtains the final document, verifies its SHA-256, confirms a clean local branch and fresh matching remote branch tip at direct parent `4bbfe8bb5302aa33f2a44ad3220e05ed6d69fdb0`, and personally signs **exactly this one new documentation file** with the pinned fingerprint. Verify the preceding signature, new signed commit's direct parent, exact Git blob/file bytes and one-file tree diff; ordinary push only. A branch-parent mismatch means **STOP**; never force, reset or rebase to make this plan fit. Markdown's intentional two-space line endings must not be accidentally removed by a whitespace fixer. Owner local `TRUST_ULTIMATE` is separately observed from GitHub attestation and the reviewer's keyring.

**Consequence of signing and publishing:** `MOD-G1-C0 CHARTER SIGNED — DEVELOPMENT AND REVIEW EXECUTION NOT YET AUTHORISED`. Only a new explicit owner instruction may admit Astra's bounded development slice; only a separate later instruction may admit ChatGPT's independent review. An eventual gate seal remains a third distinct human decision.
