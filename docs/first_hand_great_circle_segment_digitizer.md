# First Hand segment-aware labelled-curve digitizer

**Stage:** v0.8 source-curve acquisition  
**Status:** implementation checkpoint before curve observations  
**Scope:** four labelled internal curves only

## Why a separate digitizer is required

The generic diagram digitizer records an open curve as one ordered
polyline. That representation is unsuitable for the page-7 labelled
curves because node blobs, labels, arrows, the thick reciprocal spiral,
and uncertain crossings interrupt their visible centrelines.

The segment-aware tool gives every separately visible fragment its own:

```text
segment_id
```

No segment is joined to another across an occlusion or uncertain region.

## Frozen curve vocabulary

```text
AOG-LM-P07-GC-Y0
AOG-LM-P07-GC-Y1
AOG-LM-P07-GC-YAXIS
AOG-LM-P07-GC-X1
```

All four must remain:

```text
status = preregistered_later_stage
object_type = open_curve
```

## Output schema

```text
crop_id
crop_file_sha256
crop_pixel_sha256
landmark_id
pass_number
operator
segment_id
sequence_index
x_px
y_px
local_stroke_width_px
source_feature
operator_note
timestamp_utc
```

Output files:

```text
data/derived/first_hand_arm_of_god/
    great_circle_segments_pass1.csv
    great_circle_segments_pass2.csv
```

## Sampling floors

Each visible fragment requires at least:

```text
4 ordered centreline points
```

Each labelled curve requires at least:

```text
12 total points across all of its segments
```

These are acquisition floors, not claims about mathematical smoothness.

## Segment-break rule

Start a new segment whenever the visible centreline is interrupted or
ambiguous because of:

```text
filled node blobs
the thick reciprocal spiral
labels or leader lines
arrows
gaps
uncertain crossings
```

Never interpolate a hidden continuation.

### GC-Y0

The curve is the labelled `y=0` projection, identified in the source as
the x-axis. Break specifically at the central `r`-arrow entanglement.

### GC-Y1

Trace only unambiguous labelled `y=1` fragments. Break around node blobs,
the reciprocal spiral, labels, arrows, and uncertain crossings.

### GC-YAXIS

Trace only visible fragments of the labelled y-axis projection. Break
around the central filled circular node and the separate y-axis
incidence node rather than clicking through either blob.

### GC-X1

Trace only visible fragments of the labelled `x=1` projection. Break
around both registered x=1 incidence nodes rather than connecting
through them.

## Blindness boundary

The GUI shows only the untouched verified source crop. It does not show
or load:

```text
the other curve pass
earlier segments as an overlay
neutral-census points or fits
the expanded-census overlay
projective-map candidates
great-circle or conic fits
residuals
S1, S1.5, or S2 results
```

The terminal may state source labels and exclusion rules, but it does not
print or display measured landmark coordinates.

## Controls

For each visible segment:

```text
left click      add ordered centreline point
right click     remove latest point
middle click    finish this segment
Enter           finish this segment
```

After a segment closes, the terminal asks whether another disconnected
visible fragment belongs to the same labelled curve.

A complete landmark is written only after all of its segments satisfy
the sampling floors. This prevents an interrupted fragment from being
mistaken for a frozen completed curve.

## List the four curves

```bash
python scripts/digitize_first_hand_great_circle_segments.py \
  --list
```

## Pass 1

```bash
python scripts/digitize_first_hand_great_circle_segments.py \
  --pass-number 1 \
  --operator "Salah-Eddin Gherbi"
```

Validate:

```bash
python scripts/digitize_first_hand_great_circle_segments.py \
  --validate \
  data/derived/first_hand_arm_of_god/great_circle_segments_pass1.csv
```

Do not inspect, plot, compare, average, or fit pass 1 before pass 2.

## Pass 2

After a genuine visual break:

```bash
python scripts/digitize_first_hand_great_circle_segments.py \
  --pass-number 2 \
  --operator "Salah-Eddin Gherbi"
```

Validate:

```bash
python scripts/digitize_first_hand_great_circle_segments.py \
  --validate \
  data/derived/first_hand_arm_of_god/great_circle_segments_pass2.csv
```

Pass 2 never loads pass 1.

## Replacing one completed curve

```bash
python scripts/digitize_first_hand_great_circle_segments.py \
  --pass-number 1 \
  --operator "Salah-Eddin Gherbi" \
  --landmark-id AOG-LM-P07-GC-Y0 \
  --replace
```

The previous rows remain intact until the complete replacement has
passed validation.

## Interpretation boundary

This acquisition stage does not decide whether any printed curve is
exactly a circle, conic, projected great circle, or image of a particular
planar coordinate line. It creates the source observations needed for
those later tests.

## Spherical-panel domain boundary

Only the visible centreline at or inside the outer equator-at-horizon
limb belongs to the spherical projected-curve observation.

A straight or curved continuation outside that limb which terminates in
an arrow or supports a text label is an annotation leader and must not
be digitized, even when it is collinear with the in-sphere curve.

At a filled rim node, stop the curve samples before entering the node
blob. The separately digitized node landmark supplies the incidence
location.

For `GC-Y0`, the exterior continuation beyond the lower-right shared
node is excluded. The three or more interior segments should cover only
the unambiguous visible portions inside the spherical panel.

## GC-Y0 dashed back-hemisphere continuation

The dashed diagonal between the upper-left rim node and the central
region is included as the back-hemisphere continuation of `GC-Y0`.

Regular gaps between the small printed dash marks are a rendering style,
not unknown geometry. Samples from one uninterrupted dashed run therefore
remain under one `segment_id`.

A new segment is required where the dashed run is interrupted by the
thick reciprocal spiral, a filled node, or another genuine occlusion.

The exterior arrow-bearing continuation beyond the spherical horizon
remains excluded.
