import { useState, useEffect } from "react";
import EconomicForecast from "./components/EconomicForecast";
import HouseholdImpact from "./components/HouseholdImpact";
import PersonalCalculator from "./components/PersonalCalculator";
import "./App.css";

function App() {
  const [forecast, setForecast] = useState(null);
  const [baseline, setBaseline] = useState(null);
  const [stats, setStats] = useState(null);
  const [comparison, setComparison] = useState(null);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState("analysis");

  // Initialize from URL parameters
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const tabParam = params.get("tab");
    if (tabParam === "calculator") setActiveTab("calculator");
    else setActiveTab("analysis");
  }, []);

  // Update URL when tab changes
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    if (activeTab === "calculator") params.set("tab", "calculator");
    else params.delete("tab");
    const newUrl = params.toString()
      ? `?${params.toString()}`
      : window.location.pathname;
    window.history.replaceState({}, "", newUrl);
  }, [activeTab]);

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
          <h1>Spring Statement 2026: OBR forecast revisions and household impact</h1>
        </div>

        {/* Tab navigation */}
        <div className="tab-navigation">
          <button
            className={`tab-button ${activeTab === "analysis" ? "active" : ""}`}
            onClick={() => setActiveTab("analysis")}
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M3 3v18h18" />
              <path d="M18 17V9" />
              <path d="M13 17V5" />
              <path d="M8 17v-3" />
            </svg>
            Population Analysis
          </button>
          <button
            className={`tab-button ${activeTab === "calculator" ? "active" : ""}`}
            onClick={() => setActiveTab("calculator")}
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
              <circle cx="12" cy="7" r="4" />
            </svg>
            Personal Calculator
          </button>
        </div>

        {activeTab === "analysis" && (
          <>
            {error && <p className="loading">Error loading data: {error}</p>}
            {loading && !error && <p className="loading">Loading data...</p>}
            {!loading && !error && (
              <div className="results-container">
                <EconomicForecast forecast={forecast} baseline={baseline} />
                <HouseholdImpact stats={stats} comparison={comparison} />
              </div>
            )}
          </>
        )}

        {activeTab === "calculator" && <PersonalCalculator />}
      </main>
    </div>
  );
}

export default App;
