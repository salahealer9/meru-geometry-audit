# First Hand translated-isotropic reciprocal-spiral audit

**Checkpoint:** v0.8

**Analysis class:** `spiral_only_translated_isotropic_central_projective_stereographic_reciprocal`

## Scope

This is the preregistered full translated-isotropic spiral-only model.

No first-order translation-signature coefficient was used for
initialization, bounds, direction, or tuning.

No coordinate curve, scaffold, endpoint landmark, or source endpoint
theta convention was used to fit the model.

The nonlinear search variables are only:

    r_tau
    phi_tau

For every candidate translation, a and m are solved analytically.

The corrected optimization objective is:

    J = SSE / SST = 1 - weighted R^2.

## Pass 1

### Primary length-weighted fit

    r_tau                   = 0.024697224138
    phi_tau                 = 234.825259943693 deg
    tau_u                   = -0.014227379456
    tau_v                   = -0.020187485082
    t_x                     = -0.028472125567
    t_y                     = -0.040399612025
    |t|                     = 0.049424594951
    radial-bound distance   = 9.553027758618e-01
    at radial boundary      = False
    a                       = -8.041803037843 rad
    alpha0                  = 259.238626256129 deg
    m                       = 1.967848571007
    handedness              = +1
    k                       = 1.967848571007
    J                       = 0.028643967678
    weighted R^2            = 0.971356032322

    angular RMS             = 27.309138457932 deg
    angular p95             = 52.821490513726 deg
    transverse-Q RMS        = 1.904540212170
    transverse-Q p95        = 3.412670995428
    page RMS                = 66.181120563120 px
    page p95                = 145.876921607001 px

    intrinsic span          = 578.810767364584 deg
    span minus 3*pi         = 38.810767364584 deg

### Mandatory expanded-bound fit

    r_tau                   = 0.024697237411
    phi_tau                 = 234.825271527055 deg
    tau_u                   = -0.014227383021
    tau_v                   = -0.020187498808
    t_x                     = -0.028472132720
    t_y                     = -0.040399639520
    |t|                     = 0.049424621546
    radial-bound distance   = 9.703027625886e-01
    at radial boundary      = False
    a                       = -8.041803150233 rad
    alpha0                  = 259.238619816668 deg
    m                       = 1.967848666859
    handedness              = +1
    k                       = 1.967848666859
    J                       = 0.028643967678
    weighted R^2            = 0.971356032322

    angular RMS             = 27.309138381793 deg
    angular p95             = 52.821487648244 deg
    transverse-Q RMS        = 1.904540536672
    transverse-Q p95        = 3.412671660143
    page RMS                = 66.181126049503 px
    page p95                = 145.876949918517 px

    intrinsic span          = 578.810757272627 deg
    span minus 3*pi         = 38.810757272627 deg

### Secondary equal-segment fit

    r_tau                   = 0.020430291973
    phi_tau                 = 239.352637561616 deg
    tau_u                   = -0.010414397667
    tau_v                   = -0.017576608072
    t_x                     = -0.020837492837
    t_y                     = -0.035167895113
    |t|                     = 0.040877646145
    radial-bound distance   = 9.595697080273e-01
    at radial boundary      = False
    a                       = -8.043878900654 rad
    alpha0                  = 259.119688078180 deg
    m                       = 1.945511800796
    handedness              = +1
    k                       = 1.945511800796
    J                       = 0.015181932016
    weighted R^2            = 0.984818067984

    angular RMS             = 23.579456894532 deg
    angular p95             = 48.252496388557 deg
    transverse-Q RMS        = 1.344952383605
    transverse-Q p95        = 1.239674637733
    page RMS                = 50.742024907840 px
    page p95                = 98.434627386410 px

    intrinsic span          = 581.458624011134 deg
    span minus 3*pi         = 41.458624011134 deg

### Expanded-bound sensitivity

    translation separation = 0.000000028410
    tau separation         = 0.000000014181
    objective difference   = -5.784608902992e-14
    primary at boundary    = False
    expanded at boundary   = False

## Pass 2

