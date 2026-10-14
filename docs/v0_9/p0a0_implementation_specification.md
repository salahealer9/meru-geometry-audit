# P0A0 implementation-only specification — proposed freeze

Authority: signed protocol commit `d15865167b4e3c454e398bd498d9d681103096f7`, parent
`8bf0babfd91bdefb0792e93707fd0b0da1c09767`. This document and the implementation are
**proposed for independent QC**, not frozen. No registered case was executed.

`REGISTERED_S00_S12_PILOT_NOT_EXECUTED`

`NO_HEBREW_TARGET_ANALYSIS_PERFORMED`

## Bounded independent-QC amendment (implementation only)

B01 replaces the 22 registered Python `assert` statements with explicit
`require(condition, message)` checks raising `AssertionError`. All 22 condition
ASTs are identical to the original package. Normal, `-O` and `-OO` semantics of
the explicit check are covered with unrelated DEV values. The future runner
rejects any nonzero `sys.flags.optimize` before argument parsing, Git access,
output creation or fixture imports; its callable freeze verifier also rejects it.

B02 binds S11's existing serialized `local_bounds` to `parse_pi_bounds`.
Only a bracketed pair of `pi +/- unsigned-integer/positive-integer` expressions
is accepted, with finite strictly ordered endpoints. No `eval` is used. The
unchanged string `[pi-1/4,pi+1/4]` specifies exactly the previous pi±0.25 bounds;
no fixture coordinates, predicates or tolerances changed. Parser validation used
unrelated DEV strings, never the S11 case.

R01 requires successful `git verify-commit --raw` plus exactly one `VALIDSIG`
record with signing fingerprint `D4EC014EEFCC90E619D2AA59A91239ABCF512130`.
The optional primary-key fingerprint must also match. This deliberately strict
policy rejects another valid key or a different signing subkey. Human identity
and independent QC checks remain necessary. Missing/malformed/multiple status
records and nonzero verification exit codes fail closed.

R02's controlled regression results and original missing-crop limitation are in
`reports/v0_9/p0a0_implementation/AMENDMENT_QC.md`. This amendment has not frozen
the implementation and has not executed any registered case.

## Implementation and representation contracts

All changes are additive. The inherited projections, rotations, orbit functions,
placeholder modules, versions, correspondence and scientific records are unchanged.
The new `meru_geometry.p0a0` package contains only pure numerical functions and
independent reference functions; it has no source-file/image/font/network readers.
`registered_pilots/p0a0/fixtures.py` reads only its adjacent proposed JSON config,
and only when explicitly called. It has no import-time generation.

The config is the canonical serialized fixture definition: literal coordinates
or a fully specified symbolic formula. There are no generated fixture images,
registered arrays, optimizer runs or score tables in this package. Defining the
fixtures and specifying analytic expected relationships is not a pilot result.

- Binary64 arithmetic. Absolute comparisons use `atol=1e-10, rtol=0`; normalized
  score comparisons use `atol=1e-9, rtol=0`. Raster coverage is compared at 1e-10.
- All fixtures are deterministic, no RNG is called. Seed 0 is reserved/unused.
- Ordered matching delegates to the unchanged inherited SVD similarity function.
  Returned row-vector transform is `target = scale * source @ Q + translation`.
  The inherited scale constraint is nonnegative, including a zero-scale non-match.
- Normalization subtracts sample mean and divides by sample RMS radius. It is
  explicitly sampling-sensitive and is not advertised as a continuous-support
  normalization. Extent below 1e-14 is rejected; inherited matching has its own
  stricter epsilon-energy floor, retained and diagnosed in S10.
- Open polyline resampling uses 129 arclength points including endpoints. Closed
  resampling closes the path if needed and excludes the duplicated terminal
  endpoint. Consecutive exact duplicates are removed; positive tiny segments are
  retained unless cumulative arclength loses a positive increment, which raises.
  This represents the input polyline, not an unknown smooth curve between samples.
