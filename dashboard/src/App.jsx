import { useState, useEffect } from "react";
import EconomicForecast from "./components/EconomicForecast";
import FiscalOutlook from "./components/FiscalOutlook";
import HouseholdImpact from "./components/HouseholdImpact";
import "./App.css";

function App() {
  const [forecast, setForecast] = useState(null);
  const [baseline, setBaseline] = useState(null);
  const [stats, setStats] = useState(null);
  const [comparison, setComparison] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    Promise.all([
      fetch("/data/economic_forecast.json").then((r) => r.json()),
      fetch("/data/baseline_economic_assumptions.json").then((r) => r.json()),
      fetch("/data/household_stats.json").then((r) => r.json()),
      fetch("/data/household_comparison.json").then((r) => r.json()),
    ])
      .then(([forecastData, baselineData, statsData, compData]) => {
        setForecast(forecastData);
        setBaseline(baselineData);
        setStats(statsData);
        setComparison(compData);
      })
      .catch((err) => setError(err.message));
  }, []);

  const loading = !forecast || !stats || !comparison;

  return (
    <div className="app">
      <main className="main-content">
        <div className="title-row">
          <h1>UK Spring Statement 2026</h1>
        </div>

        <p className="dashboard-intro">
          PolicyEngine analysis of the OBR economic forecast revisions and their
          impact on household incomes across the UK. Data sourced from the
          Enhanced Family Resources Survey and PolicyEngine UK microsimulation
          model.
        </p>

        {error && <p className="loading">Error loading data: {error}</p>}
        {loading && !error && <p className="loading">Loading data...</p>}
        {!loading && !error && (
          <div className="results-container">
            <EconomicForecast forecast={forecast} baseline={baseline} />
            <FiscalOutlook />
            <HouseholdImpact stats={stats} comparison={comparison} />

            <footer className="footer">
              <p>
                Built by{" "}
                <a
                  href="https://policyengine.org"
                  target="_blank"
                  rel="noreferrer"
                >
                  PolicyEngine
                </a>{" "}
                using the Enhanced Family Resources Survey and PolicyEngine UK
                microsimulation model.
              </p>
            </footer>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
