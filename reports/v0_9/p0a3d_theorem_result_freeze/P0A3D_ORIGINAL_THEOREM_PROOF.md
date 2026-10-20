# Constructive exact 2D QO theorem — proposed for independent mathematical QC

Every numbered claim below is [PROVED_HERE_AWAITING_INDEPENDENT_QC]. This tag
denotes a submitted argument, not independent approval or software certification.
The theorem disposition is P0A3D_EXACT_2D_QO_THEOREM_PROPOSED. The frozen
definition is identified in PROVENANCE_AND_INFORMATION_BARRIER.json.

## 1. Hypotheses and exact arithmetic construction

1.1 Let a,b be finite ordered lists of at least two rational points in R²,
with independently declared open parameter intervals, fixed initial/final indices
and traversal order. Both lists are nonconstant. Coordinates at distinguished
initial/final indices may coincide. Only proper planar rotations are optimized.
No reversal, reflection, cyclic phase, free scale, trimming or correspondence
change is allowed. Centering/RMS is fixed separately for each supplied path.

1.2 All required numbers are constructible real algebraic numbers. An effective
representation sufficient here is a finite **positive square-root tower**:
K_0=Q, theta_i=+sqrt(r_i), r_i in the evaluated earlier tower, r_i>0.
An element at level i is a finite formal A+B theta_i, A,B at earlier levels.
The embedding uses the positive real root at every step. A generator need not
be irreducible: r_i may already be a square. We do NOT assume formal coefficient
uniqueness, that the formal quotient is a field, or that a nonzero coefficient
vector denotes a nonzero real value. This distinction is essential to dependent
radicals such as sqrt(3+2sqrt(2))=1+sqrt(2).

1.3 Addition is componentwise; multiplication is
(A+B theta)(C+D theta)=(AC+BD r)+(AD+BC)theta. These identities preserve the
chosen real embedding, even for dependent generators. All coefficient arithmetic
descends to a strictly earlier tower and ultimately rational arithmetic.

1.4 **Exact sign algorithm, including equality.** Given x=A+B sqrt(r), first
recursively decide a=sign(A), b=sign(B) in the earlier tower. If a=0, return b;
if b=0, return a; if a=b, return a. Otherwise the two terms have opposite signs.
Let d=sign(A²-B² r), recursively in the earlier tower. Return a*d. Indeed,
|A|+|B|sqrt(r)>0, so sign(|A|-|B|sqrt(r)) equals sign(A²-B²r), and the sign of
x is sign(A) times that comparison. In particular d=0 in the opposite-sign
case proves x=0 exactly. Each recursive sign problem has lower tower height.
At height zero, sign is the signed integer numerator of a rational. Thus this
algorithm terminates after finitely many rational operations for every finite
tower input. Equality of x,y is sign(x-y)=0; order is the same trichotomy.
No separation estimate, finite decimal tolerance, or opaque zero oracle is used.

1.5 **Division, including reducible towers.** First decide sign(x). If zero,
division is invalid. For nonzero x=A+B theta, let D=A²-B²r. If D!=0, then
1/x=(A-B theta)/D, with the inverse of D computed at lower height. If D=0,
nonzero x implies A and B theta have the same sign and equal magnitude; hence
x=2A with A!=0 and 1/x=1/(2A), also a lower-height inversion. If B=0 it is
just inversion of A. These cover all cases. A zero conjugate must NOT trigger
division by zero or rejection of a nonzero real element. The representation's
formal algebra can have zero divisors, but the evaluated real arithmetic does
not. Each inversion recurses down tower height, so it terminates.

1.6 **Square roots and comparisons.** For an element x, use 1.4 to decide its
sign. Negative x has no real square root; zero maps to zero. For x>0 append a
generator theta=+sqrt(x). Rational perfect squares and previously equal
radicands may be reduced exactly as optimizations, not assumptions. Elements
with different construction histories are embedded in their concatenated tower;
all later radicands reference only prior generators. This lets the same finite
algorithms compare every pair of values produced below, including nested roots,
and reconstruct an externally supplied expression without selecting an ambiguous
conjugate. Every adjoined element is algebraic by theta²-x=0 and finite algebraic
extension/transitivity. Irreducibility or minimal polynomials are unnecessary
for this constructive, explicitly embedded representation.

1.7 **Serialization and effective termination.** Encode reduced rationals by
signed decimal numerator and strictly positive denominator; encode ordered tower
radicands by sorted square-free monomial masks in earlier generator indices,
and an element by its sorted rational coefficient terms. Masks merely mean
products of distinct formal generators; they do not assert independence. Reject
forward references, duplicate masks, zero coefficients and noncanonical
rationals. Each root's positive sign assertion is independently decidable by
1.4. This is a canonical *wire representation of a construction*, not a unique
minimal representation of an algebraic value. Semantic equality uses 1.4,
never string equality. Finite lists, finite recursive arithmetic and finite
height establish computability; they do not assert a polynomial bit complexity,
uniform practical time, bounded memory, or completion under imposed software caps.

