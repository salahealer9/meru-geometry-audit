# First Hand blind two-pass digitizer

**Status:** implementation checkpoint  
**Scope:** source landmarks only; no model overlays or fit scores

## Files

```text
scripts/digitize_first_hand_diagram_landmarks.py
data/derived/first_hand_arm_of_god/
    diagram_landmarks_pass1.csv
    diagram_landmarks_pass2.csv
```

The script reads the preregistered landmark registry and the frozen crop
manifest. It verifies both the PNG file hash and canonical pixel hash
before displaying a crop.

It does not import the spherical-map audit or any self-embedment code.

## Controls

For point landmarks:

```text
left click once
```

The independent second click is made in the other pass.

For the 30-degree angular annotation:

```text
left click first endpoint
left click arc midpoint
left click second endpoint
```

For curves and contours:

```text
left click      add ordered point
right click     remove most recent point
middle click    finish
Enter           finish
```

The source crop is opened fresh for every landmark. Earlier landmarks,
the other pass, model curves, residuals, and fitted overlays are not
shown.

## Registry listing

```bash
python scripts/digitize_first_hand_diagram_landmarks.py \
  --list
```

## Pass 1

The default partitions are the page-7 calibration, scale-calibration,
and holdout objects. Page-8 Hand views remain excluded as external
holdouts.

```bash
python scripts/digitize_first_hand_diagram_landmarks.py \
  --pass-number 1 \
  --operator "Salah-Eddin Gherbi"
```

The script writes after every completed landmark, so an interrupted
session can be resumed with the same command. Existing landmarks are
skipped.

## Separation between passes

Do not inspect, plot, average, or fit pass 1 before pass 2 is complete.

A genuine separation is preferable. Close the digitizer and take a
break before starting pass 2. The second pass begins from untouched
source crops and does not load pass 1.

## Pass 2

```bash
python scripts/digitize_first_hand_diagram_landmarks.py \
  --pass-number 2 \
  --operator "Salah-Eddin Gherbi"
```

## Validate pass files

```bash
python scripts/digitize_first_hand_diagram_landmarks.py \
  --validate \
  data/derived/first_hand_arm_of_god/diagram_landmarks_pass1.csv

python scripts/digitize_first_hand_diagram_landmarks.py \
  --validate \
  data/derived/first_hand_arm_of_god/diagram_landmarks_pass2.csv
```

## Correcting one landmark

A correction must be explicit. This replaces only the selected landmark
in the selected pass file:

```bash
python scripts/digitize_first_hand_diagram_landmarks.py \
  --pass-number 1 \
  --operator "Salah-Eddin Gherbi" \
  --landmark-id AOG-LM-P07-GC-Y1 \
  --replace
```

The reason for replacement should be entered in the operator note.

## Restarting an entire pass

Use only when the pass is known to be invalid:

```bash
python scripts/digitize_first_hand_diagram_landmarks.py \
  --pass-number 1 \
  --operator "Salah-Eddin Gherbi" \
  --restart-pass
```

## External holdouts

The page-8 Hand boundaries are intentionally not included in the default
run. They may be digitized later, after the map, scale, truncation, and
three-copy construction are frozen:

```bash
python scripts/digitize_first_hand_diagram_landmarks.py \
  --pass-number 1 \
  --operator "Salah-Eddin Gherbi" \
  --partitions external_holdout
```

A corresponding independent pass 2 is then required.

## Data boundary

The two raw pass files preserve operator clicks. They should not be
manually edited. Consensus coordinates and uncertainty estimates belong
to a separate deterministic script after both passes are complete.

No projection or self-embedment verdict is issued by the digitizer.
