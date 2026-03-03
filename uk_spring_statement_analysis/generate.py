"""Main entrypoint: generate all blog post data and update the markdown."""

from pathlib import Path

from .simulation import load_sim, compute_group_stats
from .charts import generate_hnet_chart
from .tables import build_economic_tables, generate_summary_table
from .json_export import export_economic_forecast, export_household_data


def main():
    print("Generating economic forecast tables...")
    earnings_table, inflation_table = build_economic_tables()

    print("Loading baseline microsimulation...")
    baseline = load_sim()
    baseline_stats = compute_group_stats(baseline)
    print(baseline_stats.to_string(index=False))

    # TODO: once we have the Spring Statement reform, load a reformed sim:
    # from policyengine_uk import Scenario
    # scenario = Scenario(parameter_changes={...})
    # reformed = load_sim(scenario=scenario)
    # reformed_stats = compute_group_stats(reformed)
    reformed_stats = None

    print("Generating chart...")
    generate_hnet_chart(baseline_stats)

    print("Generating summary table...")
    summary_table = generate_summary_table(baseline_stats, reformed_stats)

    # Export JSON for the React dashboard
    print("Exporting JSON for dashboard...")
    export_economic_forecast()
    export_household_data(baseline_stats, reformed_stats)

    # Read the template markdown
    md_path = Path(__file__).parents[1] / "spring-statement-2026-blog.md"
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


if __name__ == "__main__":
    main()
