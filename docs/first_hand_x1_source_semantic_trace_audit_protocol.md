# First Hand X1 source-semantic trace audit

**Version:** v0.8.0  
**Status:** protocol frozen before focused X1 source-semantic review  
**Analysis class:** post-hoc source-semantic audit  
**Primary source:** Arm of God, page 7

## Purpose

The frozen geometric analyses established that the trace registered as

    AOG-LM-P07-GC-X1

is:

- reproducibly digitized after acquisition QC;
- strongly curved rather than line-like;
- well described as a circular stereographic great-circle trace;
- metrically one of the cleaner spherical rendering curves;
- but incompatible with the printed y-axis as an affine-parallel x-family
  under the tested equator-preserving central-projective construction.

The frozen parallel-family diagnostic found approximately:

    x-family equatorial departure:
        26.58 degrees

while the y-family approximately satisfies the corresponding incidence
condition and recovers its previously registered projective-infinity rim
landmark.

This audit does not attempt to repair that result.

Its purpose is to answer two source-semantic questions.

## Question 1 — label-to-stroke identity

Does the printed label

    x=1

unambiguously designate the exact visible stroke that was frozen and
digitized as

    AOG-LM-P07-GC-X1

?

## Question 2 — scaffold-role evidence

Independently of Question 1, does the page itself provide graphical or
textual evidence that the same visible stroke belongs to the
cube-octahedral great-circle scaffold?

These questions must be answered separately.

A confirmed x=1 identity does not by itself establish a scaffold role.

A scaffold-like geometric fit does not by itself establish a source
scaffold role.

## Post-hoc status

This audit is motivated by the already-observed x-family geometric
inconsistency.

It is therefore post-hoc with respect to the geometric result.

However, the semantic review must be performed without using geometric
fit quality to decide which visible stroke the label refers to.

The following already-known numerical facts must not be used as
label-identification criteria:

- eta_x;
- equatorial-departure angle;
- the approximately 30-degree horizontal-projection azimuth;
- X1 circle radius;
- X1 radius / limb-radius ratio;
- proximity to sqrt(2);
- any predicted x=1 curve from a later model;
- any scaffold residual;
- any construction-scale candidate.

## Frozen source identity

The primary source is the already-frozen Arm of God PDF and its frozen
page-7 prepared crop.

No replacement scan, redrawing, web reproduction, or later secondary
illustration may replace the frozen source in the primary audit.

The source registry presently records:

    AOG-LM-P07-GC-X1

as the printed curve labelled

    x=1

with no preregistered rim-node assignment.

That registry entry remains unchanged during this audit.

## Frozen trace identity

The existing two-pass X1 digitization remains immutable.

No trace point is added, removed, moved, or reclassified during this
checkpoint.

The QC-corrected acquisition derivative remains the authoritative
reproducibility result.

The obsolete pre-QC duplicate-input-burst residuals are not evidence
against the X1 trace.

## Allowed evidence for Question 1

Only source-visible semantic and topological evidence may be used.

Allowed evidence includes:

1. physical placement of the printed `x=1` text;
2. a visible leader line, arrow, pointer, or termination associated with
   that label;
3. direct visual contact between the label annotation and a stroke;
4. visible local stroke continuity on either side of the labelled region;
5. distinguishable crossings where one continuation is graphically
   continuous and another is not;
6. line weight or rendering convention if it visibly distinguishes
   different source objects;
7. occlusion order if genuinely visible;
8. whether the frozen traced segments lie on the same continuously visible
   stroke identified at the label.

## Forbidden evidence for Question 1

Do not identify the labelled stroke using:

- expected projective geometry;
- expected parallelism;
- expected great-circle endpoints;
- expected 30-degree or 60-degree scaffold directions;
- residual minimization;
- circle-fit quality;
- line-fit quality;
- predicted coordinate curves;
- a preferred construction scale;
- the fact that another stroke would produce a better model.

The rule is:

> source semantics identify the stroke; geometry does not.

## Crossing rule

At every crossing relevant to the X1 trace, classify continuity as one of:

    VISIBLE_CONTINUATION
    AMBIGUOUS_CONTINUATION
    OCCLUDED_OR_UNRESOLVED
    NOT_RELEVANT

A continuation may be called visible only when the printed stroke itself
supports that judgment.

No hidden continuation is invented.

## Segment-level audit

Review each frozen X1 segment independently.

For every segment record:

    segment_id
    visibly_on_labelled_x1_stroke
    confidence_class
    evidence_note
    nearest_relevant_crossing
    continuity_status

The allowed confidence classes are:

    CONFIRMED
    PROBABLE
    AMBIGUOUS
    CONTRADICTED

No numerical probability is assigned.

## Overall Question-1 outcomes

Exactly one of the following must be selected.

### X1_LABEL_TRACE_CONFIRMED

The printed x=1 annotation and visible stroke topology unambiguously
support the frozen X1 trace.

This means the geometric x-family inconsistency remains a genuine feature
of the source-labelled construction under the tested model.

### X1_LABEL_TRACE_AMBIGUOUS

The printed x=1 annotation identifies a local stroke, but one or more
crossings or hidden continuations prevent a unique association with the
full frozen X1 trace.

The geometric trace remains valid as a visible curve, but its complete
coordinate identity becomes source-semantically uncertain.

### X1_LABEL_TRACE_CONTRADICTED

The printed source visibly demonstrates that one or more frozen X1
segments follow a different branch from the stroke designated x=1.

