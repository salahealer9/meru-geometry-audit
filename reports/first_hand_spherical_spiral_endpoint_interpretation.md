# First Hand spherical spiral endpoint interpretation

**Checkpoint:** v0.8  
**Status:** interpretation of frozen endpoint-consistency result  
**Analysis class:** interpretive synthesis; no new fit

## Frozen numerical result

Inner endpoint:

    Pass-1 distance to prior landmark = 5.573018634423 px
    Pass-2 distance to prior landmark = 5.356464843230 px
    Two-pass mean distance            = 5.452027774990 px
    Spiral endpoint pass separation   = 0.775936334840 px

Prior inner-landmark consensus uncertainty:

    3.000000000000 px

Continuous-spiral descriptive source-reading scale:

    7.000000000000 px

Outer endpoint:

    Pass-1 distance to prior landmark = 13.109712967054 px
    Pass-2 distance to prior landmark = 11.379005745177 px
    Two-pass mean distance            = 12.240276302710 px
    Spiral endpoint pass separation   = 1.842616560175 px

Prior outer-landmark consensus uncertainty:

    6.750000000000 px

Continuous-spiral descriptive source-reading scale:

    7.000000000000 px

## Inner interpretation

The independently acquired continuous-spiral samples are highly
repeatable at the inner end.

Their two-pass mean lies approximately 5.45 px from the earlier neutral
inner-end landmark.

This is larger than the earlier point-landmark consensus uncertainty but
smaller than the descriptive half-stroke source-reading scale of the thick
continuous spiral.

The result therefore supports close source-level consistency but does not
establish exact pixel coincidence.

## Outer interpretation

The outer comparison has different source semantics.

During both continuous-spiral acquisitions, S10 was deliberately stopped
before the Y0 / lower-right filled-node region in accordance with the
acquisition rule forbidding tracing through filled nodes, occlusions, and
hidden continuation.

Therefore the final acquired S10 sample is the final clean visible
centreline sample before the terminal node region.

It is not an independently measured centre of the lower-right node.

The approximately 12.24 px separation from

    AOG-LM-P07-RIM-NODE-LR-SHARED

must therefore not be interpreted as a 12.24 px failure of a common
geometric endpoint.

It is primarily a measured standoff between:

1. the final clean continuous-spiral sample; and
2. the independently acquired centre of the terminal shared node.

## Consequence for spiral modelling

The continuous trace and the lower-right node must remain separate
observational objects.

For subsequent reciprocal-spiral reconstruction:

- the visible continuous spiral may constrain curve shape;
- the last S10 sample must not be forced to be the mathematical outer
  endpoint;
- the lower-right shared node may be tested separately as a candidate
  limiting/terminal source landmark;
- no model may be calibrated by snapping S10 to that node.

Likewise, the inner landmark remains an independent source-level endpoint
check rather than a compulsory calibration point.

## Interpretation boundary

This checkpoint does not establish:

- r*theta = 1;
- either frozen theta convention;
- a spherical construction map;
- a coordinate system;
- exact endpoint coincidence.

It preserves the distinction between visible clean trace, occluded
continuation, and independently acquired node landmarks.

