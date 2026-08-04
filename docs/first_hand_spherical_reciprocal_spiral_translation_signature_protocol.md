# First Hand reciprocal-spiral first-order translation-signature protocol

**Checkpoint:** v0.8
**Status:** protocol frozen before translation-signature calculation
**Analysis class:** pre-model first-order translation diagnostic

## Purpose

Before fitting the preregistered nonlinear translated-isotropic reciprocal
spiral, test whether the already-frozen centered-model residual field has the
specific first-order signature expected from displacement of the construction
origin.

This checkpoint does not adopt the translated model.

It uses only already-frozen parent-model predictions and residuals.

## Frozen inputs

Use:

    data/derived/first_hand_arm_of_god/qc/
    first_hand_spherical_reciprocal_spiral_shape_samples.csv

verified against:

    first_hand_spherical_reciprocal_spiral_shape.sha256

Use the already-frozen fields:

    pass_number
    segment_id
    sample_index
    rho
    F_rho
    weight_length
    weight_equal_segment
    predicted_alpha_length_rad
    residual_alpha_length_rad

No raw digitization is reread.

No parent reciprocal-spiral model is refitted before constructing the
diagnostic.

## Context

The frozen residual morphology is strongly reproducible and strongly
one-cycle phase structured.

The 36-bin phase means have already been inspected post hoc.

Therefore harmonic-1 dominance itself is no longer a blind result.

Any reproduction of that harmonic decomposition in this checkpoint is
descriptive only.

The new diagnostic result is whether the radial scaling and vector structure
match the first-order translation law.

## Exact radial factor

Under normalized stereographic rendering:

    Q =
        2*p / (1-rho^2)

and therefore:

    |Q| =
        2*rho / (1-rho^2).

Hence:

    1/|Q| =
        (1-rho^2)/(2*rho)
        = F(rho).

For a small construction-plane displacement t, the first-order angular
perturbation scales with:

    F(rho),

not generally with:

    1/rho.

The latter is only a small-rho approximation up to an overall factor.

## Frozen centered phase

For every sample define:

    beta_hat =
        predicted_alpha_length_rad

from the already-frozen centered reciprocal-spiral fit.

Do not use a newly fitted phase.

## First-order translation basis

For a small translation:

    t = (t_x, t_y),

the predicted first-order angular perturbation is:

    delta_beta approximately
        -t_x * F(rho) * sin(beta_hat)
        +t_y * F(rho) * cos(beta_hat).

Define:

    g_x =
        -F(rho) * sin(beta_hat)

    g_y =
         F(rho) * cos(beta_hat).

The frozen parent residual is:

    e =
        residual_alpha_length_rad.

## Parent-design orthogonalization

The parent centered fit used:

    alpha =
        a + m*F(rho).

Therefore the parent design space is:

    X0 = [1, F(rho)].

To measure only incremental first-order translation structure, orthogonalize
the two translation basis columns against X0 using the same frozen weights.

For each pass and weighting:

    G = [g_x, g_y]

    G_perp =
        G -
        X0 *
        (X0^T W X0)^(-1) *
        X0^T W G.

Then solve analytically:

    e =
        G_perp * c + epsilon

where:

    c = (c_x, c_y).

No nonlinear optimizer is used.

This is equivalent to measuring the incremental two-dimensional translation
subspace beyond the already-fitted centered model.

## Primary weighting

Use:

    weight_length.

## Secondary weighting

Repeat with:

    weight_equal_segment.

Do not choose weighting according to result.

## Primary quantities

For each independent pass report:

    c_x
    c_y
    |c|
    direction(c)

and:

    parent weighted SSE
    residual weighted SSE after translation-signature projection
    fraction of parent SSE explained

defined as:

    f_explained =
        1 - SSE_after / SSE_parent.

Also report the remaining angular:

    median absolute residual
    RMS residual
    p95 absolute residual
    maximum absolute residual.

No significance threshold is introduced.

## Cross-pass replication

Fit the translation-signature coefficients independently in Pass 1 and
Pass 2.

Report:

    Euclidean coefficient separation
    relative magnitude difference
    circular direction difference.

Strong agreement would support a common deterministic first-order
translation signature.

It would not establish the full nonlinear translated model.

## S04 treatment

S04 remains included in every primary calculation.

The previously observed negative within-segment Pearson correlation is not
sufficient grounds for primary exclusion because:

1. S04 contributes only a small fraction of total parent-model SSE;
2. its signed mean residual has the same positive sign in both passes;
3. its within-segment residual variance is small, making Pearson correlation
   unstable.

A secondary S04-excluded sensitivity calculation is permitted and must be
reported if implemented.

It must never replace the all-segment primary result.

No other segment is excluded.

## Radial-band translation-amplitude diagnostic

As a secondary diagnostic, divide rho into exactly:

    10 fixed bands

