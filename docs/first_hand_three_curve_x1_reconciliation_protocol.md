# First Hand three-curve X1 reconstruction and anisotropic reconciliation

**Checkpoint:** v0.8  
**Analysis class:** deterministic post-hoc coordinate-consistency diagnostic  
**Status:** protocol frozen before repository implementation and execution

## Motivation

The completed source-semantic audit established:

1. the frozen five-segment trace `AOG-LM-P07-GC-X1` is the stroke
   designated by the printed `x=1` annotation;

2. the source does not establish that this stroke has a separate
   cube-octahedral scaffold role.

The previously tested equator-preserving central-projective coordinate model
shows strong y-family directional closure but a substantial x-family
directional incompatibility.

This checkpoint asks two narrower questions:

1. Under an additional isotropy assumption, what x=1 great circle is implied
   by Y0, Y1, and YAXIS, without using X1?

2. If isotropy is removed and the x scale is allowed to vary freely, can any
   positive x scale reconcile the YAXIS-derived x-family direction with the
   source-confirmed X1 great circle?

## Post-hoc status

This analysis is explicitly post-hoc.

The x-family incompatibility is already known.

An external reviewer has also previously reported an approximately
89.27-degree isotropic X1 plane mismatch for one sign convention.

That value is therefore not a blind finding.

Furthermore, the zero-line YAXIS determines an unoriented plane direction.
Consequently two x-orientation sign branches exist and both must be reported.
The approximately 89.27-degree value must not be treated as the unique
isotropic prediction unless a source-independent sign convention establishes
that branch before comparison with X1.

## Frozen inputs

Use only previously frozen artifacts.

Primary geometric input:

    data/derived/first_hand_arm_of_god/qc/
    first_hand_stereographic_plane_angles.json

Required curves:

    AOG-LM-P07-GC-Y0
    AOG-LM-P07-GC-Y1
    AOG-LM-P07-GC-YAXIS
    AOG-LM-P07-GC-X1

Source-semantic prerequisites:

    reports/first_hand_x1_source_semantic_question1_ledger.md
    reports/first_hand_x1_source_semantic_question2_ledger.md

Rendering closure context is carried from the already-frozen stereographic
rendering comparator.

No curve, line, circle, sphere, or rendering fit is repeated.

## Coordinate-plane convention

Under the tested equator-preserving central-projective construction,

    x = 0  ->  g_x · (X,Y) = 0

    x = 1  ->  g_x · (X,Y) - Z = 0

    y = 0  ->  g_y · (X,Y) = 0

    y = 1  ->  g_y · (X,Y) - Z = 0

For normalized stereographic rendering, a finite great-circle image generated
by

    g · (X,Y) - Z = 0

has normalized page-circle centre

    c = g.

Thus the frozen Y1 circle centre determines g_y.

The frozen YAXIS diameter line determines only the unoriented direction of
g_x.

## Part A — three-curve isotropic candidate

### Inputs used to construct the candidate

Use:

    Y1      -> finite offset magnitude
    YAXIS   -> x-family horizontal direction

Y0 is carried as the already-frozen independent directional validation of the
Y1 y-family.

X1 is not used to construct the isotropic candidate.

### y-family magnitude

Let

    r_y = ||c_Y1||

and

    k_y = 1 / r_y.

No new fit is performed.

### x-family direction

Let u_x be a unit horizontal vector normal to the frozen YAXIS diameter line.

Because a line normal is unoriented,

    u_x

and

    -u_x

represent the same x=0 great circle.

Therefore the isotropic reconstruction has two sign branches:

    g_x,+ = +r_y u_x

    g_x,- = -r_y u_x

Both branches are mandatory outputs.

Neither branch may be selected using X1 fit quality.

### Predicted isotropic x=1 planes

For each sign branch,

    P_x1,±:
        g_x,± · (X,Y) - Z = 0.

Compute the corresponding unit plane normal and normalized stereographic
circle centre.

### X1 holdout comparison

Only after both predicted branches have been constructed, compare each against
the frozen observed X1 plane.

Report for each branch:

    predicted circle centre
    predicted source scale k_x
    unoriented plane-angle residual to X1
    normalized circle-centre displacement from X1

No branch is labelled "correct" solely because it has the smaller X1 residual.

## Part B — anisotropic reconciliation family

