"""Markdown table generation."""

import pandas as pd

from .config import (
    PREV_EARNINGS_GROWTH,
    PREV_CPI_INFLATION,
    PREV_RPI_INFLATION,
    UPDATED_EARNINGS_GROWTH,
    UPDATED_CPI_INFLATION,
    UPDATED_RPI_INFLATION,
)


def build_economic_tables():
    """Build markdown tables comparing previous and updated OBR forecasts."""
    rows_earnings = []
    rows_inflation = []
    for yr in [2026, 2027, 2028, 2029]:
        prev_e = PREV_EARNINGS_GROWTH[yr]
        upd_e = UPDATED_EARNINGS_GROWTH[yr]
        change_e = f"{upd_e - prev_e:+.1f}pp" if upd_e is not None else ""
        upd_e_str = f"{upd_e:.1f}%" if upd_e is not None else ""
        rows_earnings.append(
            f"| {yr} | {prev_e:.1f}% | {upd_e_str} | {change_e} |"
        )

        prev_i = PREV_CPI_INFLATION[yr]
        upd_i = UPDATED_CPI_INFLATION[yr]
        change_i = f"{upd_i - prev_i:+.1f}pp" if upd_i is not None else ""
        upd_i_str = f"{upd_i:.1f}%" if upd_i is not None else ""
        rows_inflation.append(
            f"| {yr} | {prev_i:.1f}% | {upd_i_str} | {change_i} |"
        )

    rows_rpi = []
    for yr in [2026, 2027, 2028, 2029]:
        prev_r = PREV_RPI_INFLATION[yr]
        upd_r = UPDATED_RPI_INFLATION[yr]
        change_r = f"{upd_r - prev_r:+.1f}pp" if upd_r is not None else ""
        upd_r_str = f"{upd_r:.1f}%" if upd_r is not None else ""
        rows_rpi.append(
            f"| {yr} | {prev_r:.1f}% | {upd_r_str} | {change_r} |"
        )

    header = "| Year | Previous forecast | Updated forecast | Change |"
    sep = "|------|-------------------|------------------|--------|"
    earnings_table = "\n".join([header, sep] + rows_earnings)
    inflation_table = "\n".join([header, sep] + rows_inflation)
    rpi_table = "\n".join([header, sep] + rows_rpi)
    return earnings_table, inflation_table, rpi_table


def generate_summary_table(
    baseline_stats: pd.DataFrame, reformed_stats: pd.DataFrame = None
) -> str:
    """Generate the markdown summary table of average hnet by household group."""
    rows = []
    for _, row in baseline_stats.iterrows():
        label = row["group"]
        prev = row["mean_hnet"]

        if reformed_stats is not None:
            updated = reformed_stats.loc[
                reformed_stats["group"] == label, "mean_hnet"
            ].iloc[0]
        else:
            updated = prev

        change = updated - prev
        rows.append(
            f"| {label} | £{prev:,.0f} | £{updated:,.0f} | £{change:+,.0f} |"
        )

    header = "| Household type | Previous 2029 hnet | Updated 2029 hnet | Change |"
    sep = "|----------------|--------------------|--------------------|--------|"
    return "\n".join([header, sep] + rows)