- Support Chamfer is the average of the two directed means of Euclidean nearest
  distances. Sampled Hausdorff is the maximum directed nearest distance. Neither
  claims continuous-support certification, labelled topology, or alignment
  invariance without an explicitly chosen preprocessing transformation.
- Graphs supply vertex IDs, undirected edges, and ordered vertex lists per stroke.
  Every edge appears once in the stroke partition. Coincident coordinates with
  distinct IDs remain distinct. Junctions/intersections must be explicitly split
  by the fixture author. Isolated vertices, duplicate edges, zero-length edges
  and invalid IDs are rejected. No snapping, intersection inference or gap closing.
- Finite-width rasterization is a union of round-capped planar segments. Pixels
  use regular subpixel-centre samples and mean coverage, ascending y rows.
  S05 freezes supersample=1 (no antialiasing), width 1/128, bounds
  [-1.25,-0.25,1.25,0.25], 33×33 and 257×257; threshold >=0.5. The implementation
  supports integer supersampling, checked only with unrelated DEV data. A planar
  ink model is not the shadow of a 3-D ribbon or hand.
- Empty/empty masks return NOT_EVALUABLE with no score; invalid coverage raises.
- Component composite = mean support error + (1/4)*absolute component-count
  difference, used only in S06. This is a declared synthetic diagnostic, not a
  selected future scientific metric or weight.
- S11's tested geometric objective is the squared normal error of a rotated
  unoriented unit axis plus 0.1 times the squared chord of an ordered unit
  landmark. Translation and scale are fixed. Its bounded local optimizer uses
  SciPy `minimize_scalar(method='bounded')`, bounds [pi-1/4,pi+1/4], xatol 1e-12,
  maxiter 200. It is deliberately not a global-search implementation.
- Alignment ties preserve the first strict minimizer: unreversed before reversed,
  shifts ascending. No near-tie equivalence threshold changes this. The analytic
  angle oracle picks the smallest angle in [0,2pi) among exact global minima.

## Planned S00–S12 oracle matrix (not execution results)

Coordinates and variant parameters are fully enumerated in
`registered_pilots/p0a0/fixture_config.json`. Planned test IDs are the named branches
of `registered_pilots/p0a0/cases.py:evaluate`. Every branch emits representation,
provenance, raw and normalized fields (or an explicit applicability statement),
claimed invariances, sensitivity, state and explanation. Known non-identifiability
is EXPECTED_BLIND_SPOT only after all corresponding assertions succeed; unexpected
exceptions or oracle discrepancies become FAIL and remain in the run record.

