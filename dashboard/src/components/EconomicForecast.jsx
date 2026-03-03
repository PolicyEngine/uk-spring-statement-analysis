import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import Section from "./Section";
import ForecastTable from "./ForecastTable";

const COLORS = { previous: "#8da0b5", updated: "#2c6496" };

function ForecastLineChart({ data, title, unit }) {
  return (
    <div className="chart-container">
      <h3>{title}</h3>
      <ResponsiveContainer width="100%" height={280}>
        <LineChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#dde3ea" />
          <XAxis dataKey="year" />
          <YAxis tickFormatter={(v) => `${v}${unit}`} />
          <Tooltip formatter={(v) => (v != null ? `${v.toFixed(1)}${unit}` : "—")} />
          <Legend />
          <Line
            type="monotone"
            dataKey="previous"
            name="Previous forecast"
            stroke={COLORS.previous}
            strokeWidth={2}
            dot={{ r: 4 }}
          />
          <Line
            type="monotone"
            dataKey="updated"
            name="Updated forecast"
            stroke={COLORS.updated}
            strokeWidth={2}
            dot={{ r: 4 }}
            connectNulls={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default function EconomicForecast({ forecast }) {
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

  const earningsCols = ["Year", "Previous forecast", "Updated forecast", "Change"];
  const inflationCols = earningsCols;

  return (
    <Section title="Economic forecast: what changed">
      <p>
        Key revisions to the OBR's economic forecast compared to the Autumn Statement
        2025.
      </p>

      <h3>Earnings growth</h3>
      <ForecastLineChart
        data={forecast.earnings_growth}
        title="Earnings growth projections (%)"
        unit="%"
      />
      <ForecastTable columns={earningsCols} rows={earningsRows} />

      <h3>CPI Inflation</h3>
      <ForecastLineChart
        data={forecast.cpi_inflation}
        title="CPI inflation projections (%)"
        unit="%"
      />
      <ForecastTable columns={inflationCols} rows={inflationRows} />
    </Section>
  );
}
