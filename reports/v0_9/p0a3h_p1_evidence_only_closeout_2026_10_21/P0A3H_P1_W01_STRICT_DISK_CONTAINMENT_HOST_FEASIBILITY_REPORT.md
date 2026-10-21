# P0A3H-P1 — W01 strict 16 MiB whole-attempt disk containment: static host-feasibility report

**Prepared:** 2026-10-21, about 22:30Z, by the engineering agent (Claude). This is read-only analysis. Nothing was installed, mounted, configured or executed on any host, and no probe was run in the agent's own container (that host is not the operator host and must not stand in for it).

**Inputs:**
- signed P1 §3 (strict cap; "If Linux containment cannot enforce a mandatory limit, report `ENVIRONMENT_UNQUALIFIED`");
- the original P1-C0 operator host register;
- the REV1 independent witness review (`caf4439b…`), read in full.

**Preserved unchanged and read-only:**
- original C1 `0ab25577…13d4` and REV1 `733352e7…bbeb`, each with its base64 copy and receipts;
- both withheld-witness bundles (`3dc0fe51…` and `caf4439b…`).

**Bottom line:**
- **For the current contract on the evidence available:** `ENVIRONMENT_UNQUALIFIED`. Nothing in the recorded host profile shows a kernel-enforced aggregate storage bound, and REV1's sampled design cannot provide one.
- **Prospectively, strict containment appears technically feasible without privilege escalation:** an unprivileged user and mount namespace whose only writable storage is one size-limited tmpfs, enforced by the kernel. It depends on host capabilities that are **not recorded** in C0, and those must first be established by a preregistered, witnessed, non-candidate host capability probe.
- **Both paths below require new human-signed authority** before any REV2 is built.

## 1. Acknowledgement of the REV1 review
The reviewer's W01 analysis is correct, and REV1 overstated its control in two places:
- **Write-and-delete between samples.** A process can write more than 16 MiB and delete it between two 0.2 s samples, and no later sample would see it. REV1's comment that every such exceedance "is always detected at the next sample" was **wrong**. Sampling detects only sustained overages; it cannot bound the high-water mark.
- **Other gaps the reviewer found:**
  - `RLIMIT_FSIZE` is a per-file limit;
  - the free-space gate is not a quota;
  - `/tmp` signature files were only listed by name, not sized;
  - `finish()` writes files after its last sample;
  - `kill_tree` acts after detection and does not stop writes in advance.

REV1 therefore does not meet the strict registered cap. It stays preserved as a withheld lock and must not be relabelled.

## 2. Kernel-enforced versus sampled controls

| Control | What it bounds | Kernel-enforced and pre-emptive? | Meets "whole attempt ≤ 16 MiB at all instants"? |
|---|---|---|---|
| Directory sampling (REV1) | Observed totals at sample times | No; measurement only | **No.** It misses transient high-water, and anything outside the tree. |
| `RLIMIT_FSIZE` | Size of one file per write | Yes, but per file only | No (no aggregate) |
| Free-space gate (`statvfs`) | Capacity available at the start | No | No |
| Candidate `run_disk_bytes` check | Each candidate run directory, at check points | No; the application checks it | No (per directory, sampled) |
| cgroup v2 `io` and `memory` controllers | I/O bandwidth; memory (tmpfs pages are charged to memory) | Yes, but not a storage quota | No: mixes process RAM with storage; `io` does not limit capacity |
| ext4/XFS user or project quotas; btrfs qgroups | Blocks per uid, project or subvolume | Yes | Could, but they need **root** to enable and set, and the filesystem must be mounted with quota support. Excluded (privileged). |
| Loop-mounted 16 MiB filesystem image | All blocks in that filesystem | Yes | Could, but loop setup and mounting need root. Excluded. |
| FUSE filesystem image (for example `fuse2fs`) | All blocks in the image | User-space filesystem enforcement | Needs a package install and `/dev/fuse` access. Excluded under the current constraints. |
| **tmpfs with `size=16m` mounted inside an unprivileged user+mount namespace** | **Every data page in that tmpfs; writes past the limit fail with `ENOSPC`** | **Yes: kernel-enforced and pre-emptive** | **Yes**, *provided* it is the attempt's **only** writable storage and all attempt paths, including `/tmp`, resolve into it (§3) |
| LD_PRELOAD write interposition | Library calls only | No | No |

## 3. Proposed strict design (static; for independent assessment; not implemented)
**Mechanism:** run the whole attempt inside a fresh **unprivileged user namespace plus a private mount namespace**. This is a standard kernel feature available to ordinary users when the host permits it. It involves no setuid helper and no host-wide change, and it does not affect the operator's real mounts.