This outcome requires positive source-visible evidence.

A better geometric fit by another branch is not sufficient.

If selected, this checkpoint still does not modify the trace.

Any corrective acquisition requires a new, separately frozen protocol.

### X1_LABEL_NOT_RESOLVABLE

The source quality or annotation is insufficient even to decide between
confirmation and contradiction.

## Question 2 — scaffold-role evidence

After Question 1 is completed and frozen within the audit record, examine
whether the same source stroke has an explicit or graphically supportable
scaffold role.

Allowed scaffold-role evidence includes:

1. textual source wording explicitly identifying the stroke or its family
   as part of the cube-octahedral great-circle framework;
2. visible continuity from the x=1-labelled stroke into an otherwise
   explicitly identified scaffold arc;
3. a shared graphical convention that is explicitly explained by the
   source;
4. a source-visible junction or continuation demonstrating that the
   coordinate-labelled stroke and a scaffold stroke are the same drawn
   object.

Geometric similarity alone is not sufficient.

Specifically, none of the following establishes source scaffold identity:

- radius ratio near sqrt(2);
- approximately 30-degree azimuth;
- similarity to the independent scaffold holdout;
- circle-fit residual;
- agreement with a reconstructed cuboctahedral grid.

## Question-2 outcomes

Exactly one of:

    SCAFFOLD_ROLE_EXPLICIT
    SCAFFOLD_ROLE_GRAPHICALLY_SUPPORTED
    SCAFFOLD_ROLE_AMBIGUOUS
    SCAFFOLD_ROLE_NOT_SUPPORTED_BY_SOURCE

`NOT_SUPPORTED_BY_SOURCE` does not mean that a later geometric scaffold
hypothesis is false.

It means only that page-7 source semantics do not establish that role.

## Review-image rules

Permitted viewing transformations are limited to:

- zoom;
- lossless crop;
- nearest-neighbour or ordinary display enlargement;
- brightness/contrast adjustment applied uniformly;
- grayscale conversion;
- a neutral overlay marking already-frozen trace points or segment IDs.

No fitted circle, predicted great circle, coordinate map, scaffold model,
30-degree radial line, or alternative candidate trace may be overlaid
during the primary semantic classification.

Any neutral overlay must be clearly labelled as an annotation and must
not alter the source pixels.

## Evidence chronology

The audit must preserve this order:

1. inspect frozen source and frozen X1 trace topology;
2. decide Question 1;
3. freeze the Question-1 evidence statement;
4. inspect source evidence relevant to possible scaffold role;
5. decide Question 2;
6. only after both source-semantic outcomes are recorded may the result be
   compared with the already-known geometric diagnostics.

This prevents the scaffold hypothesis from deciding the x=1 identity.

## Required evidence record

Produce a report containing:

### Source provenance

- source PDF identity and SHA-256;
- page number;
- prepared crop identity and SHA-256 if used;
- existing X1 trace artifact identity;
- existing X1 trace seal identity.

### Question 1

- printed label location description;
- presence/absence of leader or pointer;
- local label-to-stroke relationship;
- segment-by-segment continuity ledger;
- relevant crossing ledger;
- overall outcome;
- concise justification.

### Question 2

- source textual evidence, if any;
- source graphical evidence, if any;
- distinction between explicit evidence and geometric inference;
- overall outcome;
- concise justification.

### Existing geometry carried only as context after semantic decisions

Record, but do not use to determine the semantic outcomes:

    prior eta_x
    prior x-family equatorial departure
    prior X1 stereographic rendering closure

## No silent correction

If the result is

    X1_LABEL_TRACE_CONTRADICTED

the present frozen digitization is retained unchanged as historical
evidence.

A correction may only occur in a later checkpoint with:

- explicit reason;
- source-supported branch definition;
- new acquisition protocol;
- new raw data;
- separate provenance;
- separate result identifier.

No existing artifact is overwritten.

## Interpretation boundary

This checkpoint may establish only what the source drawing supports about:

1. the identity of the stroke labelled x=1;
2. whether the same stroke has an explicit or graphically supported
   scaffold role.

It does not establish:

- whether Tenen intended a mathematically exact affine coordinate chart;
- whether the page was drawn from an exact hidden construction;
- whether the stroke is approximately compatible with a cuboctahedral
  model;
- whether isotropy should be imposed;
- which construction scale is correct;
- whether a different projective map repairs the x-family;
- reciprocal-spiral correspondence;
- S1;
- S1.5;
- S2.

## Decision after this checkpoint

### If X1_LABEL_TRACE_CONFIRMED

Preserve the x-family inconsistency as a source-labelled structural
result.

Then a separately declared post-hoc three-curve candidate reconstruction
may be constructed from Y0, YAXIS, and Y1, with X1 evaluated only as a
post-hoc prediction.

### If X1_LABEL_TRACE_AMBIGUOUS or X1_LABEL_NOT_RESOLVABLE

Downgrade the full X1 coordinate identity to a source-semantic ambiguity.

Do not silently replace it.

A later alternative-branch study must enumerate source-supported
possibilities rather than choose the best-fitting one.

### If X1_LABEL_TRACE_CONTRADICTED

Freeze the contradiction report first.

Only afterwards preregister a corrective trace acquisition.

### Scaffold role

Regardless of the Question-1 result, do not call X1 a scaffold curve
unless Question 2 provides source-semantic support or a later separately
preregistered geometric scaffold test establishes compatibility.

