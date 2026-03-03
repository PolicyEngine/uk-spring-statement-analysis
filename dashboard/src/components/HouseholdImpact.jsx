import { useState } from "react";
import ForecastTable from "./ForecastTable";

const YEARS = ["2026", "2027", "2028", "2029"];

export default function HouseholdImpact({ allStats, allComparison }) {
  const [selectedYear, setSelectedYear] = useState("2029");

  if (!allStats || !allComparison) return null;

  const stats = allStats[selectedYear] || [];
  const comparison = allComparison[selectedYear] || [];

  const mergedColumns = [
    "Household type",
    "Number of households",
    "Median income (post-Statement)",
    "Mean income (pre-Statement)",
    "Mean income (post-Statement)",
    "Change in mean income",
  ];
  const mergedRows = stats.map((r) => {
    const comp = comparison.find((c) => c.group === r.group) || {};
    return [
      r.group,
      (r.weighted_n / 1_000_000).toFixed(2) + "m",
      r.median_hnet,
      comp.baseline_hnet,
      comp.reformed_hnet,
      comp.change,
    ];
  });

  return (
    <>
      <div className="section-heading" style={{ animationDelay: "0.35s" }}>
        <h2>What this means for households</h2>
        <p>
          Using PolicyEngine's microsimulation model, we estimated the effect
          of the above economic forecast changes on average household net
          income for six household groups.
        </p>
      </div>

      <div className="section-card" style={{ animationDelay: "0.4s" }}>
        <div className="card-header-row">
          <h3>Household income summary</h3>
          <div className="view-toggle">
            {YEARS.map((yr) => (
              <button
                key={yr}
                className={selectedYear === yr ? "active" : ""}
                onClick={() => setSelectedYear(yr)}
              >
                {yr}
              </button>
            ))}
          </div>
        </div>
        <ForecastTable columns={mergedColumns} rows={mergedRows} format="gbp" />
      </div>
    </>
  );
}
