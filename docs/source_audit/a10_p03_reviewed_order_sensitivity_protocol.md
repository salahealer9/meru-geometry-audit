# A10_P03 Reviewed Local-Order Sensitivity Protocol

## Objective

Determine whether reversing any subset of the four accepted local visit-order
decisions can remove the classical Gauss-parity failure.

## Search boundary

The search modifies only the order of the two visits within each reviewed
adjacent pair.

It preserves:

- all 31 crossing identities;
- all O/U assignments;
- the global endpoint matching;
- every unreviewed local visit order;
- all crossing signs.

The frozen Gauss snapshots are never modified.

## Reversal space

With four disjoint reviewed pairs, the complete search contains

\[
2^4=16
\]

order combinations, including the accepted baseline.

## Parity effect

Swapping two adjacent visits belonging to distinct crossing events changes the
position parity of those two visits only. It therefore toggles the even-condition
status of exactly those two crossing events.

The implementation nevertheless rebuilds and audits the complete word for every
candidate rather than relying solely on that shortcut.

## Evidential status

All reversed pairs are hypothetical sensitivity cases. The tracked accepted
orders remain the source-derived reconstruction unless separately re-adjudicated.

## Interpretation boundary

A zero-violation candidate would pass only the necessary Gauss even condition.
It would still require full classical realizability testing.

Failure of all 16 candidates rules out these four local-order decisions as a
complete explanation of the parity problem.