1. **Entry.** The operator starts the outer launcher as an ordinary user, for example with util-linux `/usr/bin/unshare --user --map-root-user --mount --propagation private --fork` (path and SHA-256 pinned in a new host profile). It runs a pinned inner bootstrap. Python 3.11 has no `os.unshare` or `os.mount`, so the util-linux `unshare` and `mount` binaries are needed and must be pinned.
2. **Single bounded store.** Inside the namespace, mount `tmpfs` with `size=16777216,nr_inodes=<fixed, e.g. 8192>,mode=0700,nosuid,nodev,noexec` over an empty directory the operator owns, for example `~/p1_attempt_mnt`.
   - This tmpfs is the **whole attempt**. It holds the extracted C1 trees, the upstream receipts, journals, case directories, raw worker evidence, key directories, the runner `TMPDIR` and the final summary and manifest.
   - **Bind-mount a subdirectory of this same tmpfs over `/tmp`**, so the candidate workers' OpenSSL `p0a3g_sig_*` temporary directories (their environment is fixed by the frozen supervisor) are counted inside the same 16 MiB.
3. **No other writable storage.** Every other mount visible in the namespace is remounted bind/read-only, using the list in `/proc/self/mountinfo`: `/`, `/home`, `/run`, `/dev/shm`, `/var/tmp`, and any other writable mount. Any write outside the tmpfs then fails with `EROFS`. **If any remount fails, the attempt stops as `ENVIRONMENT_UNQUALIFIED` before any candidate launch.**
   - Device nodes such as `/dev/null` stay usable on a read-only mount.
   - `/proc` and `/sys` are pseudo-filesystems and are not attempt storage.
   - The candidate and the external tools write only to run directories, `TMPDIR` and `/tmp`; this needs re-confirming statically for REV2.
4. **Failure semantics.**
   - Any write beyond 16 MiB fails **before** it happens (`ENOSPC`). The frozen candidate turns resulting `OSError`s into fail-closed states. The driver records the attempt as **FAIL `WHOLE_ATTEMPT_DISK_CAP_REACHED`**, never PASS.
   - No sampling is needed for the bound itself. Sampling of `statvfs` on the tmpfs (`f_blocks - f_bfree`) is kept only as **evidence** of usage, together with the kernel's own counters.
5. **Export after the attempt.**
   - After the final summary and manifest are written **inside** the tmpfs, the inner bootstrap streams a deterministic archive of the tmpfs tree to the outer launcher through an **already-open pipe**, so no filesystem write happens inside the namespace. The outer launcher stores it on persistent disk.
   - This export happens **after** the attempt ends. Its size is bounded by the tmpfs content, and it is the input to C2 packaging.
   - The namespace and tmpfs are then discarded.
6. **Recorded identity effects.**
   - Inside the namespace the process runs as uid 0 *mapped* to the operator's uid, and host-owned files appear owned by `nobody`.
   - The candidate does not check uid or ownership. Its `environment()` fingerprint (interpreter path, SHA-256, version, `platform.platform()`, flags, stdlib digests) is unaffected.
   - This needs re-confirming statically for REV2 and in the probe.
7. **Interaction with existing limits.** The worker caps and runner rlimits are unchanged. Workers may lower but never raise limits inside the userns. All three kernels and the three-file derivative are unchanged, so **no candidate-source change** is required. Only the external harness changes, plus a new host-profile addendum.

**Declared residuals of this design:**
- **Volatile storage.** If the machine loses power or crashes mid-attempt, tmpfs evidence is lost, and the attempt becomes INCOMPLETE with no retry permitted. This matters given the R1 evidence-loss history. It is the price of strict containment without root, and the reviewer must accept or reject it explicitly.
- **Unit of the cap.** The tmpfs cap counts allocated data pages, so the apparent sum of file sizes can exceed it only through sparse files. Combined with `RLIMIT_FSIZE`, that is not exploitable by the frozen candidate. Directory entries and inode metadata are bounded by `nr_inodes` rather than by `size`.
- **Accounting.** tmpfs pages are charged to the operator's memory cgroup. 16 MiB is negligible against the C0 environment.
- **Host trust.** The cooperative-host trust model is unchanged; this design gives no hostile-host isolation claim.

## 4. Host capabilities required (none of these is recorded in the authenticated P1-C0)
The C0 register records OS, kernel, binaries, libraries, `/proc/self` readability, rlimits and free space. It has **no** entries on user namespaces, mount permissions, AppArmor or seccomp policy, cgroups or container status.

The kernel string `6.6.143-09589-gf9e106250941` and node name `penguin` are consistent with a ChromeOS Linux development container (Crostini: Debian running in an LXD container inside the ChromeOS VM). That is an inference, not a measurement. If it is correct, nested user namespaces and tmpfs mounts depend on the container's security configuration (for example LXD nesting and the AppArmor/seccomp profiles).