Release only the equal-scale condition.

Retain the frozen YAXIS-derived horizontal direction.

For each sign branch define

    g_x,±(r) = ±r u_x,
    r > 0.

Equivalent source scale:

    k_x = 1/r.

X1 may be used here only as the residual target of this explicitly post-hoc
one-parameter reconciliation test.

This branch is not a holdout prediction.

## Analytic global minimum

Let the frozen observed X1 unit plane normal be

    n = (h_x, h_y, z)

and use the normalized predicted plane normal

    p_±(r) =
        (-g_x,±(r)_x,
         -g_x,±(r)_y,
          1)
        / sqrt(1+r^2).

Define

    A_± = ∓(h_x u_x + h_y u_y)

    B = z.

Then

    |n · p_±(r)|
      =
    |A_± r + B| / sqrt(1+r^2).

For each sign branch determine the exact supremum over

    r > 0

and therefore the exact global minimum unoriented plane angle.

When A_± B > 0, the interior maximum occurs at

    r* = A_± / B

with

    max |n · p_±|
      =
    sqrt(A_±^2 + B^2).

Otherwise the global maximum is obtained as the larger relevant limiting
value from

    r -> 0+
    r -> infinity.

Report explicitly whether the optimum is:

    FINITE_INTERIOR
    LIMIT_R_TO_ZERO
    LIMIT_R_TO_INFINITY.

No numerical optimizer determines the primary result.

## Deterministic residual sweep

For visualization only, evaluate a fixed logarithmic grid:

    r = 10^q
    q in [-3, +3]
    1201 equally spaced q values.

Equivalently:

    k_x in [10^-3, 10^3].

The sweep does not determine the reported global minimum; the analytic result
does.

Produce a residual-versus-log10(k_x) figure for both sign branches.

## Relationship to earlier x-family diagnostics

The anisotropic minimum is geometrically related to the already-reported
YAXIS/X1 directional incompatibility.

It is not counted as independent statistical evidence.

Its purpose is to answer the model-specific question:

    can scale alone repair the x-family?

## Y1 closure caveat

Y1 is the sole finite-offset magnitude input to the isotropic candidate.

Carry its already-frozen stereographic rendering closure diagnostics,
including the larger Y1 rendering misclosure relative to X1.

Do not invent a confidence interval for k_y.

The existing drawing/closure diagnostics are not automatically a statistical
sampling distribution and therefore are not converted into a new CI without
a separately frozen uncertainty model.

## Scaffold curve

The frozen scaffold holdout is not used to construct either the isotropic or
anisotropic candidate.

Because the completed source-semantic audit did not establish X1 as a
scaffold curve, no scaffold identity is inferred from geometric proximity.

A scaffold comparison may be reported only as a secondary descriptive
geometric comparison if it can be obtained entirely from already-frozen
scaffold geometry without refitting.

It must not alter the primary X1 result.

## Forbidden operations

Do not:

- refit Y0, Y1, YAXIS, or X1;
- choose an x-orientation sign from X1 fit quality;
- tune an anisotropic sweep range to the observed optimum;
- fit a general 2x2 map;
- fit a 3x3 projective map;
- fit a nonlinear map;
- reclassify X1 as scaffold;
- select G30, GHALF, GUNIT, or GONE;
- compute the reciprocal spiral projection;
- compute S1;
- compute S1.5;
- compute S2.

## Primary outputs

Report:

### Isotropic branch

    r_y
    k_y
    two predicted g_x sign branches
    two predicted X1 plane normals
    two X1 plane-angle residuals
    two X1 centre-displacement residuals

### Anisotropic branch

For both signs:

    analytic optimum class
    optimal r_x if finite
    optimal k_x if finite
    exact minimum X1 plane-angle residual
    residual asymptotes
    deterministic sweep curve

## Interpretation outcomes

No threshold-based PASS/FAIL classification is introduced.

Interpret continuously.

A zero or near-zero anisotropic minimum would show that the earlier X1
failure can be explained primarily by x-scale choice.

A non-negligible global minimum demonstrates that scale freedom alone cannot
reconcile the source-confirmed X1 stroke with the YAXIS-derived x-family
direction.

This does not establish the cause of the source inconsistency.

Possible causes such as drawing error, mixed constructions, or undocumented
construction conventions remain hypotheses unless separately demonstrated.