with edges:

    0.0, 0.1, 0.2, ..., 0.9, 1.0.

Within every pass and radial band, use the frozen centered phase beta_hat.

Report phase coverage before fitting any within-band harmonic.

### Phase coverage

For all samples in a radial band:

1. reduce beta_hat modulo 2*pi;
2. sort the phases;
3. include the circular wrap-around gap;
4. find the largest circular phase gap.

Define:

    phase_coverage =
        2*pi - largest_gap.

Also report occupancy of exactly:

    36 ten-degree phase bins.

### Eligibility for radial-band harmonic amplitude

A radial band is eligible only if:

    phase_coverage >= pi

and the weighted harmonic design matrix has condition number:

    <= 100.

Otherwise report:

    INSUFFICIENT_PHASE_COVERAGE

and do not infer an amplitude.

No neighboring radial bands are merged after viewing coverage.

### Within-band harmonic

For every eligible radial band fit analytically:

    e =
        c0
        + A*cos(beta_hat)
        + B*sin(beta_hat).

Report:

    amplitude =
        sqrt(A^2+B^2)

    phase_axis =
        atan2(B,A)

and the weighted mean:

    F_bar.

## Translation radial-scaling prediction

For first-order origin displacement, the harmonic amplitude should scale as:

    amplitude approximately
        |t| * F_bar.

Therefore report for each eligible band:

    amplitude
    F_bar
    amplitude / F_bar.

Do not fit an arbitrary radial power law.

Do not fit amplitude against 1/rho as the primary translation law.

If at least three radial bands satisfy the fixed coverage criteria, report
the dispersion of:

    amplitude / F_bar

across eligible bands.

This is descriptive.

No post-hoc constancy threshold is introduced.

If fewer than three bands qualify, state:

    RADIAL_AMPLITUDE_TEST_NOT_IDENTIFIABLE

and do not use the radial-band harmonic result to select a model.

## Joint rho-phase occupancy

For transparency report a fixed:

    10 rho bands x 36 phase bins

occupancy matrix for each pass.

This documents how strongly rho and phase are coupled along the single
observed spiral.

Empty cells remain empty.

No interpolation or smoothing is permitted.

## Exposed harmonic context

The already-inspected 36-bin phase means may be reproduced using the
descriptive model:

    e(phi) =
        C
        + A1*cos(phi)
        + B1*sin(phi)
        + A2*cos(2*phi)
        + B2*sin(2*phi)
        + A3*cos(3*phi)
        + B3*sin(3*phi).

Because this harmonic structure was examined before this protocol was
frozen, it is explicitly exploratory context, not a new confirmatory test.

Do not use its numerical result as the primary evidence of translation.

## No nonlinear translated fit

This checkpoint does not optimize:

    t_x
    t_y
    r_tau
    phi_tau.

It does not invoke the translated-isotropic optimizer.

The already-frozen translated-isotropic objective addendum remains dormant
until this diagnostic result is frozen and interpreted.

## No coordinate-family comparison

Do not compare the inferred translation-signature direction during fitting
with:

    X1
    Y0
    Y1
    YAXIS
    scaffold
    earlier coordinate-plane azimuths.

Any such comparison is post-fit contextual interpretation only.

## Interpretation

A translation interpretation would be strengthened if:

1. the two passes independently recover similar first-order coefficient
   vectors;
2. the two-dimensional translation-signature subspace explains a substantial
   and reproducible fraction of the frozen parent residual;
3. eligible radial bands show broadly stable amplitude/F_bar;
4. weighting sensitivity is small.

Failure of these checks would indicate that one-cycle phase morphology alone
is insufficient evidence for displaced origin.

Regardless of outcome, the full nonlinear translated-isotropic model remains
a separate preregistered test.

## Expected outputs

Primary JSON:

    data/derived/first_hand_arm_of_god/qc/
    first_hand_spherical_reciprocal_spiral_translation_signature.json

Radial-band table:

    data/derived/first_hand_arm_of_god/qc/
    first_hand_spherical_reciprocal_spiral_translation_signature_radial.csv

Joint occupancy table:

    data/derived/first_hand_arm_of_god/qc/
    first_hand_spherical_reciprocal_spiral_translation_signature_occupancy.csv

Report:

    reports/
    first_hand_spherical_reciprocal_spiral_translation_signature.md

Diagnostic figure:

    data/derived/first_hand_arm_of_god/qc/
    first_hand_spherical_reciprocal_spiral_translation_signature.png

First-run log:

    data/derived/first_hand_arm_of_god/qc/
    first_hand_spherical_reciprocal_spiral_translation_signature_first_run.log

Seal:

    data/derived/first_hand_arm_of_god/qc/
    first_hand_spherical_reciprocal_spiral_translation_signature.sha256