**Capabilities needed:**
- **C1** `/proc/sys/user/max_user_namespaces` > 0, and no policy blocks unprivileged user-namespace creation: the Debian `kernel.unprivileged_userns_clone` knob if present, the AppArmor `restrict_unprivileged_userns` knob if present, and container nesting policy.
- **C2** Inside a new user and mount namespace, `mount -t tmpfs -o size=16777216,…` succeeds, and writes beyond the size fail with `ENOSPC`.
- **C3** Inside the namespace, every other writable mount can be remounted bind/read-only, and binding the tmpfs over `/tmp` succeeds.
- **C4** The pinned util-linux `/usr/bin/unshare` and `/usr/bin/mount` are present: util-linux is Essential and `mount` is Priority: required on Debian 12. Their SHA-256 values must be recorded.
- **C5** The pinned Python 3.11.2 and OpenSSL 3.0.22 identities, and the 11 stdlib digests, are unchanged and visible inside the namespace.
- **C6** `/proc` inside the namespace still exposes the process tree and `/proc/self` entries needed by the driver.

**Passive checks the operator can make without creating anything** (read-only; to be recorded in a host-profile addendum):
- `cat /proc/sys/user/max_user_namespaces`;
- `cat /proc/sys/kernel/unprivileged_userns_clone` (if present);
- `cat /sys/kernel/security/apparmor/profiles` (if readable), `cat /proc/self/attr/current`, and `grep Seccomp /proc/self/status`;
- `cat /proc/self/mountinfo` (lists every writable mount that would need a read-only remount);
- `cat /proc/self/uid_map /proc/self/gid_map` (whether the operator is already inside a mapped container namespace);
- `sha256sum /usr/bin/unshare /usr/bin/mount`;
- `ls -l /usr/bin/unshare /usr/bin/mount`.

**The decisive checks C2 and C3 cannot be confirmed passively.** They need a short, **non-candidate host capability probe**. The probe would:
1. create a user and mount namespace;
2. mount a 16 MiB tmpfs;
3. write synthetic bytes until `ENOSPC`;
4. attempt the bind over `/tmp` and the read-only remounts;
5. record the outcomes;
6. exit, leaving nothing behind.

This is a host-qualification experiment: it involves no candidate, P0A3H code or P01–P06. It would still be a new execution on the operator host, so it should be **preregistered with exact commands and expected outcomes, and witnessed before it is run**. It must not be done ad hoc.

## 5. Determination
- **Current strict contract, on recorded evidence:** **`ENVIRONMENT_UNQUALIFIED`.** No kernel-enforced aggregate bound is evidenced for the operator host. REV1's sampled mechanism cannot satisfy it, and C0 does not record the capabilities the only non-privileged strict mechanism needs.
- **Prospective feasibility:** **conditionally feasible.** The §3 design is a genuine kernel-enforced, non-privilege-escalating containment, *if* C1–C6 hold on the host. Whether they hold is unknown; on Crostini, nested-namespace mounting is commonly possible but configuration-dependent, and this report does not assume it.

## 6. Signed authority needed next (the agent drafts nothing to sign and changes nothing)
**Path A — keep the strict cap (preferred by the reviewer).** A human-signed prospective amendment or addendum (for example "P1-A2") that:
- authorizes a preregistered, witnessed **host capability probe** for C1–C6 (exact commands, expected outcomes, nothing persistent);
- if the probe passes, authorizes the §3 namespace-plus-tmpfs execution environment for `P0A3H_P1_DEV_01`;
- records the pinned `unshare` and `mount` identities;
- **explicitly accepts the volatility residual** (crash means evidence loss means INCOMPLETE).

A separately named **C1-REV2**, with the external harness only, would then be built and freshly witnessed. If the probe fails, the result stays `ENVIRONMENT_UNQUALIFIED` for the strict contract.

**Path B — change the assurance claim.** A human-signed prospective amendment that **replaces** the hard "whole attempt disk ≤ 16 MiB" containment requirement with a **monitored storage claim**. It would state every residual openly:
- sampling interval;
- unobserved transient high-water;
- out-of-tree temporary files;
- post-final writes;
- detection rather than prevention.

It must say plainly that this **weakens** the original assurance and does not satisfy the original absolute limit. Any result under it is labelled accordingly.

**Path C — privileged host setup by the human (outside agent scope).** An amendment allowing the operator, as root, to create a disk-backed 16 MiB loop filesystem or quota before the attempt. This avoids volatility but requires the privilege the current instruction excludes, and it would need its own setup record and witness.

Until signed authority resolves this:
- no REV2 is built;
- REV1 is not released;
- `P0A3H_P1_DEV_01` is not authorized;
- P0A4 remains not run.

Retained throughout:
- all earlier negative statuses;
- `LOADED_CODE_IDENTITY_UNVERIFIED`;
- `PRODUCTION_CODE_AUTHORITY_ABSENT`.

## 7. Other observations carried forward (not acted on)
- **W02 release check.** The release check matches a substring of the certificate text. A future revision could require an exact single-line format, with no other content or only an agreed envelope. Human origin remains a separate requirement in either case.
- **Authorship.** The agent wrote the candidate and all of the harness. This report is author analysis, not independent review.