## 2. Path semantics and true arclength

2.1 For consecutive vertices p_i,p_(i+1), d_i=||p_(i+1)-p_i||² is nonnegative
rational. d_i=0 iff the endpoints are exactly equal. Bypass exactly these edges,
recording their original indices and endpoints. Do not remove nonconsecutive
returns. Every remaining length l_i=+sqrt(d_i)>0 is obtained by 1.6. A nonconstant
finite list has at least one nonzero consecutive difference: otherwise induction
makes every vertex the initial point. Hence L=sum l_i>0.

2.2 Put t_0=0 and t_(i+1)=t_i+l_i/L. The breakpoints strictly increase to 1.
On [t_i,t_(i+1)], define a(u)=p_i+(u-t_i)(p_(i+1)-p_i)/(t_(i+1)-t_i).
Endpoint agreement makes this a continuous map. Speed is L on every nonzero
edge, so u is the genuine normalized Euclidean arclength parameter. Repeated
travel over a segment contributes again to L and to its parameter interval.
Zero-edge bypass changes no map or integral and retains provenance.

2.3 Inserting a point p_i+lambda(p_(i+1)-p_i), 0<lambda<1, along an existing
straight traversal replaces l by lambda*l and (1-lambda)*l. These occupy the
same total interval with the same affine map and speed; centroids, RMS,
correlations and QO therefore remain unchanged. The rational-input theorem
applies when the inserted coordinates are rational. Reordering, adding an
off-segment point or taking a shortcut changes the map and has no such guarantee.

## 3. Exact integration and positive normalization

3.1 All breakpoints and affine coefficients belong to the finite tower. Merge
the two finite sorted breakpoint lists using exact comparison 1.4; retain an
equal breakpoint once. Each adjacent distinct pair gives positive width and
lies in exactly one segment interior of each path. Equality/crossing cases are
decidable; no numerical overlap substitutes for equality. Knots at endpoints
do not affect integrals, and continuity fixes their values.

3.2 A coordinate on any cell is m*u+c. Integrals are finite differences of
m*u²/2+c*u. For two coordinates (m*u+c),(n*u+d), the product primitive is
m*n*u³/3+(m*d+n*c)*u²/2+c*d*u. Endpoint sums, products and divisions by 2,3
stay in the same tower. Thus exact means, squared norms and cross moments are
constructible algebraic numbers. Independently, for endpoint values x,z and
y,w over a cell of width h, the product integral is
h*(2xy+xw+zy+2zw)/6. Expansion of the affine interpolants proves the equivalence.
These two formulas furnish distinct integration implementations for checking.

3.3 Let c_a=integral a and V_a=integral ||a-c_a||². The integrand is continuous,
nonnegative. If its integral were zero, it could not be positive at any point:
continuity would give a positive integral on a nonempty interval (one-sided at
an endpoint). Hence a(u)=c_a everywhere, contradicting 2.1/2.2. Therefore
V_a>0; analogously V_b>0. This proves that positive arclength suffices for
positive RMS in the stated finite continuous-path domain. It does not justify
a small positive numerical floor. Exact sign 1.4 verifies the software premise.

3.4 Set r_a=+sqrt(V_a), r_b=+sqrt(V_b), A=(a-c_a)/r_a and B=(b-c_b)/r_b.
All normalized coordinates/coefficients are algebraic by 1.3–1.6. Their means
are zero and their squared L² norms are one by direct substitution. With
J(x,y)=(-y,x), alpha=integral B·A and beta=integral B·JA are exact algebraic
cell integrals. Centering can equivalently be performed on raw moments:
integral a·b-c_a·c_b and integral b·Ja-c_b·Jc_a, divided by r_a*r_b.

## 4. Full SO(2) optimum, properness and exact ties

4.1 Every real 2-by-2 proper orthogonal matrix is Q=cI+tJ with c²+t²=1:
its first column is (c,t), and orthonormality with determinant +1 forces the
second to be (-t,c). Conversely every such pair gives an SO(2) matrix. Expanding
the squared residual and using the unit norms from 3.4 gives
F(Q)=integral ||QA-B||²=2-2(c*alpha+t*beta).

4.2 Let s=+sqrt(alpha²+beta²). For any unit (c,t),
c*alpha+t*beta<=s by the ordinary two-dimensional Cauchy–Schwarz inequality.
If s>0, equality is attained uniquely at (c,t)=(alpha/s,beta/s). No trigonometric
function evaluation or local optimizer is required. Q* has Q*^T Q*=I and
det(Q*)=(alpha²+beta²)/s²=1. It is an actual feasible proper rotation.

4.3 For s>0, the attained cross-correlation is s. Cauchy–Schwarz in the real
Hilbert space L²([0,1];R²), applied to B and Q*A, gives s<=||B||*||Q*A||=1.
This proof does not assume the desired residual's nonnegativity to select a
root. For s=0, s<=1 is immediate. Thus 0<=s<=1. It follows that 2-2s>=0 and
q=+sqrt(2-2s) is real algebraic, with 0<=q<=sqrt(2).

