"""
Generate data and charts for the Spring Statement 2026 blog post.

This script:
1. Defines household archetypes (working-age, with children, pensioners)
2. Calculates household net income at various earnings levels for each archetype
3. Compares baseline vs updated economic assumptions (earnings growth, inflation)
4. Outputs markdown tables and saves charts for the blog post

NOTE: The OBR economic determinants below are placeholders.
Replace with actual values from the EFO tables once published.
"""

from policyengine_uk import Simulation, Microsimulation
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

YEAR = 2029  # Forecast year of interest

# ---------------------------------------------------------------------------
# 1. OBR economic forecast assumptions (PLACEHOLDER — update on the day)
# ---------------------------------------------------------------------------

# Previous forecast (Autumn Statement 2025)
PREV_EARNINGS_GROWTH = {2026: 3.5, 2027: 3.0, 2028: 2.8, 2029: 2.5}
PREV_CPI_INFLATION = {2026: 2.6, 2027: 2.2, 2028: 2.0, 2029: 2.0}

# Updated forecast (Spring Statement 2026) — fill in from EFO tables
UPDATED_EARNINGS_GROWTH = {2026: None, 2027: None, 2028: None, 2029: None}
UPDATED_CPI_INFLATION = {2026: None, 2027: None, 2028: None, 2029: None}


def build_economic_tables():
    """Build markdown tables comparing previous and updated OBR forecasts."""
    rows_earnings = []
    rows_inflation = []
    for yr in [2026, 2027, 2028, 2029]:
        prev_e = PREV_EARNINGS_GROWTH[yr]
        upd_e = UPDATED_EARNINGS_GROWTH[yr]
        change_e = (
            f"{upd_e - prev_e:+.1f}pp" if upd_e is not None else ""
        )
        upd_e_str = f"{upd_e:.1f}%" if upd_e is not None else ""
        rows_earnings.append(
            f"| {yr} | {prev_e:.1f}% | {upd_e_str} | {change_e} |"
        )

        prev_i = PREV_CPI_INFLATION[yr]
        upd_i = UPDATED_CPI_INFLATION[yr]
        change_i = (
            f"{upd_i - prev_i:+.1f}pp" if upd_i is not None else ""
        )
        upd_i_str = f"{upd_i:.1f}%" if upd_i is not None else ""
        rows_inflation.append(
            f"| {yr} | {prev_i:.1f}% | {upd_i_str} | {change_i} |"
        )

    header = "| Year | Previous forecast | Updated forecast | Change |"
    sep = "|------|-------------------|------------------|--------|"
    earnings_table = "\n".join([header, sep] + rows_earnings)
    inflation_table = "\n".join([header, sep] + rows_inflation)
    return earnings_table, inflation_table


# ---------------------------------------------------------------------------
# 2. Household archetypes
# ---------------------------------------------------------------------------

EARNINGS_RANGE = np.arange(0, 100_001, 5_000)  # £0 to £100k in £5k steps


