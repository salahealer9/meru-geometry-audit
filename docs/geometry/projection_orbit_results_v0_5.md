# Projection-Orbit Results — v0.5

## Exact camera-direction orbit

For each tetrahedral rotation, the viewing direction is

\[
n_i=R_i^\mathsf{T}\hat z.
\]

| Rotation | Camera direction | Signed class | Axis class |
|---:|---|---:|---:|
| R01 | `(0, 0, 1)` | 1 | 1 |
| R02 | `(0, 1, 0)` | 2 | 2 |
| R03 | `(1, 0, 0)` | 3 | 3 |
| R04 | `(0, 0, -1)` | 4 | 1 |
| R05 | `(-1, 0, 0)` | 5 | 3 |
| R06 | `(0, -1, 0)` | 6 | 2 |
| R07 | `(0, -1, 0)` | 6 | 2 |
| R08 | `(-1, 0, 0)` | 5 | 3 |
| R09 | `(0, 0, -1)` | 4 | 1 |
| R10 | `(1, 0, 0)` | 3 | 3 |
| R11 | `(0, 1, 0)` | 2 | 2 |
| R12 | `(0, 0, 1)` | 1 | 1 |

### Exact class structure

- Signed camera-direction classes: **6**.
- Unoriented viewing-axis classes: **3**.
- Signed classes: {R01, R12}, {R02, R11}, {R03, R10}, {R04, R09}, {R05, R08}, {R06, R07}.
- Axis classes: {R01, R04, R09, R12}, {R02, R06, R07, R11}, {R03, R05, R08, R10}.

Thus the 12 proper tetrahedral rotations provide at most **six front/back-sensitive views**, or **three viewing axes** when planar reflection is allowed.

## Object-specific projection classes

The table below uses a relative-RMS equivalence threshold of `1e-08`.

| Object | SO(2) classes | O(2) classes | Closed shift/reversal handling |
|---|---:|---:|---|
| Asymmetric diagnostic probe | 6 | 3 | Open ordered curve; neither allowed |
| Canonical $(3,10)$ torus knot | 3 | 3 | Cyclic shifts and traversal reversal allowed |
| Candidate C0 reciprocal-torus curve | 6 | 3 | Open ordered curve; neither allowed |

### Asymmetric diagnostic probe

**SO(2) classes:** {R01, R12}, {R02, R11}, {R03, R10}, {R04, R09}, {R05, R08}, {R06, R07}.

**O(2) classes:** {R01, R04, R09, R12}, {R02, R06, R07, R11}, {R03, R05, R08, R10}.

### Canonical $(3,10)$ torus knot

**SO(2) classes:** {R01, R04, R09, R12}, {R02, R06, R07, R11}, {R03, R05, R08, R10}.

**O(2) classes:** {R01, R04, R09, R12}, {R02, R06, R07, R11}, {R03, R05, R08, R10}.

### Candidate C0 reciprocal-torus curve

**SO(2) classes:** {R01, R12}, {R02, R11}, {R03, R10}, {R04, R09}, {R05, R08}, {R06, R07}.

**O(2) classes:** {R01, R04, R09, R12}, {R02, R06, R07, R11}, {R03, R05, R08, R10}.

## Interpretation

The exact camera calculation establishes that the 12 group elements are not 12 independent directions. Rotations sharing a signed camera direction differ only by an in-plane rotation. Opposite directions along the same axis differ by an in-plane reflection.

Any object-specific class count below six under SO(2), or below three under O(2), is caused by additional symmetry of the object.

A literal claim that one fixed object generates 22 independent letterforms solely through the 12 proper rotations of one tetrahedron is therefore mathematically incomplete. Additional viewing, tracing, truncation, gesture, component-selection, or continuous-orientation rules would be required.

This result does not determine which additional operations, if any, were intended in the historical Meru construction.

## Generated outputs

- `figures/candidate_c0_tetrahedral_projections.png`
- `figures/projection_orbit_error_matrices.png`
- `data/derived/projection_orbit_pairwise_errors.csv` (local reproducible output; ignored by Git)
