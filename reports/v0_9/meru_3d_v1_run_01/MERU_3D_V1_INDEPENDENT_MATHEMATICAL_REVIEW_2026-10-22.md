# Meru 3D-V1 — Independent exact direction-census and separation review

**Date:** 22 October 2026  
**Nature:** Read-only independent mathematical QC of the submitted first-run JSON; original registered calculator **not rerun or imported**.  
**Signed preregistration:** `0e5c1ea4837cf2d2a169fb03c97179e929c3a8ed` (parent `7e05cd275bba83590f1cf1e6f8f88a157f70e2df`; previously verified as signed).  
**Protocol blob:** `217c2b3a3ab06846acaf767636f1efb95ef0e348`.  
**Outcome:** `MERU_3D_V1_FINITE_DIRECTION_CENSUS_AND_SEPARATION_PASS` **for the submitted mathematical evidence**, with first-run origin/provenance qualification noted below.

## Submitted first-run objects

| Object | Bytes | SHA-256 |
|---|---:|---|
| `results(1).json` | 287,711 | `2fd5b37533ccf1d9b380c1741796dae3a0a1f07bce4877a1ac5ebfc6f8d01561` |
| `exit_code(1).txt` | 2 | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` |

`exit_code.txt` is `0`. The results self-identify Python `3.11.2` and signed protocol SHA, consistent with the registered one-run workflow; these fields are recorded claims from JSON, not independent host monitoring.

## Independent result table

| Family | Tier | Signed directions | Unoriented axes | Signed pairs | Axis pairs | Maximum exact cosine | Minimum angle (display only) |
|---|---|---:|---:|---:|---:|---|---:|
| A | G0 | 6 | 3 | 15 | 3 | `0` | 90.000000000° |
| A | G1 | 14 | 7 | 91 | 21 | `sqrt(1/3)` | 54.735610317° |
| A | G2 | 26 | 13 | 325 | 78 | `sqrt(2/3)` | 35.264389683° |
| B | G0 | 6 | 3 | 15 | 3 | `0` | 90.000000000° |
| B | G1 | 18 | 9 | 153 | 36 | `sqrt(1/2)` | 45.000000000° |
| B | G2 | 42 | 21 | 861 | 210 | `sqrt(9/10)` | 18.434948823° |

The `A G0` and `B G0` result is one shared underlying six-direction set, reported twice as prescribed by the six family/tier records.

## Audit method and scope

The reviewer wrote a separate Python enumeration based solely on the four signed definitions `A0`, `C`, `E`, `T`; it does not import the registered calculator, reuse its source, or call its main routine. Each stratum was reconstructed with integer Cartesian products; sets were checked for disjointness, distinctness and antipodal closure. For each family and tier, the review rebuilt exact signed directions and canonical axis representatives, then generated every unordered pair in both quotients. Every submitted `complete_pair_table` entry was checked against exact integer dot products and squared integer norms. The review also reconstructed each stratum-pair summary, all maximizing-pair indices and full maximizing-pair triples.

Normalized dot products were ordered without floating point: sign first, then the exact rational square of the cosine, with reversed squared-ordering for negative values. The signed-direction maximum and axis absolute-dot maximum were independently compared. The measured maxima were also matched against the preregistered exact values `0`, `1/sqrt(3)`, `sqrt(2/3)`, `1/sqrt(2)` and `3/sqrt(10)`; angular degree displays were checked only as presentations.

**Result:** 200 / 200 independent assertions PASS; **0 mismatches**. The exact source JSON, check ledger and review script can be retained as reproducibility evidence.

## Scientific boundaries

This is a mathematical test of the **finite camera-direction sets**, not an observation of any actual Meru shape or Hebrew character. The six signed directions at G0 derive from tetrahedral camera-frame redundancy, and the later A/B tiers are *proposed target-blind grids*, not historical viewing prescriptions. No 3D shadow renderer, target-specific QO/QH metric, matching statistic, covering radius, sphere coverage certificate, continuous-camera optimum or object-specific image-equivalence census was tested.

The audit did **not** independently reauthenticate the original run's `SHA256SUMS.txt`, full `run_01` timestamps/command, frozen script binary, or `stderr.txt`, because only `results(1).json` and `exit_code(1).txt` were supplied for this review. The previous conversation records a successful frozen-script hash check, but the review does not mistake the JSON's provenance fields for independent integrity evidence. Before a signed **results freeze**, preserve the original `evidence/run_01` directory and preferably upload or verify its `SHA256SUMS.txt` and associated captured files. An empty `stderr.txt` is valid evidence and should remain byte-identical, not be synthesized.

**Forward step:** after preservation and human signing of the result, a new, proportionate target-blind 3D-V2 study can examine finite-grid *spherical covering radii*. Unlike nearest-neighbour separation, covering asks for the **farthest sphere point from every listed direction** and must not be inferred from the V1 numbers.
