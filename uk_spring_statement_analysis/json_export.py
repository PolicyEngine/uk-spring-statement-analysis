"""Export analysis data as JSON for the React dashboard."""

import json
from pathlib import Path

from .config import (
    PREV_EARNINGS_GROWTH,
    PREV_CPI_INFLATION,
    PREV_RPI_INFLATION,
    UPDATED_EARNINGS_GROWTH,
    UPDATED_CPI_INFLATION,
    UPDATED_RPI_INFLATION,
)

DATA_DIR = Path(__file__).parents[1] / "dashboard" / "public" / "data"


def export_economic_forecast():
    """Write economic_forecast.json with earnings growth and CPI inflation data."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    earnings = []
    inflation = []
    for yr in [2026, 2027, 2028, 2029]:
        prev_e = PREV_EARNINGS_GROWTH[yr]
        upd_e = UPDATED_EARNINGS_GROWTH[yr]
        change_e = round(upd_e - prev_e, 1) if upd_e is not None else None
        earnings.append({
            "year": yr,
            "previous": prev_e,
            "updated": upd_e,
            "change": change_e,
        })

        prev_i = PREV_CPI_INFLATION[yr]
        upd_i = UPDATED_CPI_INFLATION[yr]
        change_i = round(upd_i - prev_i, 1) if upd_i is not None else None
        inflation.append({
            "year": yr,
            "previous": prev_i,
            "updated": upd_i,
            "change": change_i,
        })

    rpi = []
    for yr in [2026, 2027, 2028, 2029]:
        prev_r = PREV_RPI_INFLATION[yr]
        upd_r = UPDATED_RPI_INFLATION[yr]
        change_r = round(upd_r - prev_r, 1) if upd_r is not None else None
        rpi.append({
            "year": yr,
            "previous": prev_r,
            "updated": upd_r,
            "change": change_r,
        })

    data = {"earnings_growth": earnings, "cpi_inflation": inflation, "rpi_inflation": rpi}
    out = DATA_DIR / "economic_forecast.json"
    out.write_text(json.dumps(data, indent=2))
    print(f"  Written {out}")


def export_household_data(baseline_stats, reformed_stats=None):
    """Write household_stats.json and household_comparison.json."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # household_stats.json
    stats = []
    for _, row in baseline_stats.iterrows():
        stats.append({
            "group": row["group"],
            "mean_hnet": round(float(row["mean_hnet"])),
            "median_hnet": round(float(row["median_hnet"])),
            "weighted_n": round(float(row["weighted_n"])),
        })

    out = DATA_DIR / "household_stats.json"
    out.write_text(json.dumps(stats, indent=2))
    print(f"  Written {out}")

    # household_comparison.json
    comparison = []
    for _, row in baseline_stats.iterrows():
        label = row["group"]
        baseline_hnet = round(float(row["mean_hnet"]))

        if reformed_stats is not None:
            reformed_hnet = round(float(
                reformed_stats.loc[
                    reformed_stats["group"] == label, "mean_hnet"
                ].iloc[0]
            ))
        else:
            reformed_hnet = baseline_hnet

        comparison.append({
            "group": label,
            "baseline_hnet": baseline_hnet,
            "reformed_hnet": reformed_hnet,
            "change": reformed_hnet - baseline_hnet,
        })

    out = DATA_DIR / "household_comparison.json"
    out.write_text(json.dumps(comparison, indent=2))
    print(f"  Written {out}")
