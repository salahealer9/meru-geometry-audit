# First Hand blind incidence-addendum digitizer

**Stage:** v0.8 post-census point addendum  
**Input:** three preregistered source-visible nodes  
**Output:** two separate three-row pass files

## Scope

The dedicated digitizer acquires only:

```text
AOG-LM-P07-X1-UC-LL-INTERSECTION
AOG-LM-P07-X1-UC-LR-INTERSECTION
AOG-LM-P07-YAXIS-UC-UCLR-INTERSECTION
```

It does not load:

```text
the other addendum pass
the provisional neutral census
the earlier overlay
the 30-degree angle result
great-circle traces or fits
a projective map
S1, S1.5, or S2
```

## Node guidance

### X1–UC–LL intersection

Click the centre of the filled node on the printed `x=1` great-circle
projection where it crosses the visible arc running from the upper
crossing toward the lower-left rim node.

Do not click the upper crossing, the lower-left rim node, or a point on
either adjacent stroke.

### X1–UC–LR intersection — UCLR

Click the centre of the filled node on the printed `x=1` great-circle
projection where it crosses the visible arc running from the upper
crossing toward the lower-right shared rim node.

This is the node called `UCLR`. It is the endpoint of the source radius
segment `r` from the central circular node.

Do not click the lower-right rim node or the nearby `r` label or arrow.

### Y-axis–UC–UCLR intersection

Click the centre of the separate filled node on the printed y-axis
great-circle projection where it crosses the visible arc from the upper
crossing toward UCLR.

This is not the central circular node. The printed y-axis visually
passes through both the central node and this separate node.

## List the nodes

```bash
python scripts/digitize_first_hand_incidence_addendum.py \
  --list
```

## Pass 1

```bash
python scripts/digitize_first_hand_incidence_addendum.py \
  --pass-number 1 \
  --operator "Salah-Eddin Gherbi"
```

Each object receives exactly one click. Enter the approximate full
visible node width in pixels when prompted.

The file is:

```text
data/derived/first_hand_arm_of_god/
    diagram_incidence_addendum_pass1.csv
```

Validate it:

```bash
python scripts/digitize_first_hand_incidence_addendum.py \
  --validate \
  data/derived/first_hand_arm_of_god/diagram_incidence_addendum_pass1.csv
```

Do not inspect or compare its coordinates before pass 2.

## Pass 2

After a genuine visual break:

```bash
python scripts/digitize_first_hand_incidence_addendum.py \
  --pass-number 2 \
  --operator "Salah-Eddin Gherbi"
```

Validate:

```bash
python scripts/digitize_first_hand_incidence_addendum.py \
  --validate \
  data/derived/first_hand_arm_of_god/diagram_incidence_addendum_pass2.csv
```

The pass-2 collection reads only its own partial output when resuming. It
does not load pass 1.

## Correcting one point

```bash
python scripts/digitize_first_hand_incidence_addendum.py \
  --pass-number 1 \
  --operator "Salah-Eddin Gherbi" \
  --landmark-id AOG-LM-P07-X1-UC-LR-INTERSECTION \
  --replace
```

Record the correction reason in the operator note.

## Data boundary

The original neutral pass files remain unchanged. The new addendum files
are frozen separately before any angle or incidence computation.