### Primary length-weighted fit

    r_tau                   = 0.023116671758
    phi_tau                 = 235.653553349982 deg
    tau_u                   = -0.013042323054
    tau_v                   = -0.019086076667
    t_x                     = -0.026098592688
    t_y                     = -0.038192562694
    |t|                     = 0.046258062924
    radial-bound distance   = 9.568833282419e-01
    at radial boundary      = False
    a                       = -8.045019303426 rad
    alpha0                  = 259.054347812416 deg
    m                       = 1.983056988422
    handedness              = +1
    k                       = 1.983056988422
    J                       = 0.028743827698
    weighted R^2            = 0.971256172302

    angular RMS             = 27.516910129984 deg
    angular p95             = 54.245660347478 deg
    transverse-Q RMS        = 2.099469705999
    transverse-Q p95        = 3.417521244463
    page RMS                = 66.711415834442 px
    page p95                = 145.360894411625 px

    intrinsic span          = 579.817898889037 deg
    span minus 3*pi         = 39.817898889037 deg

### Mandatory expanded-bound fit

    r_tau                   = 0.023116668209
    phi_tau                 = 235.653539840583 deg
    tau_u                   = -0.013042325552
    tau_v                   = -0.019086070661
    t_x                     = -0.026098597682
    t_y                     = -0.038192550670
    |t|                     = 0.046258055814
    radial-bound distance   = 9.718833317913e-01
    at radial boundary      = False
    a                       = -8.045019243062 rad
    alpha0                  = 259.054351271024 deg
    m                       = 1.983056941479
    handedness              = +1
    k                       = 1.983056941479
    J                       = 0.028743827698
    weighted R^2            = 0.971256172302

    angular RMS             = 27.516910128022 deg
    angular p95             = 54.245660842905 deg
    transverse-Q RMS        = 2.099469516995
    transverse-Q p95        = 3.417520891232
    page RMS                = 66.711411962499 px
    page p95                = 145.360879398069 px

    intrinsic span          = 579.817902180716 deg
    span minus 3*pi         = 39.817902180716 deg

### Secondary equal-segment fit

    r_tau                   = 0.018468406556
    phi_tau                 = 240.207577901823 deg
    tau_u                   = -0.009176197459
    tau_v                   = -0.016027458966
    t_x                     = -0.018358656727
    t_y                     = -0.032065855020
    |t|                     = 0.036949415895
    radial-bound distance   = 9.615315934435e-01
    at radial boundary      = False
    a                       = -8.040423663250 rad
    alpha0                  = 259.317658598659 deg
    m                       = 1.954049238329
    handedness              = +1
    k                       = 1.954049238329
    J                       = 0.015139332200
    weighted R^2            = 0.984860667800

    angular RMS             = 23.580296075667 deg
    angular p95             = 47.618358957756 deg
    transverse-Q RMS        = 1.470580104490
    transverse-Q p95        = 1.216761220535
    page RMS                = 51.045632074644 px
    page p95                = 99.457333193321 px

    intrinsic span          = 582.630622778822 deg
    span minus 3*pi         = 42.630622778822 deg

### Expanded-bound sensitivity

    translation separation = 0.000000013020
    tau separation         = 0.000000006504
    objective difference   = 2.789435349371e-15
    primary at boundary    = False
    expanded at boundary   = False

## Cross-pass primary replication

    construction translation separation = 0.003241099362
    tau-disk separation                 = 0.001617856351
    relative |t| difference             = 0.06618821209995598
    translation direction difference    = 0.828293406289 deg
    |k1-k2|                             = 0.015208417416
    relative k difference               = 0.007698699544589697
    alpha0 difference                   = 0.184278443713 deg
    handedness agrees                   = True

## Zero-refit cross-prediction

### pass1_model_on_pass2

    angular RMS          = 27.685564464958 deg
    angular p95          = 52.349237066801 deg
    transverse-Q RMS     = 2.092399692606
    page RMS             = 66.166327615111 px
    page p95             = 145.169867513765 px
    span                  = 578.813300413645 deg

### pass2_model_on_pass1

    angular RMS          = 27.518512045849 deg
    angular p95          = 54.726979584350 deg
    transverse-Q RMS     = 1.910884690083
    page RMS             = 66.833923539572 px
    page p95             = 146.063096408372 px
    span                  = 579.845446383053 deg

## Interpretation boundary

A lower objective is not sufficient by itself to support a finite
translated construction origin.

Interpretation must jointly consider:

- residual reduction;
- finite versus boundary-seeking translation;
- expanded-bound stability;
- Pass-1 / Pass-2 parameter replication;
- zero-refit cross-prediction;
- page-space geometric residual;
- independent 3*pi span holdout.

Coordinate curves remain completely unused and therefore available
for a later zero-refit prediction if this model survives.
