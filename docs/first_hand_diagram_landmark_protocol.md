# First Hand diagram landmark and uncertainty protocol

**Version:** v0.8.0 semantic revision 2  
**Status:** preregistered; no valid landmark pass files exist  
**Primary crop:** `AOG_P07_SPHERICAL_PROJECTION`

## Reason for revision

The first landmark vocabulary assigned coordinate meanings to particular
rim nodes before the published curves had been measured. That was too
strong. The revised protocol separates three evidential layers:

1. neutral visible geometry;
2. printed curve labels and incidences;
3. later mathematical interpretation.

No rim node is assigned to `x=1`, the y-axis, `y=0`, or `y=1` merely from
its apparent bearing.

## One source object, one weight

The outer circular limb is explicitly labelled `Equator Great Circle
(at horizon)`. It is one sampled object serving two semantic roles:
image-sphere boundary and equator-at-horizon.

The lower-right rim node is likewise one geometric point with several
source roles: a rim node, the visible meeting point of the labelled
`y=0` and `y=1` curves, and the visible outer terminus of the thick
spiral. It is digitized and weighted once.

## Initial neutral census

The first two independent passes contain only rows whose registry status
is:

```text
preregistered_not_digitized
```

These are:

- the equator-at-horizon limb;
- six neutral rim nodes;
- the central filled circular reference node;
- the unlabelled upper interior crossing;
- the flat-panel unit marker;
- the spherical-panel unit marker;
- the flat-panel inner endpoint;
- and the spherical-panel inner endpoint.

This stage contains no great-circle traces, spiral traces, 30-degree arc,
or page-8 Hand boundaries.

## Curve-label stage

The four printed great-circle curves are legitimate source objects:

```text
GC-Y0
GC-Y1
GC-YAXIS
GC-X1
```

They remain `preregistered_later_stage`.

When activated, the operator follows only the stroke identified by the
printed label. Expected endpoints are not used to identify the curve.
Hidden continuations are not invented. The `GC-Y0` trace excludes the
central region where its stroke is entangled with the annotation arrow
labelled `r`.

## Unit-angle discrepancy

The flat and spherical panels contain separate unit markers:

```text
flat panel:
    r=1
    theta=1 radian, approximately 57 degrees

spherical panel:
    r=1
    theta=1 MONTH, linked in the drawing to approximately 30 degrees
```

They are separate landmarks. Their disagreement is a result to measure,
not an ambiguity to average away.

The annotated 30-degree arc remains deferred because its intended
endpoints are not sufficiently unambiguous in the source image.

## Truncation variants

Two non-equivalent source conventions remain frozen:

```text
AOG-PROSE:
    theta_outer -> 0+
    theta_inner = 3*pi

AOG-DIAGRAM:
    theta_outer = 1
    theta_inner = 1 + 3*pi
```

Both span 1.5 turns, but they define different curve segments and
different inner endpoint tangents.

The flat-panel inner endpoint represents the diagram convention. The
spherical-panel inner endpoint is a separate projected holdout.

## Coordinate convention

Digitization uses prepared-crop pixels:

```text
origin:      upper-left
x:           rightward
y:           downward
units:       pixels
point:       visual centre of the intended node or marker
curve:       middle of the intended stroke
```

Text, arrowheads, leader lines, and labels are never geometry.

## Blind acquisition

No theoretical curve, fitted great circle, projective overlay, residual,
pass comparison, or self-embedment score may be shown while clicking.

Each point receives one click in pass 1 and one independent click in
pass 2. Curves, when later activated, receive two independent traces.

Pass 1 must not be plotted, summarized, or inspected before pass 2 is
complete.

## Uncertainty

For a point with pass clicks `p1` and `p2`:

```text
consensus = (p1 + p2) / 2

sigma_point = max(
    registry floor,
    local visible node or stroke radius,
    0.5 * ||p1 - p2||
)
```

Curve uncertainty is the larger of the registry floor and local
half-stroke-width.

## First computation after consensus

The neutral-census result is limited to:

- circle or ellipse fit to the outer limb;
- rim-node bearings around the fitted centre;
- regular-sixfold residual as an empirical diagnostic;
- central-node offset from the fitted centre;
- upper-crossing location;
- panel-specific unit-marker positions;
- and panel-specific inner-endpoint positions.

It computes no projection-map fit, great-circle identity, scale
selection, S1, S1.5, or S2.

A sixfold rim arrangement is tested rather than assumed. Even if found,
it is reported first as a measured source feature, not automatically as
a unique cuboctahedral interpretation.

## Later fitting boundary

A general projective map may preserve incidences without preserving
right angles. Therefore apparent 60-degree rim spacing does not by
itself disprove a labelled coordinate construction.

Possible outcomes include:

- isotropic coordinate chart drawn schematically;
- non-isotropic projective gauge;
- alignment to a hexagonal or cuboctahedral scaffold;
- label or draughting inconsistency.

The audit must distinguish these possibilities rather than choosing one
from visual expectation.

## Scope

This revised protocol contains no landmark coordinates, fitted geometry,
projection verdict, scale selection, or self-embedment result.

## Post-census incidence-landmark addendum

Inspection of the first neutral-census overlay revealed three additional
filled internal nodes that were not part of the original blind-pass
vocabulary:

```text
AOG-LM-P07-X1-UC-LL-INTERSECTION
AOG-LM-P07-X1-UC-LR-INTERSECTION
AOG-LM-P07-YAXIS-UC-UCLR-INTERSECTION
```

The second x=1 node carries the workflow alias `UCLR`.

These landmarks are registered only after the original two neutral
passes were committed. They therefore use the distinct status:

```text
preregistered_incidence_addendum
```

They must be acquired in separate point-only pass files. The original
neutral pass CSV files and checksum manifest remain immutable.

The central source node is morphologically a filled circle, not a
square. Its stable ID remains unchanged. This terminology correction
does not alter its frozen coordinates.

The y-axis addendum node is distinct from the central circular node. The
printed y-axis visually passes through both points; that relation is
tested later as an image-space incidence or collinearity diagnostic.

The UCLR node also defines a source-geometric angle with the central
circular node and lower-right shared rim node:

```text
angle(UCLR, central, LR)
```

This node-defined angle may be compared with 30 degrees. The visually
ambiguous printed 30-degree arc remains deferred and is not revived by
this amendment.

No great-circle trace, projective map, scale choice, truncation
reconciliation, S1, S1.5, or S2 result is introduced by this addendum.
