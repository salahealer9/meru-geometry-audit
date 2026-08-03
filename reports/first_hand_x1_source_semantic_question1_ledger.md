# First Hand X1 source-semantic audit — Question 1 ledger

**Checkpoint:** v0.8  
**Question:** Does the printed `x=1` annotation unambiguously designate the
visible stroke frozen as `AOG-LM-P07-GC-X1`?

**Status:** completed source-semantic visual classification; Question-1 outcome selected before opening Question 2.

## Evidence boundary

Use only:

- `01_source_context.png`
- `02_x1_label_region_source_only.png`
- `03_x1_frozen_trace_points_overlay.png`
- the five `segment_*_source_only.png` images
- the five corresponding `segment_*_overlay.png` images
- the frozen acquisition notes

Do not use:

- eta_x
- equatorial-incidence residuals
- 30-degree guides
- circle fits
- scaffold fits
- predicted x=1 geometry
- construction-scale hypotheses

Source semantics identify the stroke; geometric fit does not.

## Review order

For each segment:

1. inspect `source_only` first;
2. record visible source topology;
3. classify crossings/occlusions;
4. only then inspect the overlay;
5. decide whether the frozen points follow the same visible stroke.

Allowed continuity classes:

- `VISIBLE_CONTINUATION`
- `AMBIGUOUS_CONTINUATION`
- `OCCLUDED_OR_UNRESOLVED`
- `NOT_RELEVANT`

Allowed segment identity classes:

- `CONFIRMED`
- `PROBABLE`
- `AMBIGUOUS`
- `CONTRADICTED`

---

## Printed x=1 annotation

### Source-only observations

Printed text location:

    Near the middle-right node of the spherical diagram

Leader / pointer present:

    Yes — a short line connects the label to the curve

Leader endpoint or apparent target:

    Points directly to the middle-right node at the outer boundary, endpoint of the frozen X1 stroke

Local stroke identified without geometric inference:

    The curve immediately below the label — same as the frozen trace

Initial label-to-stroke assessment:

    CONFIRMED — the label clearly designates the traced stroke

Notes:

    No ambiguity in the label-to-stroke relationship

---

# Segment review

## S01

Frozen acquisition description:

    solid front-side run from the middle-left filled node toward the UCLL node

Source-only file:

    segment_01_S01_source_only.png

Overlay file:

    segment_01_S01_overlay.png

Visible start feature:

    Middle-left filled node on the horizon limb

Visible end feature:

    UCLL filled node

Relevant crossings / occlusions:

    None — stroke is clearly visible between nodes

Continuity classification:

    VISIBLE_CONTINUATION

Does frozen overlay remain on the source-visible stroke?

    Yes

Segment identity class:

    CONFIRMED

Evidence note:

    The frozen trace follows the visible stroke exactly from the middle-left node to the UCLL node.

---

## S02

Frozen acquisition description:

    solid front-side run from the UCLL node toward the projected y=0
    (x-axis) great circle

Source-only file:

    segment_02_S02_source_only.png

Overlay file:

    segment_02_S02_overlay.png

Visible start feature:

    UCLL filled node

Visible end feature:

    Intersection with the projected y=0 (x-axis) great circle

Relevant crossings / occlusions:

    Crosses the y=0 great circle at the end of the segment

Continuity classification:

    VISIBLE_CONTINUATION

Does frozen overlay remain on the source-visible stroke?

    Yes

Segment identity class:

    CONFIRMED

Evidence note:

    The frozen trace follows the visible stroke from UCLL node to the y=0 crossing. The stroke remains clearly visible throughout.

---

## S03

Frozen acquisition description:

    solid front-side run from the projected y=0 (x-axis) crossing toward
    the spiral occlusion near the UCLR node

Source-only file:

    segment_03_S03_source_only.png

Overlay file:

    segment_03_S03_overlay.png

Visible start feature:

    Intersection with the projected y=0 (x-axis) great circle

Visible end feature:

    Spiral occlusion / UCLR node region (stroke disappears behind the thick spiral)

Relevant crossings / occlusions:

    Ends at a spiral occlusion — the stroke goes behind the thick spiral

Continuity classification:

    OCCLUDED_OR_UNRESOLVED

Does frozen overlay remain on the source-visible stroke?

    Yes — up to the occlusion point

Segment identity class:

    CONFIRMED

Evidence note:

    The frozen trace follows the visible stroke from the y=0 crossing to the point where the thick spiral occludes it. The stroke is clearly visible before the occlusion.

