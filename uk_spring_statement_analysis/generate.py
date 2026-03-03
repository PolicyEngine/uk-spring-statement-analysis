"""Main entrypoint: generate all blog post data and update the markdown."""

from pathlib import Path

from .simulation import load_sim, compute_group_stats
from .charts import generate_hnet_chart
from .tables import build_economic_tables, generate_summary_table
from .json_export import export_economic_forecast, export_household_data


# Spring Statement 2026 updated values (OBR EFO March 2026, Table A.1)
# Passed as parameter_changes with applied_before_data_load=True so
# uprating uses the new economic assumptions.
SPRING_STATEMENT_PARAMS = {
    "gov.economic_assumptions.yoy_growth.obr.average_earnings": {
        "2026-01-01": 0.034,
        "2027-01-01": 0.024,
        "2028-01-01": 0.021,
        "2029-01-01": 0.022,
    },
    "gov.economic_assumptions.yoy_growth.obr.consumer_price_index": {
        "2026-01-01": 0.023,
        "2027-01-01": 0.020,
        "2028-01-01": 0.020,
        "2029-01-01": 0.020,
    },
    "gov.economic_assumptions.yoy_growth.obr.rpi": {
        "2026-01-01": 0.031,
        "2027-01-01": 0.030,
        "2028-01-01": 0.028,
        "2029-01-01": 0.029,
    },
    "gov.economic_assumptions.yoy_growth.obr.house_prices": {
        "2026-01-01": 0.024,
        "2027-01-01": 0.029,
        "2028-01-01": 0.027,
        "2029-01-01": 0.026,
    },
    "gov.economic_assumptions.yoy_growth.obr.per_capita.gdp": {
        "2026-01-01": 0.0292,
        "2027-01-01": 0.0323,
        "2028-01-01": 0.0310,
        "2029-01-01": 0.0296,
    },
    "gov.economic_assumptions.yoy_growth.obr.social_rent": {
        "2026-01-01": 0.044,
        "2027-01-01": 0.033,
        "2028-01-01": 0.030,
        "2029-01-01": 0.030,
    },
}


def main():
    from policyengine_uk.utils.scenario import Scenario

    print("Generating economic forecast tables...")
    earnings_table, inflation_table, rpi_table = build_economic_tables()

    print("Loading baseline microsimulation...")
    baseline = load_sim()
    baseline_stats = compute_group_stats(baseline)
    print("Baseline stats:")
    print(baseline_stats.to_string(index=False))

    # Create a Scenario with applied_before_data_load=True so the
    # parameter changes feed into uprating (not just the formula graph).
    print("Loading reformed microsimulation (Spring Statement 2026)...")
    scenario = Scenario(
        parameter_changes=SPRING_STATEMENT_PARAMS,
        applied_before_data_load=True,
    )
    reformed = load_sim(scenario=scenario)
    reformed_stats = compute_group_stats(reformed)
    print("Reformed stats:")
    print(reformed_stats.to_string(index=False))

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
