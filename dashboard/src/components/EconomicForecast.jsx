import { useState } from "react";
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
import ForecastTable from "./ForecastTable";

const COLORS = {
  previous: "#9ca3af",
  updated: "#0d9488",
};

const TABLE_COLUMNS = [
  "Year",
  "Pre-Spring Statement",
  "Spring Statement",
  "Change",
];

function getYDomain(data) {
  const vals = data.flatMap((d) =>
    [d.previous, d.updated].filter((v) => v != null),
  );
  if (vals.length === 0) return [0, 1];
  const min = Math.min(...vals);
  const max = Math.max(...vals);
  const pad = Math.max((max - min) * 0.3, 0.2);
  // Round down/up to nearest 0.5
  const lo = Math.floor((min - pad) * 2) / 2;
  const hi = Math.ceil((max + pad) * 2) / 2;
  return [Math.max(lo, 0), hi];
}

function ForecastCard({ data, title, description, unit }) {
  const [view, setView] = useState("chart");

  const rows = data.map((r) => [r.year, r.previous, r.updated, r.change]);
  const yDomain = getYDomain(data);

  return (
    <div className="section-card" style={{ margin: 0 }}>
      <div className="card-header-row">
        <div>
          <h2>{title}</h2>
          <p>{description}</p>
        </div>
        <div className="view-toggle">
          <button
            className={view === "chart" ? "active" : ""}
            onClick={() => setView("chart")}
          >
            Chart
          </button>
          <button
            className={view === "table" ? "active" : ""}
            onClick={() => setView("table")}
          >
            Table
          </button>
        </div>
      </div>

      {view === "chart" ? (
        <div className="chart-container">
          <ResponsiveContainer width="100%" height={320}>
            <LineChart
              data={data}
              margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="year" tick={{ fontSize: 13 }} />
              <YAxis
                domain={yDomain}
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
                  v != null ? `${v.toFixed(1)}${unit}` : "\u2014"
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
                name="Pre-Spring Statement"
                stroke={COLORS.previous}
                strokeWidth={2}
                dot={{ r: 4 }}
                animationDuration={500}
              />
              <Line
                type="monotone"
                dataKey="updated"
                name="Spring Statement"
                stroke={COLORS.updated}
                strokeWidth={2.5}
                dot={{ r: 4 }}
                connectNulls={false}
                animationDuration={500}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      ) : (
        <ForecastTable columns={TABLE_COLUMNS} rows={rows} />
      )}
    </div>
  );
}

export default function EconomicForecast({ forecast }) {
  if (!forecast) return null;

  return (
    <>
      <div className="section-heading" style={{ animationDelay: "0.15s" }}>
        <h2>Economic forecast: what changed</h2>
        <p>
          Comparing pre-Spring Statement 2026 (OBR EFO November 2025) with
          Spring Statement 2026 (OBR EFO March 2026) forecasts.
        </p>
      </div>

      <div className="charts-grid charts-grid-3">
        <ForecastCard
          data={forecast.earnings_growth}
          title="Earnings growth"
          description="OBR projected average earnings year-on-year growth"
          unit="%"
        />
        <ForecastCard
          data={forecast.cpi_inflation}
          title="CPI inflation"
          description="OBR projected Consumer Price Index year-on-year growth"
          unit="%"
        />
        <ForecastCard
          data={forecast.rpi_inflation}
          title="RPI inflation"
          description="OBR projected Retail Price Index year-on-year growth"
          unit="%"
        />
      </div>

      <div className="charts-grid charts-grid-3">
        <ForecastCard
          data={forecast.house_prices || []}
          title="House prices"
          description="OBR projected house prices year-on-year growth"
          unit="%"
        />
        <ForecastCard
          data={forecast.per_capita_gdp || []}
          title="Per capita GDP"
          description="OBR projected nominal per capita GDP year-on-year growth"
          unit="%"
        />
        <ForecastCard
          data={forecast.social_rent || []}
          title="Social rent"
          description="OBR projected social rent year-on-year growth"
          unit="%"
        />
      </div>
    </>
  );
}
