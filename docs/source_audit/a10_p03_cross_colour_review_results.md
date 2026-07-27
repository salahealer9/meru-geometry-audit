# A10_P03 Cross-Colour Endpoint Review Results

## Review boundary

The same-colour connectivity audit produced three non-branched open chains:

- one red chain;
- one green chain;
- one blue chain.

Each chain retained exactly two free endpoints.

The cross-colour review therefore considered all 12 pairings between
differently coloured free endpoints.

## Outcome

| Status | Count |
|---|---:|
| Accepted | 3 |
| Rejected | 9 |
| Ambiguous | 0 |
| Unreviewed | 0 |

All decisions were assigned high confidence.

## Accepted perfect matching

The three accepted transitions are:

| Candidate | Decision reason |
|---|---|
| `X_RG_R_S07E_G_S11E` | `colour_transition_supported` |
| `X_RB_R_S01S_B_S06E` | `colour_transition_supported` |
| `X_GB_G_S01S_B_S01S` | `colour_transition_supported` |

These are exactly the three edges of ranked perfect matching 1.

At each accepted junction:

- the two differently coloured lines meet at the same equatorial intersection;
- their local tangent directions align;
- the source drawing supports continuation through a colour change.

## Rejected alternatives

The remaining nine candidates were rejected with reason
`colour_transition_conflict`.

Each rejected candidate reuses at least one endpoint already assigned by the
accepted source-supported perfect matching. These are graph-compatibility
rejections rather than nine independent claims about local source geometry.

## Global graph result

Combining all accepted relations gives:

- 24 visible segment edges;
- 21 accepted same-colour continuation edges;
- 3 accepted cross-colour transition edges;
- 48 endpoint vertices;
- 48 total graph edges.

Every endpoint vertex has degree two, and the graph has one connected
component.

Therefore all 24 visible coloured fragments form one connected,
non-branched closed cycle in the source-derived two-dimensional topology.

## Interpretation

The three colours do not behave as three independently closed loops in
A10_P03. They behave as three consecutive coloured portions of one continuous
closed path.

This establishes source-supported two-dimensional connectivity. It does not
yet establish:

- exact geometry inside every occluded gap;
- complete over-under crossing information;
- a unique three-dimensional embedding;
- a unique dimpled-surface equation;
- equivalence with the canonical \((3,10)\) torus knot.
