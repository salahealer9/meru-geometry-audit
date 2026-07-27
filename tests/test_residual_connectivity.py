"""Tests for residual endpoint-pairing analysis."""

from __future__ import annotations

import numpy as np
import pytest

from meru_geometry.connectivity import (
    ConnectivityComponent,
    SegmentTraversal,
)
from meru_geometry.residual_connectivity import (
    best_merge_per_component_pair,
    closure_candidate,
    rank_free_endpoint_pairs,
    residual_candidate_identifier,
)


def component(
    segment_id: int,
    start_free: bool = True,
    end_free: bool = True,
) -> ConnectivityComponent:
    free = []

    if start_free:
        free.append((segment_id, "start"))

    if end_free:
        free.append((segment_id, "end"))

    return ConnectivityComponent(
        segment_ids=(segment_id,),
        accepted_connection_ids=(),
        free_endpoints=tuple(free),
        closed=False,
        branched=False,
        traversal=(
            SegmentTraversal(
                segment_id=segment_id,
                forward=True,
                entry_endpoint="start",
                exit_endpoint="end",
            ),
        ),
    )


def test_inter_component_pair_count() -> None:
    segments = {
        1: np.asarray(
            [[0.0, 0.0], [1.0, 0.0]]
        ),
        2: np.asarray(
            [[2.0, 0.0], [3.0, 0.0]]
        ),
    }

    candidates = rank_free_endpoint_pairs(
        "red",
        segments,
        (component(1), component(2)),
        include_same_component=False,
    )

    assert len(candidates) == 4
    assert all(
        candidate.candidate_type == "merge"
        for candidate in candidates
    )


def test_best_candidate_is_retained_per_component_pair() -> None:
    segments = {
        1: np.asarray(
            [[0.0, 0.0], [1.0, 0.0]]
        ),
        2: np.asarray(
            [[2.0, 0.0], [3.0, 0.0]]
        ),
    }

    candidates = rank_free_endpoint_pairs(
        "red",
        segments,
        (component(1), component(2)),
    )

    selected = best_merge_per_component_pair(
        candidates
    )

    assert len(selected) == 1
    assert selected[0].distance == pytest.approx(1.0)


def test_closure_candidate_uses_two_free_endpoints() -> None:
    segments = {
        1: np.asarray(
            [
                [0.0, 0.0],
                [1.0, 0.0],
                [1.0, 1.0],
            ]
        )
    }

    candidate = closure_candidate(
        "blue",
        segments,
        component(1),
        component_id=1,
    )

    assert candidate.candidate_type == "close"
    assert candidate.component_a == 1
    assert candidate.component_b == 1


def test_closure_requires_exactly_two_free_endpoints() -> None:
    segments = {
        1: np.asarray(
            [[0.0, 0.0], [1.0, 0.0]]
        )
    }

    with pytest.raises(
        ValueError,
        match="exactly two",
    ):
        closure_candidate(
            "blue",
            segments,
            component(
                1,
                start_free=True,
                end_free=False,
            ),
            component_id=1,
        )


def test_identifier_records_layer_type_and_components() -> None:
    segments = {
        1: np.asarray(
            [[0.0, 0.0], [1.0, 0.0]]
        )
    }

    candidate = closure_candidate(
        "blue",
        segments,
        component(1),
        component_id=1,
    )

    assert (
        residual_candidate_identifier(candidate)
        == "B_C_C01_C01_S01S_S01E"
    )