def make_situation(archetype: str, earnings: int) -> dict:
    """Return a PolicyEngine situation dict for a given archetype and earnings."""
    if archetype == "single_no_children":
        return {
            "people": {
                "adult": {
                    "age": {YEAR: 30},
                    "employment_income": {YEAR: earnings},
                },
            },
            "benunits": {
                "benunit": {"members": ["adult"]},
            },
            "households": {
                "household": {
                    "members": ["adult"],
                },
            },
        }

    elif archetype == "couple_no_children":
        return {
            "people": {
                "adult_1": {
                    "age": {YEAR: 35},
                    "employment_income": {YEAR: earnings},
                },
                "adult_2": {
                    "age": {YEAR: 33},
                    "employment_income": {YEAR: 0},
                },
            },
            "benunits": {
                "benunit": {"members": ["adult_1", "adult_2"]},
            },
            "households": {
                "household": {
                    "members": ["adult_1", "adult_2"],
                },
            },
        }

    elif archetype == "single_parent_2_children":
        return {
            "people": {
                "parent": {
                    "age": {YEAR: 30},
                    "employment_income": {YEAR: earnings},
                },
                "child_1": {"age": {YEAR: 7}},
                "child_2": {"age": {YEAR: 4}},
            },
            "benunits": {
                "benunit": {
                    "members": ["parent", "child_1", "child_2"],
                },
            },
            "households": {
                "household": {
                    "members": ["parent", "child_1", "child_2"],
                },
            },
        }

    elif archetype == "couple_2_children":
        return {
            "people": {
                "adult_1": {
                    "age": {YEAR: 35},
                    "employment_income": {YEAR: earnings},
                },
                "adult_2": {
                    "age": {YEAR: 33},
                    "employment_income": {YEAR: 0},
                },
                "child_1": {"age": {YEAR: 7}},
                "child_2": {"age": {YEAR: 4}},
            },
            "benunits": {
                "benunit": {
                    "members": [
                        "adult_1",
                        "adult_2",
                        "child_1",
                        "child_2",
                    ],
                },
            },
            "households": {
                "household": {
                    "members": [
                        "adult_1",
                        "adult_2",
                        "child_1",
                        "child_2",
                    ],
                },
            },
        }

    elif archetype == "single_pensioner":
        return {
            "people": {
                "pensioner": {
                    "age": {YEAR: 70},
                    "state_pension": {YEAR: 11_500},
                },
            },
            "benunits": {
                "benunit": {"members": ["pensioner"]},
            },
            "households": {
                "household": {
                    "members": ["pensioner"],
                },
            },
        }

    elif archetype == "pensioner_couple":
        return {
            "people": {
                "pensioner_1": {
                    "age": {YEAR: 70},
                    "state_pension": {YEAR: 11_500},
                },
                "pensioner_2": {
                    "age": {YEAR: 68},
                    "state_pension": {YEAR: 8_000},
                },
            },
            "benunits": {
                "benunit": {
                    "members": ["pensioner_1", "pensioner_2"],
                },
            },
            "households": {
                "household": {
                    "members": ["pensioner_1", "pensioner_2"],
                },
            },
        }

    raise ValueError(f"Unknown archetype: {archetype}")


ARCHETYPES = {
    "Single adult, no children": "single_no_children",
    "Couple, no children": "couple_no_children",
    "Single parent, 2 children": "single_parent_2_children",
    "Couple, 2 children": "couple_2_children",
    "Single pensioner": "single_pensioner",
    "Pensioner couple": "pensioner_couple",
}


# ---------------------------------------------------------------------------
# 3. Calculate household net income across the earnings distribution
# ---------------------------------------------------------------------------


def calculate_hnet_by_earnings(archetype_key: str) -> pd.DataFrame:
    """Calculate household net income at each earnings level for an archetype."""
    results = []
    for earnings in EARNINGS_RANGE:
        situation = make_situation(archetype_key, int(earnings))
        sim = Simulation(situation=situation)
        hnet = sim.calculate("household_net_income", YEAR)[0]
        results.append({"earnings": earnings, "household_net_income": hnet})
    return pd.DataFrame(results)


