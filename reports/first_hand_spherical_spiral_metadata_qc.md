# First Hand spherical spiral metadata-only QC

**Checkpoint:** v0.8  
**Analysis class:** metadata-only acquisition QC  
**Outcome:** `QC_NONE_REQUIRED`

## Frozen inputs

Pass 1:

    data/derived/first_hand_arm_of_god/
    spherical_spiral_segments_pass1.csv

    214 rows
    10 visible segments

Pass 2:

    data/derived/first_hand_arm_of_god/
    spherical_spiral_segments_pass2.csv

    229 rows
    10 visible segments

Both raw passes were independently sealed before cross-pass comparison.

## Provenance consistency

Both passes use the same prepared source crop.

Crop file SHA-256:

    ef8b7d652edea5227166e54ca1bf6e81a4c02afd0d78c9d793e615a2db6906f6

Crop pixel SHA-256:

    afb1df2172f081fa426f2f86c56912079116f6441ba64df367861d00375fddc4

Operator in both passes:

    Salah-Eddin Gherbi

## Duplicate-event audit

Pass 1:

    exact repeated XY coordinates: 0
    exact repeated event keys:     0

Pass 2:

    exact repeated XY coordinates: 0
    exact repeated event keys:     0

No duplicate-event burst analogous to the earlier X1 acquisition artifact
is present.

## Segment integrity

Pass 1 contains:

    S01 through S10

Pass 2 contains:

    S01 through S10

Within every segment, sequence indices begin at zero and are contiguous.

No malformed segment numbering was observed.

## Stroke-width metadata

Every acquired segment in both passes records:

    local_stroke_width_px = 14

Therefore the frozen descriptive acquisition floor associated with these
segments is:

    max(2 px, 0.5 * 14 px) = 7 px

This value is a source-reading scale only.

It is not interpreted as a Gaussian standard deviation or confidence
interval.

## Acquisition notes

The two passes independently record the same sequence of visible source
boundaries.

Some raw operator notes contain interpretive source descriptions such as
"30 degrees" and "360 degrees completed."

Those notes remain preserved verbatim in the immutable raw acquisitions.

However, angular or theoretical wording is not used for segment
correspondence or reproducibility analysis.

Only source-visible start/end features and ordering are used.

## QC decision

No objective acquisition-system or data-integrity artifact has been found.

Therefore:

    QC_NONE_REQUIRED

No point is excluded.

No derived QC coordinate file is created.

The two sealed raw pass CSV files are the authoritative inputs to the
reproducibility analysis.

## Interpretation boundary

This QC result concerns acquisition integrity only.

It says nothing about:

- agreement between the two traces;
- the reciprocal-spiral equation;
- spherical-map correctness;
- coordinate geometry;
- scaffold geometry;
- endpoint agreement.

No cross-pass geometric distance was computed in reaching this decision.

