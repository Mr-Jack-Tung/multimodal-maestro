from contextlib import ExitStack as DoesNotRaise

from typing import Optional

import numpy as np

import pytest

from som import mask_non_max_suppression, compute_iou_vectorized


@pytest.mark.parametrize(
    "masks, iou_threshold, expected_result, exception",
    [
        (
            np.array([
                [
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1]
                ],
                [
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1]
                ]
            ], dtype=bool),
            0.6,
            np.array([
                [
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1]
                ]
            ], dtype=bool),
            DoesNotRaise()
        ),  # two masks, both filled with ones
        (
            np.array([
                [
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1]
                ],
                [
                    [1, 1, 1, 0],
                    [1, 1, 1, 0],
                    [1, 1, 1, 0],
                    [1, 1, 1, 0]
                ]
            ], dtype=bool),
            0.6,
            np.array([
                [
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1]
                ]
            ], dtype=bool),
            DoesNotRaise()
        ),  # two masks, one filled with ones, the other filled 75% with ones
        (
            np.array([
                [
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1]
                ],
                [
                    [1, 1, 0, 0],
                    [1, 1, 0, 0],
                    [1, 1, 0, 0],
                    [1, 1, 0, 0]
                ]
            ], dtype=bool),
            0.6,
            np.array([
                [
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1]
                ],
                [
                    [1, 1, 0, 0],
                    [1, 1, 0, 0],
                    [1, 1, 0, 0],
                    [1, 1, 0, 0]
                ]
            ], dtype=bool),
            DoesNotRaise()
        ),  # two masks, one filled with ones, the other filled 50% with ones
        (
            np.array([
                [
                    [1, 1, 1, 0],
                    [1, 1, 1, 0],
                    [1, 1, 1, 0],
                    [1, 1, 1, 0]
                ],
                [
                    [0, 1, 1, 1],
                    [0, 1, 1, 1],
                    [0, 1, 1, 1],
                    [0, 1, 1, 1]
                ],
                [
                    [1, 1, 1, 0],
                    [1, 1, 1, 0],
                    [1, 1, 1, 0],
                    [0, 0, 0, 0]
                ],
                [
                    [0, 0, 0, 0],
                    [0, 1, 1, 1],
                    [0, 1, 1, 1],
                    [0, 1, 1, 1]
                ]
            ], dtype=bool),
            0.6,
            np.array([
                [
                    [1, 1, 1, 0],
                    [1, 1, 1, 0],
                    [1, 1, 1, 0],
                    [1, 1, 1, 0]
                ],
                [
                    [0, 1, 1, 1],
                    [0, 1, 1, 1],
                    [0, 1, 1, 1],
                    [0, 1, 1, 1]
                ]
            ], dtype=bool),
            DoesNotRaise()
        ),  # four masks
    ]
)
def test_mask_non_max_suppression(
    masks: np.ndarray,
    iou_threshold: float,
    expected_result: Optional[np.ndarray],
    exception: Exception
) -> None:
    with exception:
        result = mask_non_max_suppression(masks=masks, iou_threshold=iou_threshold)
        assert np.array_equal(result, expected_result)


@pytest.mark.parametrize(
    "masks, expected_result, exception",
    [
        (
            np.array([
                [
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1]
                ]
            ], dtype=bool),
            np.array([
                [1.0]
            ], dtype=np.float64),
            DoesNotRaise()
        ),  # single mask filled with ones
        (
            np.array([
                [
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1]
                ],
                [
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1]
                ]
            ], dtype=bool),
            np.array([
                [1.0, 1.0],
                [1.0, 1.0]
            ], dtype=np.float64),
            DoesNotRaise()
        ),  # two masks filled with ones
        (
            np.array([
                [
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1]
                ],
                [
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1]
                ],
                [
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1]
                ]
            ], dtype=bool),
            np.array([
                [1.0, 1.0, 1.0],
                [1.0, 1.0, 1.0],
                [1.0, 1.0, 1.0]
            ], dtype=np.float64),
            DoesNotRaise()
        ),  # three masks filled with ones
        (
            np.array([
                [
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1]
                ],
                [
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]
                ]
            ], dtype=bool),
            None,
            pytest.raises(ValueError)
        ),  # two masks, one filled with ones, the other with zeros
        (
            np.array([
                [
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1]
                ],
                [
                    [1, 1, 0, 0],
                    [1, 1, 0, 0],
                    [1, 1, 0, 0],
                    [1, 1, 0, 0]
                ]
            ], dtype=bool),
            np.array([
                [1.0, 0.5],
                [0.5, 1.0]
            ], dtype=np.float64),
            DoesNotRaise()
        ),  # two masks, one filled with ones, the other filled 50% with ones
(
            np.array([
                [
                    [0, 1, 1, 1],
                    [0, 1, 1, 1],
                    [0, 1, 1, 1],
                    [0, 1, 1, 1]
                ],
                [
                    [1, 1, 1, 0],
                    [1, 1, 1, 0],
                    [1, 1, 1, 0],
                    [1, 1, 1, 0]
                ]
            ], dtype=bool),
            np.array([
                [1.0, 0.5],
                [0.5, 1.0]
            ], dtype=np.float64),
            DoesNotRaise()
        ),  # two masks, both filled 75% with ones
        (
            np.array([
                [
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1]
                ],
                [
                    [1, 1, 0, 0],
                    [1, 1, 0, 0],
                    [1, 1, 0, 0],
                    [1, 1, 0, 0]
                ],
                [
                    [1, 1, 0, 0],
                    [1, 1, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]
                ],
                [
                    [0, 0, 1, 1],
                    [0, 0, 1, 1],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]
                ],
            ], dtype=bool),
            np.array([
                [1.00, 0.50, 0.25, 0.25],
                [0.50, 1.00, 0.50, 0.00],
                [0.25, 0.50, 1.00, 0.00],
                [0.25, 0.00, 0.00, 1.00],
            ], dtype=np.float64),
            DoesNotRaise()
        ),  # four masks
    ]
)
def test_compute_iou_vectorized(
    masks: np.ndarray,
    expected_result: Optional[np.ndarray],
    exception: Exception
) -> None:
    with exception:
        result = compute_iou_vectorized(masks)
        assert np.array_equal(result, expected_result)