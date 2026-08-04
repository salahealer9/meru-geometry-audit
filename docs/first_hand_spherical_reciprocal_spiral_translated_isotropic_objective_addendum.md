# First Hand translated-isotropic reciprocal-spiral objective addendum

**Checkpoint:** v0.8  
**Status:** corrective preregistration before implementation and before any
translated-isotropic real-data fit  
**Parent protocol:** `first_hand_spherical_reciprocal_spiral_translated_isotropic_protocol.md`

## Reason for correction

The parent protocol proposed minimizing the raw weighted angular SSE of

    beta_unwrapped = a + m / R_t

over translation t.

Before implementation and before any translated-isotropic result was
calculated, a mathematical degeneracy was identified.

For a translation whose magnitude T tends to infinity, all vectors

    Q - t

become approximately parallel.

Their angular variation then scales as

    O(1/T).

Consequently a raw angular residual and its squared-error objective may
scale toward zero merely because the candidate origin has been moved
arbitrarily far away.

Therefore raw angular SSE is not a well-posed translation-selection
objective.

No translated-isotropic real-data result has been calculated under the
superseded objective.

## Corrected invariant

For every fixed candidate translation t, retain the exact model relation

    beta_unwrapped =
        a + m * (1/R_t)

where

    R_t = ||Q - t||.

The intercept a and slope m remain determined analytically by weighted
linear least squares.

Define:

    SSE =
        sum_i w_i *
        (beta_i - a - m/R_i)^2

and:

    beta_bar =
        sum_i w_i beta_i / sum_i w_i

    SST =
        sum_i w_i *
        (beta_i - beta_bar)^2.

The corrected translation objective is:

    J(t) = SSE / SST

which is equivalently:

    J(t) = 1 - R_w^2(t).

Minimize J.

No numerical optimizer is used for a or m.

## Why this removes the trivial angular-collapse advantage

At large translation magnitude, both the angular residual variance and
the total angular variance shrink.

Normalizing SSE by SST prevents a candidate from improving solely because
all observed directions have become nearly constant.

The translated model must instead improve the fraction of angular
structure explained by the reciprocal relation.

## Degenerate angular variance

If:

    SST <= 1e-18

the candidate is invalid and receives infinite objective.

If any:

    R_t <= 1e-12

the candidate is invalid and receives infinite objective.

No source point is deleted.

## Translation parameterization

Do not optimize directly over an arbitrarily bounded construction-plane
translation.

Instead parameterize the candidate construction origin by a normalized
stereographic page-disk position:

    tau =
        (tau_u, tau_v)

with:

    r_tau = ||tau|| < 1.

Convert tau to construction-plane translation by:

    t =
        2*tau / (1 - ||tau||^2).

Thus every finite construction-plane translation corresponds to a point
inside the unit disk, while translation magnitude tending to infinity
corresponds to:

    ||tau|| -> 1.

The optimized parameters are represented in polar form:

    r_tau
    phi_tau

with:

    tau_u = r_tau*cos(phi_tau)
    tau_v = r_tau*sin(phi_tau).

## Primary search domain

Use:

    0 <= r_tau <= 0.98
    -pi <= phi_tau <= pi.

The value:

    r_tau = 0.98

corresponds to a construction-plane translation magnitude of approximately:

    |t| = 2*0.98 / (1 - 0.98^2)
        ≈ 49.49494949.

This is deliberately broad.

## Mandatory expanded-bound sensitivity

Repeat the primary length-weighted optimization with:

    0 <= r_tau <= 0.995
    -pi <= phi_tau <= pi.

The expanded boundary corresponds to:

    |t| ≈ 199.49874687.

This repeat is mandatory regardless of the primary result.

Report:

    parameter separation between the two solutions
    objective difference
    whether either solution lies at its radial search boundary.

Do not select whichever bound gives a preferred scientific conclusion.

A solution driven toward the stereographic unit boundary indicates that a
finite translated origin is not stably identified by this test.

## Deterministic optimizer

Use SciPy differential evolution with the following frozen settings:

    strategy = "best1bin"
    maxiter = 300
    popsize = 15
    tol = 1e-10
    atol = 1e-12
    mutation = (0.5, 1.0)
    recombination = 0.7
    seed = 20260804
    updating = "immediate"
    workers = 1
    polish = True

Optimization variables:

    (r_tau, phi_tau).

Bounds are exactly those specified above.

The random seed is reset to the same frozen value for every independent
optimization.

No result-dependent restart is permitted.

## Primary and secondary weighting

For each pass independently:

### Primary

Optimize t using the already-frozen:

    weight_length.

### Secondary

Optimize t independently using the already-frozen:

    weight_equal_segment

within the primary r_tau <= 0.98 search domain.

The secondary fit is a mandatory weighting-sensitivity result.

Do not choose between primary and secondary according to outcome.

The mandatory r_tau <= 0.995 expanded-bound repeat is applied to the
primary length-weighted fit.

## Model parameters after translation selection

At the selected t, report the analytically profiled:

    a
    m
    alpha0 = a mod 2*pi
    handedness = sign(m)
    k = abs(m)
    weighted R^2
    J = 1 - weighted R^2.

## Page-space geometric diagnostic

Raw angular SSE is not used to select t.

After fitting, construct a geometric diagnostic without any additional fit.

For each observed sample:

    W_i = Q_i - t
    R_i = ||W_i||

and:

    beta_hat_i =
        a + m/R_i.

Define the model point at the same translated radial coordinate:

    Q_hat_i =
        t +
        R_i *
        [cos(beta_hat_i), sin(beta_hat_i)].

Render Q_hat back to normalized stereographic page coordinates using:

    q_hat = ||Q_hat||

    p_hat =
        Q_hat /
        (sqrt(1 + q_hat^2) + 1).

Compare p_hat with the already-frozen observed normalized page point:

    p_i = (u_i, v_i).

Define pixel discrepancy:

    d_page_px =
        R_limb * ||p_hat - p_i||.

Report weighted:

    median
    mean
    RMS
    p95
    maximum.

This is a model diagnostic, not an additional optimization objective.

## Construction-plane transverse diagnostic

Also report:

    d_Q =
        2*R_i*abs(sin(delta_beta_i/2))

where:

    delta_beta_i =
        beta_i - beta_hat_i.

This removes the misleading shrinkage of raw angular residual at large
translation.

Report weighted:

    median
    mean
    RMS
    p95
    maximum.

## Cross-prediction

Cross-prediction remains as specified in the parent protocol.

Use the complete fitted tuple from the training pass:

    t
    a
    m

without any refit, angular offset, branch adjustment, or phase correction.

Evaluate directly on the other frozen pass.

Report:

    angular residual
    construction-plane transverse discrepancy
    stereographic page-pixel discrepancy.

## Intrinsic 3*pi span holdout

The source's:

    3*pi

span remains excluded from optimization.

After fitting, compute:

    Delta_beta =
        beta_last - beta_first

around the fitted translated origin.

Compare only after fitting with:

    3*pi = 540 degrees.

The holdout must not influence:

    t
    a
    m
    k.

## Boundary interpretation

The following quantities must always be reported:

    fitted r_tau
    distance to primary radial bound
    fitted |t|
    expanded-bound fitted r_tau
    expanded-bound fitted |t|.

Do not silently describe a boundary-seeking solution as a finite recovered
construction origin.

## Superseded parent-protocol instruction

The parent instruction:

    "Minimize that frozen objective over t"

where "that frozen objective" meant raw weighted angular SSE is superseded.

All other parent-protocol restrictions remain in force unless explicitly
modified by this addendum.

