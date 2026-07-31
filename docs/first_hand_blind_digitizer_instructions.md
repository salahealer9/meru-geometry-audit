# First Hand blind two-pass digitizer

**Status:** revised neutral-census workflow  
**Scope:** source geometry only; no model overlays or fit scores

## Initial default run

The registry now uses status to separate acquisition stages.

The default run selects only:

```text
preregistered_not_digitized
```

That initial set contains the horizon limb, six neutral rim nodes, the
central reference node, upper interior crossing, two separate unit
markers, and two separate inner endpoints.

It excludes:

```text
preregistered_later_stage
deferred_source_ambiguous
preregistered_external_holdout
```

Therefore the four great-circle traces, both spiral traces, the
ambiguous 30-degree arc, and page-8 Hand views do not enter the initial
passes.

## Pass 1

```bash
python scripts/digitize_first_hand_diagram_landmarks.py \
  --pass-number 1 \
  --operator "Salah-Eddin Gherbi"
```

For the horizon limb, trace the middle of the black outer stroke and
finish with Enter or middle click.

For each point, click once at the visual centre requested by the
registry instruction.

Do not inspect the output CSV after pass 1.

## Pass 2

After a real break, repeat from untouched source crops:

```bash
python scripts/digitize_first_hand_diagram_landmarks.py \
  --pass-number 2 \
  --operator "Salah-Eddin Gherbi"
```

The digitizer does not load pass 1 while pass 2 is collected.

## Later-stage curves

A printed great circle may be activated only by explicit ID after the
neutral census is committed:

```bash
python scripts/digitize_first_hand_diagram_landmarks.py \
  --pass-number 1 \
  --operator "Salah-Eddin Gherbi" \
  --landmark-id AOG-LM-P07-GC-Y0
```

Its hidden continuation must not be guessed. The trace follows only
clean stroke segments identified by the printed label.

## Deferred annotation

`AOG-LM-P07-THIRTY-DEGREE-ARC` is not digitized. Its intended endpoints
are source-ambiguous and require a later protocol amendment.

## Validation

```bash
python scripts/digitize_first_hand_diagram_landmarks.py \
  --validate \
  data/derived/first_hand_arm_of_god/diagram_landmarks_pass1.csv
```

The pass files preserve raw clicks and are not manually edited.

No projection or self-embedment verdict is issued by the digitizer.
