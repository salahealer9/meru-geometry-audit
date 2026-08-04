# First Hand three-curve X1 reconstruction and anisotropic reconciliation

**Status:** deterministic post-hoc coordinate-consistency diagnostic

No source curve, line, circle, rendering model, or projective map was refitted.

## Source-semantic prerequisites

- X1 label/trace: `X1_LABEL_TRACE_CONFIRMED`
- X1 scaffold role: `SCAFFOLD_ROLE_NOT_SUPPORTED_BY_SOURCE`

## Three-curve isotropic candidate

- r_y from frozen Y1 centre: `1.186584347553`
- k_y = 1/r_y: `0.842755091168`

YAXIS supplies only an unoriented horizontal normal, so both sign branches are mandatory.

### plus_frozen_yaxis_normal

- predicted centre: `(-0.592793451592, 1.027899964786)`
- X1 plane-angle residual: `22.496479194 deg`
- X1 centre displacement: `0.594056184288`

### minus_frozen_yaxis_normal

- predicted centre: `(0.592793451592, -1.027899964786)`
- X1 plane-angle residual: `89.269138711 deg`
- X1 centre displacement: `2.113030663385`

No sign branch is selected as the source-correct orientation from X1 fit quality.

## Anisotropic scale reconciliation

Only x-scale is released. The YAXIS-derived horizontal direction remains fixed.

### plus_frozen_yaxis_normal

- optimum class: `FINITE_INTERIOR`
- global minimum plane-angle residual: `20.715146971 deg`
- r -> 0 residual: `45.013146975 deg`
- r -> infinity residual: `52.232240366 deg`
- optimal r_x: `0.866351356057`
- optimal k_x: `1.154266098862`

### minus_frozen_yaxis_normal

- optimum class: `LIMIT_R_TO_ZERO`
- global minimum plane-angle residual: `45.013146975 deg`
- r -> 0 residual: `45.013146975 deg`
- r -> infinity residual: `52.232240366 deg`

- minimum over both unoriented sign branches: `20.715146971 deg`

The analytic result, not the plotted sweep, determines the global minimum.

## Rendering-closure context

- Y1 Delta_R: `-8.743111 px`
- Y1 antipodal deviation: `2.438130 deg`
- X1 Delta_R: `-0.534270 px`
- X1 antipodal deviation: `0.178841 deg`

Y1 is the sole finite-offset magnitude input to the isotropic candidate and carries the previously frozen weaker rendering closure.

## Interpretation boundary

This checkpoint tests whether equal scale, and then arbitrary positive x-scale, can reconcile the source-confirmed X1 stroke with the YAXIS-derived x-family direction. It does not explain the cause of any incompatibility and does not assign X1 a scaffold role.
