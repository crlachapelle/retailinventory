from __future__ import annotations

import math

import pandas as pd
import pytest

from legacy_inventory_processor import calc_inv_turn


def _write_inventory_csv(tmp_path, rows):
    csv_path = tmp_path / "inventory.csv"
    pd.DataFrame(rows).to_csv(csv_path, index=False)
    return csv_path


def test_calc_inv_turn_happy_path(tmp_path):
    csv_path = _write_inventory_csv(
        tmp_path,
        [
            {"year": 2020, "cost": 10, "sold": 4, "beg_inv": 20, "end_inv": 30},
            {"year": 2020, "cost": 5, "sold": 6, "beg_inv": 10, "end_inv": 14},
            {"year": 2021, "cost": 1, "sold": 100, "beg_inv": 1, "end_inv": 1},
        ],
    )

    result = calc_inv_turn(csv_path, 2020)

    expected_cgs = (10 * 4) + (5 * 6)
    expected_t = ((20 + 30) / 2) + ((10 + 14) / 2)
    assert math.isclose(result, expected_cgs / expected_t)


def test_calc_inv_turn_returns_zero_when_no_matching_year(tmp_path):
    csv_path = _write_inventory_csv(
        tmp_path,
        [
            {"year": 2021, "cost": 2, "sold": 5, "beg_inv": 1, "end_inv": 1},
        ],
    )

    assert calc_inv_turn(csv_path, 2020) == 0.0


def test_calc_inv_turn_returns_zero_when_avg_inventory_is_zero(tmp_path):
    csv_path = _write_inventory_csv(
        tmp_path,
        [
            {"year": 2020, "cost": 8, "sold": 10, "beg_inv": 0, "end_inv": 0},
        ],
    )

    assert calc_inv_turn(csv_path, 2020) == 0.0


def test_calc_inv_turn_raises_for_missing_required_columns(tmp_path):
    csv_path = tmp_path / "inventory.csv"
    pd.DataFrame(
        [
            {"year": 2020, "cost": 10, "sold": 4, "beg_inv": 20},
        ]
    ).to_csv(csv_path, index=False)

    with pytest.raises(ValueError):
        calc_inv_turn(csv_path, 2020)
