# First Hand spherical spiral segment correspondence

**Checkpoint:** v0.8  
**Status:** source-topological correspondence frozen before cross-pass distance calculation

## Inputs

Two independently sealed raw acquisitions:

    Pass 1: 214 rows, 10 segments
    Pass 2: 229 rows, 10 segments

Metadata-only QC outcome:

    QC_NONE_REQUIRED

No cross-pass coordinate distance, fitting, registration, or theoretical
spiral geometry was used to establish correspondence.

## Correspondence rule

Pair segments only from:

- acquisition order;
- source-visible start feature;
- source-visible end feature;
- occlusion/crossing topology;
- acquisition notes stripped of theoretical/angular interpretation.

The following information is explicitly not used:

- numerical proximity between passes;
- 30-degree geometry;
- 360-degree winding claims;
- r*theta = 1;
- coordinate-map predictions;
- scaffold predictions;
- endpoint-consensus coordinates.

## Frozen correspondence

### S01

Pass 1:

    central/innermost region
        ->
    dashed back-hemisphere Y0 interruption

Pass 2:

    central/innermost region
        ->
    dashed back-hemisphere Y0 interruption

Classification:

    ONE_TO_ONE

Pair:

    P1:S01 <-> P2:S01

---

### S02

Pass 1:

    dashed back-hemisphere Y0
        ->
    YAXIS

Pass 2:

    dashed back-hemisphere Y0
        ->
    YAXIS

Classification:

    ONE_TO_ONE

Pair:

    P1:S02 <-> P2:S02

---

### S03

Pass 1:

    YAXIS
        ->
    visible radial source line through the white-marker / UCLR region

Pass 2:

    YAXIS
        ->
    visible radial source line through the white-marker / UCLR region

Classification:

    ONE_TO_ONE

Pair:

    P1:S03 <-> P2:S03

Note:

    The raw acquisition notes additionally describe this radial line using
    an angular value. That value is not used here.

---

### S04

Pass 1:

    radial source line through white-marker / UCLR region
        ->
    Y0

Pass 2:

    radial source line through white-marker / UCLR region
        ->
    Y0

Classification:

    ONE_TO_ONE

Pair:

    P1:S04 <-> P2:S04

---

### S05

Pass 1:

    Y0
        ->
    YAXIS

Pass 2:

    Y0
        ->
    YAXIS

Classification:

    ONE_TO_ONE

Pair:

    P1:S05 <-> P2:S05

Note:

    Raw notes contain an interpretive winding description.
    It is not used to establish correspondence.

---

### S06

Pass 1:

    YAXIS
        ->
    dashed back-hemisphere Y0

Pass 2:

    YAXIS
        ->
    dashed back-hemisphere Y0

Classification:

    ONE_TO_ONE

Pair:

    P1:S06 <-> P2:S06

---

### S07

Pass 1:

    dashed back-hemisphere Y0
        ->
    YAXIS

Pass 2:

    dashed back-hemisphere Y0
        ->
    YAXIS

Classification:

    ONE_TO_ONE

Pair:

    P1:S07 <-> P2:S07

---

### S08

Pass 1:

    YAXIS
        ->
    white marker

Pass 2:

    YAXIS
        ->
    white marker

Classification:

    ONE_TO_ONE

Pair:

    P1:S08 <-> P2:S08

---

### S09

Pass 1:

    white marker
        ->
    X1 / UCLR region

Pass 2:

    white marker
        ->
    X1 / UCLR region

Classification:

    ONE_TO_ONE

Pair:

    P1:S09 <-> P2:S09

---

### S10

Pass 1:

    X1 / UCLR region
        ->
    Y0 / lower-right rim region

Pass 2:

    X1 / UCLR region
        ->
    Y0 / lower-right rim region

Classification:

    ONE_TO_ONE

Pair:

    P1:S10 <-> P2:S10

---

# Correspondence summary

Resolved source runs:

    10

ONE_TO_ONE:

    10

PASS1_SPLIT:

    0

PASS2_SPLIT:

    0

MANY_TO_MANY:

    0

UNRESOLVED:

    0

No visible source length is excluded from the primary reproducibility
analysis on correspondence grounds.

## Interpretation boundary

The equality of segment counts alone was not used to establish correspondence.

The one-to-one mapping is supported by independently recorded source-visible
boundary topology in both acquisitions.

This ledger does not establish geometric agreement between paired segments.

That question remains unopened until this correspondence is frozen.

