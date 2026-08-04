# First Hand parallel-family equatorial-incidence diagnostic

**Status:** deterministic post-hoc structural diagnostic

No curve, circle, line, rendering map, or projective map was refitted.

## Exact model condition

For an affine-parallel pair under the tested equator-preserving central-projective model, the two spherical great-circle planes must intersect in the equatorial plane:

```text
z_intersection = 0
```

No post-hoc PASS/FAIL threshold is introduced.

## y-family: Y0 and Y1

- |s_z|: `0.009048457837`
- equatorial departure: `0.518445520 deg`
- horizontal azimuth pair: `120.474784920 deg`, `300.474784920 deg`

### Frozen lower-right infinity landmark

- frozen node bearing: `299.783644635 deg`
- nearest predicted antipodal direction: `300.474784920 deg`
- angular node separation: `0.691140285 deg`
- page-space node separation: `4.150278 px`
- frozen node radial residual from limb: `0.439598 px`

The lower-right node was registered before this diagnostic as the visible common y=0/y=1 projective-infinity point.

## x-family: YAXIS and X1

- |s_z|: `0.447466454616`
- equatorial departure: `26.581250131 deg`
- horizontal-projection azimuth pair: `29.972197026 deg`, `209.972197026 deg`

Because this intersection is not assumed equatorial, the reported azimuth is only the azimuth of its horizontal projection.

No rim node is assigned to the x-family.

## Relation to prior eta diagnostic

- prior eta_y: `0.436938761 deg`
- prior eta_x: `30.008196754 deg`

These are mathematically related expressions of the same parallel-family constraint and are not treated as independent statistical evidence.

## Frozen stereographic rendering context

- Y1 epsilon_power: `-0.050489387`
- Y1 Delta_R: `-8.743111 px`
- Y1 Delta_antipodal: `2.438130 deg`
- X1 epsilon_power: `-0.003122798`
- X1 Delta_R: `-0.534270 px`
- X1 Delta_antipodal: `0.178841 deg`

Rendering closure and affine-parallel directional closure remain separate diagnostics.

## Interpretation boundary

This checkpoint does not reclassify X1, fit a more flexible projective map, select a construction scale, or compute the reciprocal spiral or self-embedment metrics.
