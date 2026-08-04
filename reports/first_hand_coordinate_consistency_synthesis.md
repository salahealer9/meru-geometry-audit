# First Hand coordinate-consistency synthesis

**Checkpoint:** v0.8  
**Status:** synthesis of already-frozen source-semantic and geometric results  
**Analysis class:** interpretive synthesis; no new geometric fit or optimization

## Scope

This checkpoint consolidates the source-semantic and coordinate-geometry
results obtained for the page-7 spherical projection in Stan Tenen's
*Arm of God* document.

It introduces no new fitted geometry.

It does not:

- refit any curve;
- alter any digitization;
- select a construction scale;
- reclassify X1 as scaffold;
- fit a more flexible projective map;
- compute the reciprocal spiral projection;
- compute S1, S1.5, or S2.

The purpose is to state clearly which parts of the labelled coordinate
construction are supported, which are incompatible with the tested model,
and which questions remain unresolved.

---

# 1. Source-semantic status of X1

The completed source-semantic audit established:

    X1_LABEL_TRACE_CONFIRMED

The printed `x=1` annotation designates the frozen five-segment trace
`AOG-LM-P07-GC-X1`.

Every acquired segment follows the source-designated stroke wherever that
stroke is visible.

Three inter-segment transitions are visibly continuous.

The S03 -> S04 interval is hidden by the thick spiral / UCLR region and was
not reconstructed through the occlusion.

Therefore the later x-family geometric incompatibility cannot be attributed
to an unsupported reassignment of the visible `x=1` stroke.

The separate scaffold-role review established:

    SCAFFOLD_ROLE_NOT_SUPPORTED_BY_SOURCE

The source places the construction within cube-octahedral geometry but does
not explicitly or graphically establish that the source-confirmed `x=1`
stroke is a distinguished scaffold curve.

Consequently the X1 inconsistency may not be dismissed by simply
reclassifying the labelled curve as scaffold geometry.

---

# 2. Stereographic rendering status

Under the tested stereographic rendering comparator, X1 is itself a
well-defined great-circle-like image trace.

Frozen X1 rendering diagnostics include approximately:

    Delta_R              = -0.534270 px
    antipodal deviation  =  0.178841 deg

Thus the x-family failure is not a consequence of X1 being a poorly defined
or unreproducibly traced image curve.

Y1 has weaker rendering closure:

    Delta_R              = -8.743111 px
    antipodal deviation  =  2.438130 deg

This caveat is retained whenever Y1 supplies finite-offset magnitude
information.

Rendering closure and coordinate-family consistency are distinct questions.

---

# 3. y-coordinate family

The labelled y-coordinate family consists of:

    Y0 = y=0 / x-axis
    Y1 = y=1

Under the tested equator-preserving central-projective interpretation, the
family shows strong directional consistency.

Frozen directional diagnostic:

    eta_y = 0.436938761 deg

Frozen equatorial-incidence diagnostic:

    |s_z|                  = 0.009048457837
    equatorial departure  = 0.518445520 deg

The reconstructed projective-infinity direction is:

    300.474784920 deg

The independently frozen lower-right rim landmark is:

    299.783644635 deg

giving:

    angular separation    = 0.691140285 deg
    page-space separation = 4.150278 px

The equatorial-incidence residual and eta_y are mathematically related
expressions of the same parallel-family condition and are not treated as
independent statistical evidence.

The comparison with the independently frozen lower-right source landmark is
a distinct source-landmark consistency check.

Within the accuracy of the hand-drawn source, the y-family is therefore
strongly compatible with the tested affine-parallel central-projective
interpretation.

---

# 4. x-coordinate family

The labelled x-coordinate family consists of:

    YAXIS = x=0 / y-axis
    X1    = x=1

The corresponding frozen directional diagnostic is:

    eta_x = 30.008196754 deg

The equatorial-incidence diagnostic gives:

    |s_z|                  = 0.447466454616
    equatorial departure  = 26.581250131 deg

For an exact affine-parallel pair under the tested equator-preserving
central-projective construction, the two corresponding spherical
great-circle planes must intersect on the equatorial plane.

The source-confirmed YAXIS/X1 pair does not satisfy that condition.

The reported horizontal-projection azimuth of the non-equatorial
intersection is:

    29.972197026 deg

Because the intersection is not equatorial, this number is not itself an
equatorial scaffold-node identification and is not used to assign X1 a
scaffold role.

---

# 5. Three-curve isotropic X1 prediction