| Test ID | Representation / exact input definition | Independent oracle / planned relationship | Tolerance / diagnostic |
|---|---|---|---|
| S00 | Three literal 3-D points, cyclic permutation camera, improper z reflection; three nonfinite variants | Scalar component sums independent of projection API; improper/nonfinite raise ValueError | Coordinates 1e-10; exceptions exact |
| S01 | Four literal samples; row Q=[[3/5,4/5],[-4/5,3/5]], scale 5/2, translation (4,-7) | Recover known transform; analytic trigonometric correlation oracle without SVD | Transform 1e-10; relative error 1e-9 |
| S02 | Ordered scalene triangle (0,0),(3,0),(1/4,1), x mirror | Analytic SO2 residual >1e-3; O2 zero with negative determinant; no silent reflection | Oracle error 1e-9 |
| S03 | 65 samples of (5t,2t), t=i/64 versus t=(i/64)^4 | Same straight segment: arclength output exactly (5j/128,2j/128); index-sensitive error >.01 | Coordinates 1e-10, resampled relative 1e-9; expected index blind spot |
| S04 | Three collinear vertices, two edges; one versus two labelled strokes | Support tied at zero; same geometric components and degree endpoints; labelled endpoints 2 versus 4 | Integer counts exact; support 1e-10; non-identifiability explicit |
| S05 | [-1,1] horizontal path versus gap (1/8,9/64) | Gap 1/64; supplied components 1 versus 2; separate scalar horizontal capsule oracle for both rasters; coarse tie and fine difference | Geometry/coverage 1e-10; counts exact; resolution blind spot |
| S06 | Three-point main path plus detached segment (1,.01) to (1.01,.01) | Exhaustive scalar distances; sampled H=sqrt(2)/100; small mean <.01; explicit component term adds .25 | Distances 1e-10; count exact; support not component-aware |
| S07 | Main path plus spur from (1,0) to (1,1/32) | Exposed endpoints 2 versus 3, junctions 0 versus 1; sampled H=1/32, scalar exhaustive comparison | 1e-10, integer counts exact; support not endpoint-aware |
| S08 | Five collinear samples versus displaced central sample (17/16,1/32) | H=1/32, mean=1/160; scalar check raw and normalized; raw feature concealed at .05 but not .01 | 1e-10; normalized threshold diagnostics retained without preclaimed ordering |
| S09 | Five literal asymmetric points, reversed and cyclically shifted by 2 | Reversal allowed and closed shift yield zero; open shift forbidden; analytic residuals for denied operations | Relative 1e-9; denied errors >1e-4; shift/reversal flags exact |
| S10 | Zero extent, exact duplicates, NaN/±Inf, 1e-12 segment and tiny detached graph edge | Explicit exceptions; duplicate arclength convention; positive tiny increments retained; inherited epsilon floor raises; graph retains tiny component | Exceptions exact; ordinary resampling 1e-10; tiny endpoint/increments checked exactly/strictly |
| S11 | Unoriented axis plus ordered unit landmark, w=.1 | Independent polynomial f(c)=1-c²+2w(1-c); global 0 at theta=0, competing local 4w at pi, interior maximum c=-w; retain local/global discrepancy >.39 | Objective 1e-10, optimized value 1e-9; LOCAL_BOUNDED_ONLY |
| S12 | Four 3-D points; 12 tetrahedral frames and duplicate first; rational 3/5–4/5 axial roll | Six signed directions, three axes; scalar coordinate projection; roll equivalent to proper planar rotation; front/back planar det=-1 | Coordinates/determinant 1e-10; roll match 1e-9; class counts exact |

S02's triangle has three unequal edge lengths. Any support-preserving similarity
must have scale one and fix the unique side-length incidence at each vertex;
its mirror cannot be recovered by a proper planar motion. Ordered labels only
strengthen that obstruction. S11's oracle follows by c=cos(theta): the concave
quadratic has maxima at c=-w and endpoint minima; 0<w<1 ensures the pi stationary
point is a strict local circle minimum. These are analytical planned oracles,
not observations from running the registered case.

## Execution isolation and future command

Default pytest searches `tests/`. Registered source is outside this directory,
is not named `test_*.py`, has no pytest functions and does not generate on import.
Only the future named runner calls `configuration`, `generate`, and `evaluate`.
The runner requires a distinct signed implementation commit, exact clean HEAD
and branch, ancestry from the preregistration, and artifact hashes/committed bytes
matching the manifest. Acknowledgement flags do not themselves grant permission.
The human must authorize the later synthetic execution separately after QC/freeze.

Future command, **not executed here** (replace the placeholder with the reviewed
full signed implementation commit; output must not exist and must be outside repo):

```bash
python scripts/p0a0_registered_pilot.py \
  --freeze-commit FULL_SIGNED_IMPLEMENTATION_COMMIT \
  --authorized-synthetic-run \
  --output ../p0a0_registered_pilot_once.jsonl
```

The runner records all 13 cases once in fixed ascending order, preserving failures
and local-optimizer diagnostics. It never auto-repairs, rewrites fixtures or calls
historical scientific scripts. Output creation is exclusive; no previous run is
overwritten. Human workflow must prohibit repeated runs to new paths after a
failure without a new amendment/freeze. The guard is workflow protection, not an
access-control sandbox or a substitute for independent code review.
