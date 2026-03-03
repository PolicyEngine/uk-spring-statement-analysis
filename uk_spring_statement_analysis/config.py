"""Configuration and constants."""

from pathlib import Path

OUTPUT_DIR = Path(__file__).parents[1] / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

YEAR = 2029  # Forecast year of interest

# OBR economic forecast assumptions (PLACEHOLDER — update on the day)

# Previous forecast (Autumn Statement 2025 / OBR EFO November 2025)
PREV_EARNINGS_GROWTH = {2026: 3.3, 2027: 2.3, 2028: 2.1, 2029: 2.2}
PREV_CPI_INFLATION = {2026: 2.5, 2027: 2.0, 2028: 2.0, 2029: 2.0}
PREV_RPI_INFLATION = {2026: 3.7, 2027: 3.1, 2028: 2.9, 2029: 2.9}
PREV_HOUSE_PRICES = {2026: 2.2, 2027: 2.8, 2028: 2.7, 2029: 2.6}
PREV_PER_CAPITA_GDP = {2026: 3.3, 2027: 3.3, 2028: 3.0, 2029: 2.9}
PREV_SOCIAL_RENT = {2026: 4.5, 2027: 3.5, 2028: 3.0, 2029: 3.0}

# Updated forecast (Spring Statement 2026) — from OBR EFO March 2026, Table A.1
UPDATED_EARNINGS_GROWTH = {2026: 3.4, 2027: 2.4, 2028: 2.1, 2029: 2.2}
UPDATED_CPI_INFLATION = {2026: 2.3, 2027: 2.0, 2028: 2.0, 2029: 2.0}
UPDATED_RPI_INFLATION = {2026: 3.1, 2027: 3.0, 2028: 2.8, 2029: 2.9}
UPDATED_HOUSE_PRICES = {2026: 2.4, 2027: 2.9, 2028: 2.7, 2029: 2.6}
UPDATED_PER_CAPITA_GDP = {2026: 2.9, 2027: 3.2, 2028: 3.1, 2029: 3.0}
UPDATED_SOCIAL_RENT = {2026: 4.4, 2027: 3.3, 2028: 3.0, 2029: 3.0}

# Household group definitions
GROUPS = {
    "Single adult, no children": lambda ft, pen: (ft == "SINGLE") & (pen == 0),
    "Couple, no children": lambda ft, pen: (ft == "COUPLE_NO_CHILDREN") & (pen == 0),
    "Single parent": lambda ft, pen: ft == "LONE_PARENT",
    "Couple with children": lambda ft, pen: ft == "COUPLE_WITH_CHILDREN",
    "Single pensioner": lambda ft, pen: (ft == "SINGLE") & (pen == 1),
    "Pensioner couple": lambda ft, pen: (ft == "COUPLE_NO_CHILDREN") & (pen == 1),
}
