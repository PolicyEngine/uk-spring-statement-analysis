"""
Generate data and charts for the Spring Statement 2026 blog post.

This script:
1. Loads the PE UK microsimulation (Enhanced FRS)
2. Groups benefit units by family type and pensioner status
3. Calculates weighted average and median household net income per group
4. Compares baseline vs updated economic assumptions (earnings growth, inflation)
5. Outputs markdown tables and saves charts for the blog post

NOTE: The OBR economic determinants below are placeholders.
Replace with actual values from the EFO tables once published.
"""

from policyengine_uk import Microsimulation, Scenario
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
# 2. Household group definitions (using microsimulation data)
# ---------------------------------------------------------------------------

GROUPS = {
    "Single adult, no children": lambda ft, pen: (ft == "SINGLE") & (pen == 0),
    "Couple, no children": lambda ft, pen: (ft == "COUPLE_NO_CHILDREN") & (pen == 0),
    "Single parent": lambda ft, pen: ft == "LONE_PARENT",
    "Couple with children": lambda ft, pen: ft == "COUPLE_WITH_CHILDREN",
    "Single pensioner": lambda ft, pen: (ft == "SINGLE") & (pen == 1),
    "Pensioner couple": lambda ft, pen: (ft == "COUPLE_NO_CHILDREN") & (pen == 1),
}


def load_sim(scenario=None):
    """Load a Microsimulation, optionally with a reform scenario."""
    if scenario is not None:
        return Microsimulation(scenario=scenario)
    return Microsimulation()


def classify_benunits(sim):
    """Return family_type and is_pensioner_benunit MicroSeries at benunit level."""
    family_type = sim.calculate("family_type", YEAR)
    is_sp_age = sim.calculate("is_SP_age", YEAR, map_to="benunit")
    benunit_adults = sim.calculate("benunit_count_adults", YEAR)
    is_pensioner_bu = (is_sp_age >= benunit_adults).astype(float)
    return family_type, is_pensioner_bu


# ---------------------------------------------------------------------------
# 3. Calculate average household net income by group
# ---------------------------------------------------------------------------


def compute_group_stats(sim):
    """Return a DataFrame with weighted mean and median hnet per group."""
    family_type, is_pensioner_bu = classify_benunits(sim)
    hnet = sim.calculate("household_net_income", YEAR, map_to="benunit")

    rows = []
    for label, mask_fn in GROUPS.items():
        mask = mask_fn(family_type, is_pensioner_bu)
        mean_hnet = float(hnet[mask].mean())
        median_hnet = float(hnet[mask].median())
        count = float(mask.sum())
        rows.append({
            "group": label,
            "mean_hnet": mean_hnet,
            "median_hnet": median_hnet,
            "weighted_n": count,
        })
    return pd.DataFrame(rows)


def generate_hnet_chart(baseline_stats):
    """Generate a bar chart of average hnet by household group."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(
        baseline_stats["group"],
        baseline_stats["mean_hnet"] / 1_000,
    )
    ax.set_xlabel("Average household net income (£k)")
    ax.set_title(f"Average household net income by family type ({YEAR})")
    ax.grid(True, alpha=0.3, axis="x")
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "hnet_by_group.png", dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------
# 4. Summary table: compare baseline vs reform
# ---------------------------------------------------------------------------


def generate_summary_table(baseline_stats, reformed_stats=None) -> str:
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
            updated = prev  # placeholder until we have the reform

        change = updated - prev
        rows.append(
            f"| {label} | £{prev:,.0f} | £{updated:,.0f} | £{change:+,.0f} |"
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

    print("Loading baseline microsimulation...")
    baseline = load_sim()
    baseline_stats = compute_group_stats(baseline)
    print(baseline_stats.to_string(index=False))

    # TODO: once we have the Spring Statement reform, load a reformed sim:
    # scenario = Scenario(parameter_changes={...})
    # reformed = load_sim(scenario=scenario)
    # reformed_stats = compute_group_stats(reformed)
    reformed_stats = None

    print("Generating chart...")
    generate_hnet_chart(baseline_stats)

    print("Generating summary table...")
    summary_table = generate_summary_table(baseline_stats, reformed_stats)

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

    # Inject chart reference
    md = md.replace(
        "[Line charts showing projected household net income across the earnings distribution for different household types.]",
        "![Average household net income by family type](output/hnet_by_group.png)",
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