A post-hoc three-curve reconstruction was performed using:

    Y1      -> finite-offset magnitude
    YAXIS   -> x-family horizontal direction

with Y0 retained as existing y-family context.

X1 was not used to construct the isotropic candidate.

Because the YAXIS plane normal is unoriented, two sign branches are required.

Frozen Y1-derived magnitude:

    r_y = 1.186584347553
    k_y = 0.842755091168

The two isotropic X1 predictions give:

## Plus frozen-YAXIS-normal branch

    X1 plane residual       = 22.496479194 deg
    X1 centre displacement = 0.594056184288

## Minus frozen-YAXIS-normal branch

    X1 plane residual       = 89.269138711 deg
    X1 centre displacement = 2.113030663385

The previously discussed approximately 89.27-degree result therefore
corresponds to only one of the two mathematically mandatory sign branches.

It is not the unique isotropic prediction.

The more favorable branch still misses the source-confirmed X1 plane by
approximately 22.50 degrees.

---

# 6. Arbitrary positive x-scale

The isotropy condition was then released while retaining the frozen
YAXIS-derived horizontal x-family direction.

For the favorable sign branch, the exact analytic optimum over all positive
x-scales is:

    optimal r_x = 0.866351356057
    optimal k_x = 1.154266098862

with global minimum X1 plane residual:

    20.715146971 deg

The isotropic favorable-branch residual was:

    22.496479194 deg

so arbitrary x-scale freedom improves the discrepancy by only about:

    1.781332223 deg

For the opposite sign branch the optimum occurs only in the limiting case

    r_x -> 0+
    k_x -> infinity

and still leaves:

    45.013146975 deg

The exact minimum over both sign branches is therefore:

    20.715146971 deg

No numerical optimizer determines this result; the global minimum was
obtained analytically.

---

# 7. Interpretation of scale freedom

The anisotropic result answers a narrower question than the earlier x-family
diagnostics:

> Can the X1 inconsistency be repaired solely by choosing a different
> positive x-axis scale?

Under the tested model, the answer is no.

Changing x-scale alters the inclination of the predicted x=1 plane but does
not alter the horizontal direction fixed by the source-labelled YAXIS.

The remaining approximately 20.72-degree global minimum therefore shows
that the incompatibility is not principally a construction-unit or
x-scale-selection problem.

The eta_x, equatorial-incidence residual, isotropic residual, and anisotropic
minimum are geometrically related diagnostics of the same underlying
x-family incompatibility.

They are not four independent statistical detections.

---

# 8. Present coordinate-level conclusion

The current evidence supports an asymmetric result.

## y-family

    Y0 + Y1

is strongly compatible with the tested affine-parallel central-projective
interpretation and approximately recovers its independently frozen
projective-infinity source landmark.

## x-family

    YAXIS + X1

is incompatible with the corresponding affine-parallel condition under the
same model.

The source-semantic audit confirms that:

1. X1 is genuinely the source-labelled `x=1` stroke;
2. the source does not separately establish X1 as scaffold geometry.

The failure also cannot be removed by allowing an arbitrary positive x-axis
scale.

A concise statement is therefore:

> The source-confirmed `x=1` stroke cannot be reconciled with the
> source-labelled y-axis as an affine-parallel coordinate pair under the
> tested equator-preserving central-projective construction by adjustment
> of the x-axis scale. The y-coordinate family, by contrast, shows strong
> directional and source-landmark consistency under the same framework.

---

# 9. What this does not establish

The audit does not presently determine why the x-family is inconsistent.

The current results do not establish any of the following as the cause:

- hand-drawing error;
- transcription error;
- conflation of coordinate and scaffold geometry;
- an undocumented alternate projection;
- a different non-linear map;
- an intentionally illustrative rather than exact construction.

These remain hypotheses unless separately tested.

In particular, the source itself does not presently provide a mathematical
explanation for the X1 inconsistency.

---

# 10. Boundary before spiral/self-embedment work

The coordinate-map audit is now sufficiently constrained to permit the next
stage without silently repairing the source.

Any reciprocal-spiral projection must preserve the distinction between:

1. source statements;
2. the tested coordinate-map family;
3. the observed page-7 drawing;
4. any later candidate reconstruction.

No spiral result may retroactively alter the frozen coordinate-family
findings.

The next stage may therefore investigate the reciprocal spiral on the
already-audited spherical-map candidates, followed later by the preregistered
self-embedment hierarchy:

    S1   directed tangent alignment
    S1.5 Darboux-frame alignment
    S2   collision-free recursive nesting

without treating the page-7 X1 inconsistency as resolved.

