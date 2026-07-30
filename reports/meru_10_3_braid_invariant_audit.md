# Meru `10_3.wrl` braid and knot-invariant audit

**Status:** Complete numerical braid reconstruction  
**Source:** `f24de4a08a_10_3.wrl`  
**SHA-256:** `855c46cfeeb31e4394b7a4a294b397aac4cbc14154e172a326e33243dd9e384b`  
**Result:** **PASS**

## Question

Does the native centreline independently encode a three-strand torus
braid of type 3,10, without relying on the asset filename, Meru's written
designation or the earlier toroidal winding fit?

## Centreline and phase convention

The centreline is recovered as the centroid of each of the
300 consecutive tube sections, each containing
20 vertices.

The closed braid uses the following recorded convention:

```text
braid axis:             y
phase coordinate:       atan2(z,x)
diagram coordinate:     y
depth coordinate:       sqrt(x^2+z^2)
viewer convention:      larger radial coordinate is over
strand order:           descending y before each crossing
positive generator:     the upper strand before the crossing passes over the lower strand
```

The native traversal was reversed to make the phase coordinate strictly
increasing:

```text
orientation reversed:   True
minimum azimuth step:   0.0622913353335
maximum azimuth step:   0.0633725766303
major turns:            3
```

This reversal fixes the traversal convention used to record the braid.
It does not change the underlying unoriented knot type.

## Exhaustive piecewise-linear crossing census

The phase origin was selected away from a crossing. The three projected
strand functions were then partitioned at the union of all native
piecewise-linear breakpoints, and every strand pair was tested on every
interval.

```text
piecewise-linear breakpoints:       301
crossings:                           20
start projection margin:            40.4038766482
minimum breakpoint crossing margin: 1.50104982761
minimum over/under depth gap:        36.9297269815
minimum third-strand gap:            50.7127376368
minimum event/breakpoint gap:        0.00529297471675
```

All crossings are isolated from breakpoints, have a large nonzero depth
ordering and remain well separated from the third strand.

## Recovered braid

The signed word is

\[
\beta = (\sigma_2^{-1}\sigma_1^{-1})^{10}.
\]

In explicit generator order:

```text
sigma_2^-1 sigma_1^-1 sigma_2^-1 sigma_1^-1 sigma_2^-1 sigma_1^-1 sigma_2^-1 sigma_1^-1 sigma_2^-1 sigma_1^-1 sigma_2^-1 sigma_1^-1 sigma_2^-1 sigma_1^-1 sigma_2^-1 sigma_1^-1 sigma_2^-1 sigma_1^-1 sigma_2^-1 sigma_1^-1
```

Its diagnostics are:

```text
crossing number:       20
writhe:                -20
induced permutation:   [2, 0, 1]
closure components:    1
all negative:          True
negative 3,10 pattern: True
```

The closure permutation has one cycle, so the braid closes to one knot
rather than a multi-component link.

Under the exact projection and generator conventions recorded above,
the native centreline is the negative three-strand torus braid
\((\sigma_2^{-1}\sigma_1^{-1})^{10}\). Relative to the usual
positive braid convention, this is the mirror-handed representative of
the standard 3,10 torus knot. This handedness statement is
convention-relative: reflecting the diagram or reversing the chosen
viewing convention reverses every generator sign.

## Alexander polynomial

The reduced Burau calculation gives

```text
Delta(t) = t**18 - t**17 + t**15 - t**14 + t**12 - t**11 + t**9 - t**7 + t**6 - t**4 + t**3 - t + 1
degree   = 18
|Delta(-1)| = 3
```

The result agrees exactly with the torus-knot formula for \(T(3,10)\):

```text
t**18 - t**17 + t**15 - t**14 + t**12 - t**11 + t**9 - t**7 + t**6 - t**4 + t**3 - t + 1
```

The Alexander polynomial is mirror-insensitive and is not, by itself, a
unique classifier of all knots. Here it is an independent invariant
check supporting the stronger result supplied by the exact recovered
braid word.

## Result

The native `10_3.wrl` centreline independently yields:

- an exhaustive 20-crossing generic three-braid projection;
- the signed word
  \((\sigma_2^{-1}\sigma_1^{-1})^{10}\);
- a one-component closure;
- and the Alexander polynomial of \(T(3,10)\).

The published “3,10” designation is therefore encoded directly in the
native centreline both as a toroidal winding structure and as an
independently reconstructed braid and knot invariant.

## Scope boundary

This is a deterministic, tolerance-aware double-precision audit of the
piecewise-linear centreline. It is not a formal exact-arithmetic proof.

The signed chirality result is tied to the explicitly recorded phase,
viewing and generator conventions. The Alexander polynomial does not
distinguish a knot from its mirror image.

The result certifies the topology of the recovered native digital
geometry. It does not independently establish broader linguistic,
cosmological or consciousness-related interpretations attached to the
Meru model.
