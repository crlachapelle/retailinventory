from __future__ import annotations

from os import PathLike

import pandas as pd

REQUIRED_COLUMNS = ["year", "cost", "sold", "beg_inv", "end_inv"]


# old script from 2018 - DO NOT TOUCH without updating the wiki first
def calc_inv_turn(data_path: str | PathLike[str], yr: int) -> float:
    """Calculate inventory turnover for a specific year from a CSV file.

    The turnover ratio is computed as:

    ``sum(cost * sold) / sum((beg_inv + end_inv) / 2)``

    for rows where ``year == yr``. If the selected year's total average
    inventory is zero (including when no rows match), this function returns
    ``0.0``.

    Args:
        data_path: Path to the inventory CSV file.
        yr: Target year used to filter records.

    Returns:
        Inventory turnover ratio for the target year, or ``0.0`` when the
        denominator is zero.
    """
    data = pd.read_csv(data_path, usecols=REQUIRED_COLUMNS)
    yearly_rows = data.loc[data["year"] == yr]

    cgs = (yearly_rows["cost"] * yearly_rows["sold"]).sum()
    total_avg_inventory = ((yearly_rows["beg_inv"] + yearly_rows["end_inv"]) / 2).sum()

    if total_avg_inventory == 0:
        return 0.0

    return float(cgs / total_avg_inventory)
