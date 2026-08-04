# First Hand planar reciprocal-spiral audit

**Status:** Deterministic planar baseline  
**Primary source:** `AOG_PDF_2005A`  
**Source SHA-256:** `80d52f4b6afefe65ae50e4c01378765c34ae4fde1ad44e8b299870c2e1d3e6fa`  
**Result:** Planar generator reproduced; no self-embedment verdict

## Source-defined curve

The source identifies the unitary reciprocal spiral

\[
r\theta=1,
\qquad
r(\theta)=\frac{1}{\theta},
\qquad
\theta>0.
\]

In Cartesian coordinates:

\[
\gamma(\theta)
=
\left(
\frac{\cos\theta}{\theta},
\frac{\sin\theta}{\theta}
\right).
\]

All endpoint tangents below use the orientation from the inner spiral
end toward the outer end. Since the inner endpoint has larger
\(\theta\), this orientation corresponds to decreasing \(\theta\).

## Analytic asymptotes

As \(\theta\to0^+\):

```text
x(theta) -> +infinity
y(theta) -> 1
r(theta) -> +infinity
oriented tangent -> (+1, 0)
planar arc length -> infinity
```

As \(\theta\to+\infinity\):

```text
x(theta) -> 0
y(theta) -> 0
r(theta) -> 0
```

The paper's point-to-line description is therefore mathematically
correct for the planar reciprocal spiral.

## Frozen truncation A — prose/asymptotic reading

```text
outer theta:       0+  (asymptotic)
inner theta:       3*pi
angular span:      3*pi
turns:             1.5
inner radius:      0.106103295394597
inner position:    (-0.106103295394597, 3.89817183251938e-17)
planar arc length: infinite
```

The directed planar endpoint-tangent mismatch is:

```text
96.0566105942 degrees
```

This is not a self-embedment result because the source explicitly
compactifies the outer end through a spherical projection.

## Frozen truncation B — diagram/unit-point reading

```text
outer theta:       1
inner theta:       1 + 3*pi = 10.4247779607694
angular span:      3*pi
turns:             1.5
outer position:    (0.54030230586814, 0.841470984807897)
inner position:    (-0.0518286632004452, -0.0807183604269105)
planar arc length: 2.5678748465106
```

The marked unit point has \(r=1\) and \(\theta=1\), but its Cartesian
height is

```text
y(1) = sin(1) = 0.841470984807897
|y(1)-1| = 0.158529015192103
```

It is therefore near, but not on, the asymptotic line \(y=1\).

The directed planar endpoint-tangent mismatch is:

```text
140.479349758 degrees
```

Again, this does not decide the spherical self-embedment claim.

## What has been established

- The planar equation is reproduced without fitted parameters.
- The point-to-line asymptotes are verified.
- Both source-supported intervals span exactly \(3\pi\), or 1.5 turns.
- The prose and diagram endpoint conventions define materially
  different finite curve segments.
- Their planar endpoint positions, tangents and arc lengths are now
  frozen for later spherical reconstruction.

## Scope boundary

No S1, S1.5 or S2 verdict is issued here.

The endpoint-alignment claim concerns the compactified spherical or
dimpled-surface construction. Testing it in the plane would answer a
different question and would unfairly reject a claim whose defining
operation has not yet been reconstructed.

The next phase must freeze candidate flat-to-sphere maps using the
source's great-circle constraints and page-7 diagram before inspecting
any self-embedment score.
