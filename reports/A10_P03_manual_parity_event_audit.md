# A10_P03 manual parity-event audit

**Status:** Frozen manual source adjudication  
**Review date:** 2026-07-29  
**Source panel:** `A10_P03.png`  
**Development branch:** `dimpled-surface-reconstruction-v0.7`

## Purpose

This audit records the manual source review of the 16 crossing events
that fail the classical Gauss even condition in the frozen 62-visit,
31-event visible-crossing word derived from A10_P03.

The purpose was not to repair the Gauss word. It was to determine whether
the parity-affected crossing locations contained an evident local error,
such as:

- a wrongly identified crossing;
- an incorrect over/under relation;
- an incorrect local visit order;
- a missed crossing inside the reviewed visible segment;
- or an incorrectly traced short local continuation.

## Frozen parity result

The affected event set is:

```text
E01 E03 E05 E07 E09 E13 E14 E15
E16 E17 E21 E22 E23 E24 E28 E30
````

The frozen word therefore remains non-realizable as a complete classical
one-component planar Gauss word under the necessary even condition.

## Review method

Each affected event was inspected in the source panel using:

1. the unmarked A10_P03 image;
2. segment-specific digitization overlays;
3. labelled crossing overlays;
4. source-forward and frozen-traversal orders;
5. independent review of both participating strands where available;
6. explicit separation of visible segment interiors from hidden or
   partially occluded endpoint continuations.

Parity was not used to decide whether an additional crossing existed.
A crossing was accepted only when supported visually by the source.

## Event-level adjudications

| Event | Over strand | Under strand | Review basis | Result |
|---|---|---|---|---|
| E01 | Blue S04 | Green S03 | Blue S04 | Confirmed; no additional local crossing |
| E03 | Blue S03 | Red S04 | Red S04 central cluster | Confirmed; no additional local crossing |
| E05 | Red S03 | Green S07 | Red S03 | Confirmed; no additional local crossing |
| E07 | Green S04 | Red S06 | Green S04 | Confirmed; no additional local crossing |
| E09 | Blue S03 | Red S03 | Red S03 | Confirmed; no additional local crossing |
| E13 | Red S01 | Green S10 | Red S01 | Confirmed; no additional local crossing |
| E14 | Red S03 | Blue S02 | Red S03 | Confirmed; no additional local crossing |
| E15 | Blue S01 | Red S02 | Blue S01 and Red S02 | Confirmed; no additional local crossing |
| E16 | Blue S04 | Green S04 | Green S04 and Blue S04 | Confirmed; no additional local crossing |
| E17 | Green S06 | Blue S03 | Green S06 and central cluster | Confirmed; no additional local crossing |
| E21 | Red S01 | Green S09 | Red S01 | Confirmed; no additional local crossing |
| E22 | Green S04 | Green S02 | Green S04 | Confirmed; no additional local crossing |
| E23 | Green S06 | Blue S04 | Green S06 and Blue S04 | Confirmed; no additional local crossing |
| E24 | Blue S01 | Red S01 | Red S01 and Blue S01 | Confirmed; no additional local crossing |
| E28 | Green S04 | Red S07 | Green S04 | Confirmed; no additional local crossing |
| E30 | Green S04 | Blue S05 | Green S04 | Confirmed; no additional local crossing |

All 16 affected crossing locations were confirmed at high confidence.
No additional crossing was observed within the reviewed visible segment
interiors.

## Segment-family findings

| Review family | Affected events | Interior result | Confidence |
|---|---|---|---|
| Green S04 | E07; E16; E22; E28; E30 | complete | high |
| Red S01 | E13; E21; E24 | complete | high |
| Red S03 | E05; E09; E14 | complete | high |
| Red S04 central cluster | E03; E17 | complete through central crossing cluster | high |
| Green S06 | E17; E23 | complete | high |
| Blue S04 | E01; E16; E23 | complete | high |
| Blue S01 and Red S02 | E15 | complete | high |

## Central E03/E04/E17 cluster

The dense central cluster was resolved as three distinct pairwise
crossings:

```text
E17: Green S06 over Blue S03
E04: Green S06 over Red S04
E03: Blue S03 over Red S04
```

The resulting local depth order is:

```text
Green S06 > Blue S03 > Red S04
```

No fourth crossing was observed in this cluster.

## What the manual audit establishes

The review supports the following local conclusions:

* the 16 parity-affected crossing identities are visually supported;
* their recorded over/under relations are supported;
* their local source-forward orders are supported;
* the reviewed segment interiors contain no evident omitted crossing;
* the central three-strand cluster is represented by E03, E04 and E17;
* E15 is supported independently by both Blue S01 and Red S02;
* E16, E23 and E24 were each checked from both participating segment
  families.

## What the manual audit does not establish

The audit does **not** establish that the frozen sequence is a complete
planar projection.

In particular, local confirmation of every affected crossing does not
remove the global parity failure. Classical Gauss parity depends on the
cyclic placement of all visits and is independent of over/under
assignment.

The audit also does not establish:

* a unique hidden interpolation behind the sphere or dimple;
* a unique three-dimensional embedding;
* equivalence with the exact torus knot T(3,10);
* completeness of every occluded continuation;
* or internal consistency of the source drawing as a complete
  transparent knot projection.

## Remaining source-level uncertainties

The following accepted endpoint pairings retain partially occluded
geometric routes and require a dedicated continuation ledger:

```text
R:S03E <-> R:S04E
R:S04S <-> R:S05S
```

These routes must not be repaired solely to satisfy parity. Any additional
crossing must be supported independently by the source transition
sequence or by a constrained forward model.

## Conclusion

Manual source review was completed for all 16 events failing the
classical Gauss even condition. Each affected crossing was confirmed at
high confidence with the recorded strand identities, local visit order
and over/under relationship. No additional crossing was observed within
the reviewed visible segment interiors.

These findings do not repair or validate the global Gauss word. The
frozen 62-visit sequence remains non-realizable as a complete classical
planar one-component Gauss word. It should therefore be interpreted as a
**visible-crossing baseline extracted from an occluded or schematic
surface rendering**, rather than as a certified complete knot diagram.

The remaining explanations include source-hidden geometry,
reconstruction assumptions not represented in the present endpoint
graph, schematic omission, or internal inconsistency in the source
drawing. The present audit does not yet distinguish conclusively among
those possibilities.
