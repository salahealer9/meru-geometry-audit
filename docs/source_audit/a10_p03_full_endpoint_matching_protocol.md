# A10_P03 Full Endpoint-Matching Search Protocol

## Objective

Enumerate every perfect matching represented in the combined A10_P03
same-colour and cross-colour endpoint-candidate graph.

## Search space

The provisional graph contains:

- 48 endpoint nodes from 24 visible fragments;
- 47 candidate endpoint edges;
- 16 connected candidate-graph components;
- 15 forced two-node components;
- one 18-node component containing all endpoint uncertainty;
- 28 complete perfect matchings.

## Preserved evidence

Every candidate search preserves:

- all digitized visible fragments;
- all 31 reviewed crossing events;
- all reviewed over-under assignments;
- all crossing-to-fragment locations;
- the manually resolved exact visit-order tie.

The tracked Gauss and signed-Gauss snapshots are never modified.

## Candidate status

Accepted and rejected endpoint rows are included so that the graph search is
exhaustive relative to the currently recorded candidate inventory.

This does not make them evidentially equivalent.

Rejected rows may carry substantive source-review reasons, including:

- `different_feature`;
- `colour_intersection`;
- `crossing_conflict`;
- `colour_transition_conflict`.

The search therefore represents an upper-bound sensitivity audit.

## Candidate evaluation

Each perfect matching is evaluated for:

1. complete endpoint coverage;
2. global component count;
3. existence of one degree-two global cycle;
4. number of classical Gauss-parity violations;
5. number of accepted endpoint edges retained;
6. reason codes attached to selected rejected edges;
7. total geometric candidate score and distance.

## Interpretation

A zero-violation matching would pass only the necessary Gauss even condition.
Its changed endpoint connections would require targeted source reinspection.

Failure of all 28 matchings would rule out all currently represented endpoint
connectivity alternatives as a complete explanation of the parity failure.