---

## S04

Frozen acquisition description:

    solid front-side run from near the UCLR node toward the printed
    theta = 1 MONTH annotation

Source-only file:

    segment_04_S04_source_only.png

Overlay file:

    segment_04_S04_overlay.png

Visible start feature:

    UCLR node region (resumes after spiral occlusion)

Visible end feature:

    Printed theta = 1 MONTH annotation region

Relevant crossings / occlusions:

    Resumes after the spiral occlusion; ends near the annotation text

Continuity classification:

    VISIBLE_CONTINUATION

Does frozen overlay remain on the source-visible stroke?

    Yes — the stroke is clearly visible between the UCLR node and the annotation

Segment identity class:

    CONFIRMED

Evidence note:

    The frozen trace follows the visible stroke from the UCLR node to the theta = 1 MONTH annotation. The stroke remains clear throughout.

---

## S05

Frozen acquisition description:

    solid front-side run from the theta = 1 MONTH annotation region toward
    the middle-right filled node on the horizon limb

Source-only file:

    segment_05_S05_source_only.png

Overlay file:

    segment_05_S05_overlay.png

Visible start feature:

    Theta = 1 MONTH annotation region

Visible end feature:

    Middle-right filled node on the horizon limb

Relevant crossings / occlusions:

    None — stroke remains visible from the annotation to the horizon node

Continuity classification:

    VISIBLE_CONTINUATION

Does frozen overlay remain on the source-visible stroke?

    Yes — the stroke is clearly visible and the overlay follows it exactly

Segment identity class:

    CONFIRMED

Evidence note:

    The frozen trace follows the visible stroke from the theta = 1 MONTH annotation to the middle-right horizon node. No ambiguity or occlusion.

---

# Cross-segment continuity ledger

## S01 -> S02

Boundary feature:

    UCLL node

Continuity status:

    VISIBLE_CONTINUATION

Evidence:

    The two segments meet at the UCLL filled node. The visible stroke is continuous through the node, and the frozen trace follows it without interruption.

## S02 -> S03

Boundary feature:

    projected y=0 (x-axis) crossing

Continuity status:

    VISIBLE_CONTINUATION

Evidence:

    The two segments connect at the y=0 great circle crossing. The stroke passes through the intersection and continues clearly on the other side.

## S03 -> S04

Boundary feature:

    spiral / UCLR occlusion region

Continuity status:

    OCCLUDED_OR_UNRESOLVED

Evidence:

    The stroke disappears behind the thick spiral near the UCLR node. S03 ends at the occlusion; S04 resumes after the UCLR node. The spiral and the UCLR node touch each other, so no new segment is possible between the two. The frozen trace does not invent the hidden portion.

## S04 -> S05

Boundary feature:

    theta = 1 MONTH annotation region

Continuity status:

    VISIBLE_CONTINUATION

Evidence:

    The stroke passes through the annotation region without interruption. S04 ends near the label; S05 continues from the same visible stroke up to the middle right node.

---

# Question-1 outcome

Select exactly one only after all five segments and four inter-segment
boundaries have been reviewed.

    [X] X1_LABEL_TRACE_CONFIRMED
    [ ] X1_LABEL_TRACE_AMBIGUOUS
    [ ] X1_LABEL_TRACE_CONTRADICTED
    [ ] X1_LABEL_NOT_RESOLVABLE

Justification:

    The printed x=1 label unambiguously designates the source-visible stroke represented by the frozen five-segment X1 trace. Visual inspection of the source-only and overlay crops confirms that the label's leader identifies this stroke and that every frozen segment remains on it wherever the stroke is visible. The S01→S02, S02→S03, and S04→S05 boundaries are visibly continuous. At S03→S04, the stroke is hidden by the thick spiral / UCLR region, so continuity through the hidden interval is not directly observed; the frozen acquisition appropriately stops before the occlusion and resumes only where the stroke becomes visible again. No source-visible alternative branch is indicated at any reviewed visible crossing.

## Interpretation boundary

This ledger decides only whether the printed `x=1` annotation supports the
existing frozen X1 trace.

It does not decide whether X1 is:

- a mathematically valid affine x=1 curve;
- a cube-octahedral scaffold curve;
- compatible with a 30-degree construction;
- compatible with a later three-curve reconstruction.

Question 2, scaffold-role evidence, remains unopened until this result is
frozen.