def generate_hnet_charts():
    """Generate line charts of hnet vs earnings for each archetype group."""

    # Group 1: working-age without children
    fig, ax = plt.subplots(figsize=(10, 6))
    for label, key in [
        ("Single adult, no children", "single_no_children"),
        ("Couple, no children", "couple_no_children"),
    ]:
        df = calculate_hnet_by_earnings(key)
        ax.plot(
            df["earnings"] / 1_000,
            df["household_net_income"] / 1_000,
            label=label,
        )
    ax.set_xlabel("Employment income (£k)")
    ax.set_ylabel("Household net income (£k)")
    ax.set_title("Working-age adults without children (2029)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "hnet_no_children.png", dpi=150)
    plt.close(fig)

    # Group 2: working-age with children
    fig, ax = plt.subplots(figsize=(10, 6))
    for label, key in [
        ("Single parent, 2 children", "single_parent_2_children"),
        ("Couple, 2 children", "couple_2_children"),
    ]:
        df = calculate_hnet_by_earnings(key)
        ax.plot(
            df["earnings"] / 1_000,
            df["household_net_income"] / 1_000,
            label=label,
        )
    ax.set_xlabel("Employment income (£k)")
    ax.set_ylabel("Household net income (£k)")
    ax.set_title("Working-age adults with children (2029)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "hnet_with_children.png", dpi=150)
    plt.close(fig)

    # Group 3: pensioners (single chart, no earnings sweep — just bar chart)
    fig, ax = plt.subplots(figsize=(8, 5))
    pensioner_hnet = {}
    for label, key in [
        ("Single pensioner", "single_pensioner"),
        ("Pensioner couple", "pensioner_couple"),
    ]:
        situation = make_situation(key, 0)
        sim = Simulation(situation=situation)
        hnet = sim.calculate("household_net_income", YEAR)[0]
        pensioner_hnet[label] = hnet

    ax.bar(pensioner_hnet.keys(), [v / 1_000 for v in pensioner_hnet.values()])
    ax.set_ylabel("Household net income (£k)")
    ax.set_title("Pensioner household net income (2029)")
    ax.grid(True, alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "hnet_pensioners.png", dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------
# 4. Summary table: hnet at median earnings for each archetype
# ---------------------------------------------------------------------------

def get_median_earnings() -> float:
    """Compute weighted median employment income for working-age adults
    with positive earnings from the PE UK microsimulation data."""
    sim = Microsimulation()
    income = sim.calculate("employment_income", YEAR)
    age = sim.calculate("age", YEAR)

    mask = (age >= 18) & (age < 66) & (income > 0)
    return float(income[mask].median())


def generate_summary_table() -> str:
    """Generate the markdown summary table of hnet by household type."""
    median_earnings = get_median_earnings()
    print(f"  Using median earnings: £{median_earnings:,.0f}")
    rows = []
    for label, key in ARCHETYPES.items():
        if "pensioner" in key:
            earnings = 0
        else:
            earnings = median_earnings

        situation = make_situation(key, earnings)
        sim = Simulation(situation=situation)
        hnet = sim.calculate("household_net_income", YEAR)[0]

        # TODO: once we have the updated forecast, run a second simulation
        # with updated economic assumptions and compute the change.
        prev_hnet = hnet  # placeholder — same as current until we have reform
        updated_hnet = hnet  # placeholder
        change = updated_hnet - prev_hnet

        rows.append(
            f"| {label} | £{prev_hnet:,.0f} | £{updated_hnet:,.0f} | £{change:+,.0f} |"
        )

    header = "| Household type | Previous 2029 hnet | Updated 2029 hnet | Change |"
    sep = "|----------------|--------------------|--------------------|--------|"
    return "\n".join([header, sep] + rows)


# ---------------------------------------------------------------------------
# 5. Main: generate everything and write updated markdown
# ---------------------------------------------------------------------------


def main():
    print("Generating economic forecast tables...")
    earnings_table, inflation_table = build_economic_tables()

    print("Generating household net income charts...")
    generate_hnet_charts()

    print("Generating summary table...")
    summary_table = generate_summary_table()

    # Read the template markdown
    md_path = Path(__file__).parent / "spring-statement-2026-blog.md"
    md = md_path.read_text()

    # Inject the earnings growth table
    md = md.replace(
        "| Year | Previous forecast | Updated forecast | Change |\n"
        "|------|-------------------|------------------|--------|\n"
        "| 2026 | | | |\n"
        "| 2027 | | | |\n"
        "| 2028 | | | |\n"
        "| 2029 | | | |\n"
        "\n"
        "### Inflation",
        earnings_table + "\n\n### Inflation",
    )

    # Inject the inflation table
    md = md.replace(
        "| Year | Previous forecast | Updated forecast | Change |\n"
        "|------|-------------------|------------------|--------|\n"
        "| 2026 | | | |\n"
        "| 2027 | | | |\n"
        "| 2028 | | | |\n"
        "| 2029 | | | |",
        inflation_table,
    )

    # Inject chart references
    md = md.replace(
        "[Line charts showing projected household net income across the earnings distribution for different household types.]",
        "",
    )
    md = md.replace(
        "[Brief description of the impact on this group.]\n\n"
        "#### Working-age adults with children",
        "![Working-age adults without children](output/hnet_no_children.png)\n\n"
        "#### Working-age adults with children",
    )
    md = md.replace(
        "[Brief description of the impact on this group.]\n\n"
        "#### Pensioners",
        "![Working-age adults with children](output/hnet_with_children.png)\n\n"
        "#### Pensioners",
    )
    md = md.replace(
        "[Brief description of the impact on this group.]\n\n"
        "### Change in net income from previous forecast",
        "![Pensioner households](output/hnet_pensioners.png)\n\n"
        "### Change in net income from previous forecast",
    )

    # Inject summary table
    md = md.replace(
        "[Table or chart showing the change in projected 2029 household net income by family type, comparing the previous forecast to the updated one.]\n\n"
        "| Household type | Previous 2029 hnet | Updated 2029 hnet | Change |\n"
        "|----------------|--------------------|--------------------|--------|\n"
        "| Single adult, no children | | | |\n"
        "| Couple, no children | | | |\n"
        "| Single parent, 2 children | | | |\n"
        "| Couple, 2 children | | | |\n"
        "| Single pensioner | | | |\n"
        "| Pensioner couple | | | |",
        summary_table,
    )

    md_path.write_text(md)
    print(f"Updated blog post written to {md_path}")
    print(f"Charts saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
