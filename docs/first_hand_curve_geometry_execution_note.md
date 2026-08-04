# First Hand curve geometry — execution note

The analysis protocol and raw observations were frozen before real-data
execution.

Two pre-result implementation failures occurred after crossing the
execution boundary:

1. the first implementation queried `limb_geometry` from the expanded
   neutral-analysis wrapper rather than from the original frozen neutral
   geometry census;
2. after correcting that interface, the raw-pixel nonlinear circle
   optimizer exhausted its function-evaluation budget before a result
   artifact was produced.

No pass-agreement statistic, circle/ellipse residual, calibration result,
holdout result, projective result, or self-embedment result had been
reported before these corrections.

The second correction is numerical rather than scientific:

- the geometric circle objective is unchanged;
- equal-pass and arc-length weighting are unchanged;
- the 12 px review threshold is unchanged;
- coordinate values are translated and scaled before optimization;
- a weighted algebraic circle supplies a deterministic initial estimate;
- the nonlinear fit still minimizes the geometric radial residual;
- ellipse model bounds are unchanged;
- the circle-derived ellipse starting value is clipped inside those
  pre-existing bounds;
- the scaffold holdout partition is unchanged.

These changes are intended solely to make the preregistered descriptive
fits numerically well-conditioned.
