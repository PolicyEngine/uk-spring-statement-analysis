import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import ForecastTable from "./ForecastTable";

const TEAL = "#0d9488";
const TEAL_LIGHT = "#5eead4";
const GRAY = "#9ca3af";

function shorten(group) {
  return group
    .replace("Single adult, no children", "Single adult")
    .replace("Couple, no children", "Couple")
    .replace("Couple with children", "Couple + kids")
    .replace("Single parent", "Single parent")
    .replace("Single pensioner", "Single pensioner")
    .replace("Pensioner couple", "Pensioner couple");
}

function formatCurrency(v) {
  return `£${v.toLocaleString("en-GB", { maximumFractionDigits: 0 })}`;
}

function HnetBarChart({ data }) {
  const chartData = data
    .map((d) => ({
      group: shorten(d.group),
      mean_hnet: Math.round(d.mean_hnet),
    }))
    .sort((a, b) => a.mean_hnet - b.mean_hnet);

  return (
    <div className="section-card">
      <h2>Average household net income by family type</h2>
      <p>Weighted mean household net income (2029 projection)</p>
      <div className="chart-container">
        <ResponsiveContainer width="100%" height={360}>
          <BarChart
            data={chartData}
            layout="vertical"
            margin={{ top: 10, right: 40, left: 10, bottom: 0 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis
              type="number"
              tickFormatter={(v) => `£${(v / 1000).toFixed(0)}k`}
              tick={{ fontSize: 13 }}
            />
            <YAxis
              type="category"
              dataKey="group"
              width={140}
              tick={{ fontSize: 13 }}
            />
            <Tooltip
              formatter={(v) => formatCurrency(v)}
              contentStyle={{
                background: "#fff",
                border: "1px solid #e5e7eb",
                borderRadius: 8,
                fontSize: 13,
              }}
            />
            <Bar
              dataKey="mean_hnet"
              name="Mean hnet"
              fill={TEAL}
              barSize={28}
              animationDuration={500}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default function HouseholdImpact({ stats, comparison }) {
  if (!stats || !comparison) return null;

  const statsColumns = ["Household type", "Mean hnet", "Median hnet", "Weighted N"];
  const statsRows = stats.map((r) => [
    r.group,
    r.mean_hnet,
    r.median_hnet,
    Math.round(r.weighted_n).toLocaleString("en-GB"),
  ]);

  const compColumns = [
    "Household type",
    "Baseline hnet",
    "Reformed hnet",
    "Change",
  ];
  const compRows = comparison.map((r) => [
    r.group,
    r.baseline_hnet,
    r.reformed_hnet,
    r.change,
  ]);

  return (
    <>
      <div className="section-card" style={{ animationDelay: "0.35s" }}>
        <h2>What this means for households</h2>
        <p>
          Using PolicyEngine's microsimulation model, we calculated average
          household net income for six household groups under the baseline and
          updated forecasts.
        </p>
      </div>

      <div className="hero-chart">
        <HnetBarChart data={stats} />
      </div>

      <div className="section-card" style={{ animationDelay: "0.4s" }}>
        <h3>Household net income statistics</h3>
        <ForecastTable columns={statsColumns} rows={statsRows} format="gbp" />
      </div>

      <div className="section-card" style={{ animationDelay: "0.5s" }}>
        <h3>Change in net income from previous forecast</h3>
        <ForecastTable columns={compColumns} rows={compRows} format="gbp" />
      </div>
    </>
  );
}
