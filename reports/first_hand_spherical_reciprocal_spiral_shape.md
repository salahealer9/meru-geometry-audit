# First Hand spherical reciprocal-spiral shape audit

**Checkpoint:** v0.8

**Analysis class:** `spiral_led_isotropic_central_projective_stereographic_reciprocal_shape`

## Question

Does the independently acquired spherical spiral satisfy the
radial-angular relation required by a stereographically rendered
isotropic central-projective image of `r*theta = 1`?

The labelled coordinate curves and scaffold are not used.

## Frozen page frame

    center_x = 1255.126838755607 px
    center_y = 694.602781503521 px
    R_limb   = 341.906449919406 px

## Model

    F(rho) = (1-rho^2)/(2*rho)

    alpha_unwrapped = a + m*F(rho)

    k = abs(m)

## Pass 1

Radial domain:

    rho_min             = 0.083771388784
    rho_max             = 0.963139650284
    count rho <= 0      = 0
    count rho >= 1      = 0
    all in open disk    = True

Source-order angular topology:

    unwrapped span      = -10.374183345022 rad
    unwrapped span      = -594.396921564648 deg
    maximum gap jump    = 9.533283153093 deg

### Primary length-weighted fit

    intercept a       = -7.771677222792 rad
    alpha0 mod 2*pi   = 4.794693391567 rad
    alpha0 mod 2*pi   = 274.715695396054 deg
    signed slope m    = 1.768957243729
    handedness        = +1
    spiral scale k    = 1.768957243729
    weighted R^2      = 0.935638314990

Angular residual:

    median |residual| = 38.158774368687 deg
    mean   |residual| = 35.672576928929 deg
    RMS residual      = 41.263379333750 deg
    p95   |residual|  = 64.815527424515 deg
    max   |residual|  = 66.302354071706 deg

Fixed-rho angular chord discrepancy:

    median = 58.666986356482 px
    RMS    = 63.993468596472 px
    p95    = 108.270972267391 px
    max    = 122.772414972595 px

### Secondary equal-segment fit

    intercept a       = -7.761344081868 rad
    alpha0 mod 2*pi   = 4.805026532491 rad
    alpha0 mod 2*pi   = 275.307740760139 deg
    signed slope m    = 1.776394199464
    handedness        = +1
    spiral scale k    = 1.776394199464
    weighted R^2      = 0.956197751744

Angular residual:

    median |residual| = 35.338838777764 deg
    mean   |residual| = 35.976887420650 deg
    RMS residual      = 40.405102832096 deg
    p95   |residual|  = 64.724586631073 deg
    max   |residual|  = 68.868375763884 deg

Fixed-rho angular chord discrepancy:

    median = 38.485199582105 px
    RMS    = 55.458464058742 px
    p95    = 106.697661784209 px
    max    = 119.337219652930 px

### Weighting sensitivity

    |delta k|           = 0.007436955735
    relative delta k    = 0.004195327800

## Pass 2

Radial domain:

    rho_min             = 0.086363859927
    rho_max             = 0.968397417359
    count rho <= 0      = 0
    count rho >= 1      = 0
    all in open disk    = True

Source-order angular topology:

    unwrapped span      = -10.367107878307 rad
    unwrapped span      = -593.991527183805 deg
    maximum gap jump    = 11.754316198140 deg

### Primary length-weighted fit

    intercept a       = -7.809383836583 rad
    alpha0 mod 2*pi   = 4.756986777776 rad
    alpha0 mod 2*pi   = 272.555265566122 deg
    signed slope m    = 1.806808782103
    handedness        = +1
    spiral scale k    = 1.806808782103
    weighted R^2      = 0.941790997491

Angular residual:

    median |residual| = 35.713329213725 deg
    mean   |residual| = 33.927147852759 deg
    RMS residual      = 39.448741257376 deg
    p95   |residual|  = 64.380505521001 deg
    max   |residual|  = 66.048875946914 deg

Fixed-rho angular chord discrepancy:

    median = 56.538573904944 px
    RMS    = 64.256317125647 px
    p95    = 109.187918626887 px
    max    = 138.810176210175 px

### Secondary equal-segment fit

    intercept a       = -7.801790254618 rad
    alpha0 mod 2*pi   = 4.764580359742 rad
    alpha0 mod 2*pi   = 272.990345764118 deg
    signed slope m    = 1.808358801843
    handedness        = +1
    spiral scale k    = 1.808358801843
    weighted R^2      = 0.963032524869

Angular residual:

    median |residual| = 30.393579676103 deg
    mean   |residual| = 32.282469189176 deg
    RMS residual      = 37.144967261877 deg
    p95   |residual|  = 62.795195782202 deg
    max   |residual|  = 66.628400769301 deg

Fixed-rho angular chord discrepancy:

    median = 38.139509700063 px
    RMS    = 54.455134401329 px
    p95    = 107.328441706178 px
    max    = 136.334664770984 px

### Weighting sensitivity

    |delta k|           = 0.001550019740
    relative delta k    = 0.000857509205

## Cross-pass primary replication

    |k1-k2|             = 0.037851538375
    relative k diff     = 0.021171149399
    handedness agrees   = True
    alpha0 difference   = 0.037706613791 rad
    alpha0 difference   = 2.160429829932 deg

## Interpretation boundary

This is a spiral-only shape test.

No source endpoint theta convention was imposed.

No coordinate-derived scale was compared or selected.

No Y0, Y1, YAXIS, X1, or scaffold curve was used to fit the result.

No general anisotropic, 2x2, projective, or nonlinear model was fitted.

Compatibility would support this specific geometric construction
family but would not prove that it was the historical construction.
