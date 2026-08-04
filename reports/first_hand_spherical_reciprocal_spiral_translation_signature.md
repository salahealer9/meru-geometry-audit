# First Hand reciprocal-spiral translation signature

**Checkpoint:** v0.8

**Analysis class:** `first_order_reciprocal_spiral_translation_signature`

## Scope

This audit tests the first-order residual signature expected from
displacement of the construction origin.

The frozen centered reciprocal-spiral model was not refitted.

No nonlinear translated model was optimized.

## Pass 1

### Primary length-weighted signature

    c_x                         = 0.152681322402
    c_y                         = -0.204631623887
    |c|                         = 0.255314879522
    direction                   = 306.727638909192 deg
    parent SSE explained        = 0.264823719816
    remaining angular RMS       = 35.380220530398 deg
    remaining angular p95       = 52.745359561535 deg

### Equal-segment sensitivity

    |c|                         = 0.181936120591
    direction                   = 309.307753997567 deg
    parent SSE explained        = 0.213820929759

### S04-excluded sensitivity

    |c|                         = 0.257079658970
    direction                   = 307.389853869811 deg
    parent SSE explained        = 0.256129443984

## Pass 2

### Primary length-weighted signature

    c_x                         = 0.174215465673
    c_y                         = -0.221364349518
    |c|                         = 0.281697006937
    direction                   = 308.203020909288 deg
    parent SSE explained        = 0.331608239708
    remaining angular RMS       = 32.251409076066 deg
    remaining angular p95       = 52.516952003173 deg

### Equal-segment sensitivity

    |c|                         = 0.214431396911
    direction                   = 311.320419425678 deg
    parent SSE explained        = 0.305921900176

### S04-excluded sensitivity

    |c|                         = 0.286560629944
    direction                   = 309.991239832923 deg
    parent SSE explained        = 0.328293354523

## Cross-pass primary replication

    coefficient separation      = 0.027270926523
    relative magnitude diff     = 0.09825528290827842
    direction difference        = 1.475382000096 deg

## Radial amplitude diagnostic

### Pass 1

    eligible bands              = 1
    status                      = RADIAL_AMPLITUDE_TEST_NOT_IDENTIFIABLE
    amplitude/F mean            = None
    amplitude/F std             = None
    amplitude/F CV              = None

### Pass 2

    eligible bands              = 1
    status                      = RADIAL_AMPLITUDE_TEST_NOT_IDENTIFIABLE
    amplitude/F mean            = None
    amplitude/F std             = None
    amplitude/F CV              = None

## Interpretation boundary

The numerical result measures only the first-order translation
signature contained in the already-frozen centered-model residual.

It does not establish a finite translated reciprocal-spiral model.

The separately preregistered nonlinear translated-isotropic test
remains dormant until this result is frozen and interpreted.
