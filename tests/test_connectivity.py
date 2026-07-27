"""Tests for adjudicated endpoint connectivity."""

from __future__ import annotations

import pytest

from meru_geometry.connectivity import (
    build_endpoint_connectivity,
    format_endpoint,
)


def connection(
    candidate_id: str,
    segment_a: int,
    endpoint_a: str,
    segment_b: int,
    endpoint_b: str,
) -> dict[str, object]:
    return {
        "candidate_id": candidate_id,
        "segment_a": segment_a,
        "endpoint_a": endpoint_a,
        "segment_b": segment_b,
        "endpoint_b": endpoint_b,
    }


def test_forward_chain_traversal() -> None:
    components = build_endpoint_connectivity(
        [1, 2],
        [
            connection(
                "C1",
                1,
                "end",
                2,
                "start",
            )
        ],
    )

    assert len(components) == 1

    component = components[0]

    assert component.segment_ids == (1, 2)
    assert component.free_endpoints == (
        (1, "start"),
        (2, "end"),
    )

    assert [
        (item.segment_id, item.forward)
        for item in component.traversal
    ] == [
        (1, True),
        (2, True),
    ]


def test_reversed_segment_traversal() -> None:
    components = build_endpoint_connectivity(
        [1, 2],
        [
            connection(
                "C1",
                1,
                "end",
                2,
                "end",
            )
        ],
    )

    component = components[0]

    assert [
        (item.segment_id, item.forward)
        for item in component.traversal
    ] == [
        (1, True),
        (2, False),
    ]


def test_duplicate_endpoint_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="already connected",
    ):
        build_endpoint_connectivity(
            [1, 2, 3],
            [
                connection(
                    "C1",
                    1,
                    "end",
                    2,
                    "start",
                ),
                connection(
                    "C2",
                    1,
                    "end",
                    3,
                    "start",
                ),
            ],
        )


def test_separate_components_are_preserved() -> None:
    components = build_endpoint_connectivity(
        [1, 2, 3],
        [
            connection(
                "C1",
                1,
                "end",
                2,
                "start",
            )
        ],
    )

    assert len(components) == 2
    assert components[0].segment_ids == (1, 2)
    assert components[1].segment_ids == (3,)


def test_closed_component_has_no_free_endpoints() -> None:
    components = build_endpoint_connectivity(
        [1, 2],
        [
            connection(
                "C1",
                1,
                "end",
                2,
                "start",
            ),
            connection(
                "C2",
                2,
                "end",
                1,
                "start",
            ),
        ],
    )

    component = components[0]

    assert component.closed
    assert component.free_endpoints == ()
    assert len(component.traversal) == 2
    assert format_endpoint((2, "end")) == "S02E"
