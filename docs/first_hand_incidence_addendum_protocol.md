# First Hand incidence-landmark addendum

**Stage:** v0.8 post-neutral-census amendment  
**Status:** preregistered before addendum digitization  
**Scope:** three additional filled internal nodes only

## Discovery boundary

The original neutral landmark passes were committed before the first
neutral-census overlay was inspected. Overlay inspection revealed three
additional filled internal incidence nodes that improve fidelity to the
published diagram.

The original pass files remain immutable:

```text
data/derived/first_hand_arm_of_god/
    diagram_landmarks_pass1.csv
    diagram_landmarks_pass2.csv
    diagram_landmark_passes.sha256
```

The new nodes are not appended to those files.

## Central-node morphology correction

The existing stable landmark:

```text
AOG-LM-P07-CENTRAL-REFERENCE-NODE
```

is a **filled circular node**, not a square.

Its source description is corrected while its original clicks and
coordinates remain unchanged. It remains neutral with respect to the
fitted image centre, chart origin, and projection pole.

## Added point landmarks

### `AOG-LM-P07-X1-UC-LL-INTERSECTION`

The filled node on the printed `x=1` great-circle projection where it
intersects the visible arc running from the upper crossing toward the
lower-left rim node.

No hidden continuation or rim endpoint is assigned in advance.

### `AOG-LM-P07-X1-UC-LR-INTERSECTION`

The filled node on the printed `x=1` great-circle projection where it
intersects the visible arc running from the upper crossing toward the
lower-right shared rim node.

This node has the workflow alias:

```text
UCLR
```

The source radius segment `r` is visually defined from the central
circular node toward UCLR.

### `AOG-LM-P07-YAXIS-UC-UCLR-INTERSECTION`

The filled node on the printed y-axis great-circle projection where it
intersects the visible arc running from the upper crossing toward UCLR.

It is distinct from the central circular node. The printed y-axis
visually passes through both points.

## Status and acquisition

All three rows use:

```text
status = preregistered_incidence_addendum
object_type = point
minimum_samples = 2
```

Each node receives one click in addendum pass 1 and one independent
click in addendum pass 2.

The addendum pass files will be separate:

```text
diagram_incidence_addendum_pass1.csv
diagram_incidence_addendum_pass2.csv
```

No addendum pass data exist at this protocol checkpoint.

## Uncertainty

For each node:

```text
consensus = (pass1 + pass2) / 2

uncertainty = max(
    2 px,
    visible node radius,
    half the inter-pass separation
)
```

## Node-defined 30-degree diagnostic

The expanded census may evaluate:

```text
angle(UCLR, central, LR)
```

where:

- `central` is `AOG-LM-P07-CENTRAL-REFERENCE-NODE`;
- `UCLR` is `AOG-LM-P07-X1-UC-LR-INTERSECTION`;
- `LR` is `AOG-LM-P07-RIM-NODE-LR-SHARED`.

This is a direct three-point image-space angle. It is distinct from the
ambiguous printed 30-degree arc, which remains deferred.

## Y-axis diagnostic

The expanded census may measure the image-space alignment of:

```text
central circular node
y-axis addendum node
```

and later compare both points against the segment-aware printed y-axis
trace.

This does not assume that the line is a Euclidean diameter or that the
map is angle preserving.

## Interpretation boundary

This amendment registers source-visible points only. It introduces no:

```text
great-circle curve fit
hidden-curve interpolation
projective-map selection
unit-angle selection
truncation reconciliation
S1
S1.5
S2
```
