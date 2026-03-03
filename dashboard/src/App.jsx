import useData from "./hooks/useData";
import Header from "./components/Header";
import EconomicForecast from "./components/EconomicForecast";
import FiscalOutlook from "./components/FiscalOutlook";
import HouseholdImpact from "./components/HouseholdImpact";
import Footer from "./components/Footer";

export default function App() {
  const { data: forecast, error: forecastErr } = useData("/data/economic_forecast.json");
  const { data: stats, error: statsErr } = useData("/data/household_stats.json");
  const { data: comparison, error: compErr } = useData("/data/household_comparison.json");

  const loading = !forecast || !stats || !comparison;
  const error = forecastErr || statsErr || compErr;

  return (
    <>
      <Header />
      <main className="dashboard">
        {error && <p className="loading">Error loading data: {error.message}</p>}
        {loading && !error && <p className="loading">Loading data...</p>}
        {!loading && !error && (
          <>
            <EconomicForecast forecast={forecast} />
            <FiscalOutlook />
            <HouseholdImpact stats={stats} comparison={comparison} />
          </>
        )}
      </main>
      <Footer />
    </>
  );
}
