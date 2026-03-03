"""Configuration and constants."""

from pathlib import Path

OUTPUT_DIR = Path(__file__).parents[1] / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

YEAR = 2029  # Forecast year of interest

# OBR economic forecast assumptions (PLACEHOLDER — update on the day)

# Previous forecast (Autumn Statement 2025)
PREV_EARNINGS_GROWTH = {2026: 3.5, 2027: 3.0, 2028: 2.8, 2029: 2.5}
PREV_CPI_INFLATION = {2026: 2.6, 2027: 2.2, 2028: 2.0, 2029: 2.0}

# Updated forecast (Spring Statement 2026) — fill in from EFO tables
UPDATED_EARNINGS_GROWTH = {2026: None, 2027: None, 2028: None, 2029: None}
UPDATED_CPI_INFLATION = {2026: None, 2027: None, 2028: None, 2029: None}

# Household group definitions
GROUPS = {
    "Single adult, no children": lambda ft, pen: (ft == "SINGLE") & (pen == 0),
    "Couple, no children": lambda ft, pen: (ft == "COUPLE_NO_CHILDREN") & (pen == 0),
    "Single parent": lambda ft, pen: ft == "LONE_PARENT",
    "Couple with children": lambda ft, pen: ft == "COUPLE_WITH_CHILDREN",
    "Single pensioner": lambda ft, pen: (ft == "SINGLE") & (pen == 1),
    "Pensioner couple": lambda ft, pen: (ft == "COUPLE_NO_CHILDREN") & (pen == 1),
}
