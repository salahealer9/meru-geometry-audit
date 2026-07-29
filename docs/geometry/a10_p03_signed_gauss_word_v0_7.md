# A10_P03 Source-Reviewed Signed Gauss Word — v0.7

## Result

The frozen 62-visit O/U Gauss word has been combined with the reviewed oriented sign of every crossing event.

- Crossing events: **31**
- Signed visits: **62**
- Positive events: **0**
- Negative events: **31**
- Writhe: **-31**
- Degenerate signs: **0**
- Unresolved order decisions: **0**
- Unresolved sign decisions: **0**
- Signed-token SHA-256: `373a2407f14b140ceb5ddf03f61dff43327fbeb7236bc4b82e6f83800c4afd94`

## Notation

Each ASCII token has the form:

```text
E<event><O-or-U><crossing-sign>
```

For example, `E13O-` denotes the over-strand visit to negative crossing event E13.

This is an explicit project notation rather than an assertion that every published Gauss-code convention uses the same token layout.

## Canonical signed O/U Gauss word

```text
E13O- E21O- E24U- E15U- E26U- E25U- E14O- E05O- E09U- E03U- E04U- E10O- E19U- E20U- E07U- E28U-
E18O- E29O- E31O- E08O- E13U- E21U- E27U- E12U- E25O- E26O- E11O- E05U- E06U- E04O- E17O- E23O-
E10U- E02U- E07O- E28O- E22O- E30O- E16U- E01U- E22U- E18U- E29U- E27O- E12O- E15O- E24O- E11U-
E14U- E06O- E09O- E03O- E17U- E23U- E02O- E19O- E20O- E01O- E16O- E30U- E08U- E31U-
```

Every event occurs exactly twice, once as `O` and once as `U`, and both visits carry the same oriented event sign.

## Sign evidence

- Signs stable across all tangent spans: **31/31**
- Primary tangent span: **6 px**
- Sensitivity spans: **2, 4, 6, 8, 10 and 12 px**
- Manually reviewed low-angle events: `E03`, `E21`, `E24`, `E27`

The remaining events use the basis `derived_stable_all_spans`.

## Reproducibility boundary

The signed sequence is frozen in:

- `data/manual_digitizations/A10_P03/signed_gauss_word.csv`;
- `data/manual_digitizations/A10_P03/signed_gauss_word.sha256`.

Normal execution validates the reconstruction against these files. Replacing them requires the explicit `--update-snapshot` option.

## Interpretation boundary

This result establishes a source-reviewed signed O/U Gauss word for the reconstructed A10_P03 planar diagram under the documented coordinate and sign convention.

It does not yet establish:

- equivalence with a canonical `(3,10)` torus knot;
- minimal crossing number;
- a canonical Dowker–Thistlethwaite representation;
- an Alexander or Jones polynomial;
- a unique three-dimensional embedding.

The next stage is to derive a convention-explicit Dowker-style code and independently validate that it reconstructs the same signed Gauss data.