4.4 If sign(s)=0 exactly, alpha²+beta²=0 forces both real numbers alpha,beta
to vanish. Every Q has F(Q)=2; canonical witness I attains q=sqrt(2), and the
state is EXACT_WHOLE_ROLL_TIE. If s>0, only the unit pair in 4.2 maximizes
correlation. No small nonzero s may enter the tie branch. The exact predicates
in section 1 decide this dichotomy for every finite valid input.

4.5 **Independent attained-residual obligation.** On each common cell, apply
the serialized Q* to the independently reconstructed normalized source affine
coefficients, subtract the target coefficients, square both coordinates, and
integrate their polynomial primitives. Sum the cells. Exact equality with
2-2s follows also by 4.1–4.4, but the checker must evaluate the direct polynomial
residual, orthogonality and determinant separately from the production score
formula. Algebraic equality uses the sign algorithm, not interval containment.

4.6 A constructive algorithm is now explicit: validate rational ordered inputs;
bypass/log zero edges; form positive lengths, exact knots and moments; normalize;
merge knots; integrate alpha,beta; decide s=0 or s>0; construct Q* and q; serialize
the finite tower and identities; independently reconstruct and check them. Every
step is finite in the abstract exact-arithmetic model. A finite software budget
can interrupt it honestly without changing its domain or the theorem.

## 5. Falsifiable counterexamples and boundaries

5.1 **Irrational lengths.** The rational displacement (1,1) has length sqrt(2).
The ordered vertices (1,3),(2,4),(4,5) have lengths sqrt(2),sqrt(5). A rational-
length-only method omits valid inputs. These are abstract arithmetic examples.

5.2 **Support is not traversal; retracing counts.** Let a run from (-2,0) to
(2,0), while b runs (2,0),(-2,0),(2,0). Both trace the same continuous support.
After centering, a is odd under u->1-u and b is even; beta=0 since both are
collinear, and alpha=0 by symmetry. Both radii are positive, so q=sqrt(2), not
zero. b's coincident endpoint coordinates remain distinguished parameter ends.
One cannot discard its return trip or optimize an unregistered cyclic phase.

5.3 **Reversal/reflection are not searched.** Take an ordered noncollinear
two-edge path with unequal edge lengths, for example the path in 5.1. Reversal
changes the location of its single genuine turn from sqrt(2)/(sqrt(2)+sqrt(5))
to sqrt(5)/(sqrt(2)+sqrt(5)). A proper rotation and deterministic translation/
positive scale cannot move that parameter value. If QO were zero, continuous
normalized paths would be equal everywhere, forcing equal turn locations, a
contradiction. Reflection changes the sign of a nonzero oriented pair of edge
directions, which no proper rotation can repair. Neither transform is a nuisance
in this theorem. This is a logical counterexample, not an extra software branch.

5.4 **Sampling limitation.** Replacing an off-chord middle vertex of the path
in 5.1 by just its endpoints changes a two-direction path into a straight one.
No proper similarity turns the former normalized map into the latter, so their
QO is strictly positive by attainment and continuity. Exact honest subdivision
in 2.3 is not arbitrary resampling invariance or a smooth-curve error bound.

5.5 **Exact zero versus tiny nonzero.** Let a=(-3,0)->(3,0). Let b=(2,0)->
(-2,0)->(2+e,0), with rational e>=0. Put h=4, k=4+e and L=h+k.
Direct integration of (6u-3)b_x(u), with the turn at h/L, gives the raw centered
correlation C=(k-h)(h²+4hk+k²)/(2L²). beta=0. At e=0, C=0 exactly and every roll
ties. At every rational e>0, C>0, both RMS values are positive, and the optimum
has positive cosine 1. This family distinguishes zero from arbitrarily small
positive correlations. Finite overlap with zero cannot decide this distinction.

5.6 **No 3D extrapolation.** A nonconstant 3D segment parallel to a projection
kernel can project to one point, so its planar length/RMS vanish. The hypotheses
here do not cover that observation. No 3D code, camera family, QH, visibility,
source optics, or scientific control inference follows from this theorem.

5.7 **Resource versus theorem.** Tower height and formal coefficient growth can
increase with path size. A prescribed operation/bit/height limit may expire even
on a valid path; this is RESOURCE_INCOMPLETE, never invalid geometry or score
zero. No complexity bound or universal performance is proved beyond effective
finite termination in an unbounded exact rational computation model.

## 6. Adversarial review boundary

Review 1.4 and the zero-conjugate inversion case in 1.5 especially carefully;
assuming an irreducible basis would invalidate this construction. Independently
check beta orientation, exact merged knots, whole-roll symmetry, positivity and
direct residual. Review code separately: these arguments do not establish that
the implementation follows them. No mathematical gap is intentionally omitted
from the proposed theorem; all claims await independent QC. Common rational
arithmetic/runtime trust and implementation/resource limitations are recorded
separately. This proposal neither verifies the software nor freezes the result.
