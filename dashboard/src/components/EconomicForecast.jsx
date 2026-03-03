import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";
import ForecastTable from "./ForecastTable";

const COLORS = {
  previous: "#9ca3af",
  updated: "#0d9488",
};

function ForecastLineChart({ data, title, description, unit }) {
  return (
    <div className="section-card">
      <h2>{title}</h2>
      <p>{description}</p>
      <div className="chart-container">
        <ResponsiveContainer width="100%" height={320}>
          <LineChart
            data={data}
            margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey="year" tick={{ fontSize: 13 }} />
            <YAxis
              tickFormatter={(v) => `${v}${unit}`}
              tick={{ fontSize: 13 }}
              label={{
                value: `Growth rate (${unit})`,
                angle: -90,
                position: "insideLeft",
                offset: -30,
                style: { fontSize: 12, fill: "#6b7280" },
              }}
            />
            <Tooltip
              formatter={(v) =>
                v != null ? `${v.toFixed(1)}${unit}` : "—"
              }
              contentStyle={{
                background: "#fff",
                border: "1px solid #e5e7eb",
                borderRadius: 8,
                fontSize: 13,
              }}
            />
            <Legend wrapperStyle={{ fontSize: 13 }} />
            <Line
              type="monotone"
              dataKey="previous"
              name="Previous forecast"
              stroke={COLORS.previous}
              strokeWidth={2}
              dot={{ r: 4 }}
              animationDuration={500}
            />
            <Line
              type="monotone"
              dataKey="updated"
              name="Updated forecast"
              stroke={COLORS.updated}
              strokeWidth={2.5}
              dot={{ r: 4 }}
              connectNulls={false}
              animationDuration={500}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default function EconomicForecast({ forecast, baseline }) {
  if (!forecast) return null;

  const earningsRows = forecast.earnings_growth.map((r) => [
    r.year,
    r.previous,
    r.updated,
    r.change,
  ]);

  const inflationRows = forecast.cpi_inflation.map((r) => [
    r.year,
    r.previous,
    r.updated,
    r.change,
  ]);

  const rpiRows = forecast.rpi_inflation.map((r) => [
    r.year,
    r.previous,
    r.updated,
    r.change,
  ]);

  const housePricesRows = (forecast.house_prices || []).map((r) => [
    r.year,
    r.previous,
    r.updated,
    r.change,
  ]);

  const perCapitaGdpRows = (forecast.per_capita_gdp || []).map((r) => [
    r.year,
    r.previous,
    r.updated,
    r.change,
  ]);

  const socialRentRows = (forecast.social_rent || []).map((r) => [
    r.year,
    r.previous,
    r.updated,
    r.change,
  ]);

  const columns = ["Year", "Previous forecast", "Updated forecast", "Change"];

  return (
    <>
      <div className="section-card" style={{ animationDelay: "0.15s" }}>
        <h2>Economic forecast: what changed</h2>
        <p>
          Key revisions to the OBR's economic forecast compared to the Autumn
          Statement November 2025
          {baseline ? ` (source: ${baseline.source})` : ""}.
        </p>
      </div>

      <div className="charts-grid charts-grid-3">
        <ForecastLineChart
          data={forecast.earnings_growth}
          title="Earnings growth"
          description="OBR projected average earnings year-on-year growth"
          unit="%"
        />
        <ForecastLineChart
          data={forecast.cpi_inflation}
          title="CPI inflation"
          description="OBR projected Consumer Price Index year-on-year growth"
          unit="%"
        />
        <ForecastLineChart
          data={forecast.rpi_inflation}
          title="RPI inflation"
          description="OBR projected Retail Price Index year-on-year growth"
          unit="%"
        />
      </div>

      <div className="charts-grid charts-grid-3">
        <div className="section-card" style={{ margin: 0 }}>
          <h3>Earnings growth data</h3>
          <ForecastTable columns={columns} rows={earningsRows} />
        </div>
        <div className="section-card" style={{ margin: 0 }}>
          <h3>CPI inflation data</h3>
          <ForecastTable columns={columns} rows={inflationRows} />
        </div>
        <div className="section-card" style={{ margin: 0 }}>
          <h3>RPI inflation data</h3>
          <ForecastTable columns={columns} rows={rpiRows} />
        </div>
      </div>

      <div className="charts-grid charts-grid-3">
        <ForecastLineChart
          data={forecast.house_prices || []}
          title="House prices"
          description="OBR projected house prices year-on-year growth"
          unit="%"
        />
        <ForecastLineChart
          data={forecast.per_capita_gdp || []}
          title="Per capita GDP"
          description="OBR projected nominal per capita GDP year-on-year growth"
          unit="%"
        />
        <ForecastLineChart
          data={forecast.social_rent || []}
          title="Social rent"
          description="OBR projected social rent year-on-year growth (CPI+1%, lagged)"
          unit="%"
        />
      </div>

      <div className="charts-grid charts-grid-3">
        <div className="section-card" style={{ margin: 0 }}>
          <h3>House prices data</h3>
          <ForecastTable columns={columns} rows={housePricesRows} />
        </div>
        <div className="section-card" style={{ margin: 0 }}>
          <h3>Per capita GDP data</h3>
          <ForecastTable columns={columns} rows={perCapitaGdpRows} />
        </div>
        <div className="section-card" style={{ margin: 0 }}>
          <h3>Social rent data</h3>
          <ForecastTable columns={columns} rows={socialRentRows} />
        </div>
      </div>
    </>
  );
}
