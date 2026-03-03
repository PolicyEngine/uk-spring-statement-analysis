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
import Section from "./Section";
import ForecastTable from "./ForecastTable";

const PE_BLUE = "#2c6496";
const PE_BLUE_LIGHT = "#8da0b5";

function shorten(group) {
  return group
    .replace("Single adult, no children", "Single adult")
    .replace("Couple, no children", "Couple")
    .replace("Couple with children", "Couple + kids")
    .replace("Single parent", "Single parent")
    .replace("Single pensioner", "Single pensioner")
    .replace("Pensioner couple", "Pensioner couple");
}

function HnetBarChart({ data }) {
  const chartData = data.map((d) => ({
    group: shorten(d.group),
    mean_hnet: Math.round(d.mean_hnet),
  }));

  return (
    <div className="chart-container">
      <h3>Average household net income by family type (2029)</h3>
      <ResponsiveContainer width="100%" height={320}>
        <BarChart
          data={chartData}
          layout="vertical"
          margin={{ top: 10, right: 30, left: 120, bottom: 0 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#dde3ea" />
          <XAxis
            type="number"
            tickFormatter={(v) => `£${(v / 1000).toFixed(0)}k`}
          />
          <YAxis type="category" dataKey="group" width={110} />
          <Tooltip
            formatter={(v) =>
              `£${v.toLocaleString("en-GB", { maximumFractionDigits: 0 })}`
            }
          />
          <Bar dataKey="mean_hnet" name="Mean hnet" fill={PE_BLUE} barSize={24} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

function ComparisonChart({ data }) {
  const chartData = data.map((d) => ({
    group: shorten(d.group),
    baseline: Math.round(d.baseline_hnet),
    reformed: Math.round(d.reformed_hnet),
  }));

  return (
    <div className="chart-container">
      <h3>Baseline vs reformed household net income</h3>
      <ResponsiveContainer width="100%" height={320}>
        <BarChart
          data={chartData}
          margin={{ top: 10, right: 30, left: 10, bottom: 0 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#dde3ea" />
          <XAxis dataKey="group" tick={{ fontSize: 12 }} />
          <YAxis tickFormatter={(v) => `£${(v / 1000).toFixed(0)}k`} />
          <Tooltip
            formatter={(v) =>
              `£${v.toLocaleString("en-GB", { maximumFractionDigits: 0 })}`
            }
          />
          <Legend />
          <Bar dataKey="baseline" name="Baseline" fill={PE_BLUE_LIGHT} />
          <Bar dataKey="reformed" name="Reformed" fill={PE_BLUE} />
        </BarChart>
      </ResponsiveContainer>
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
    <Section title="What this means for households">
      <p>
        Using PolicyEngine's microsimulation model, we calculated average household
        net income for six household groups under the baseline and updated forecasts.
      </p>

      <HnetBarChart data={stats} />

      <h3>Household net income statistics</h3>
      <ForecastTable columns={statsColumns} rows={statsRows} format="gbp" />

      <ComparisonChart data={comparison} />

      <h3>Change in net income from previous forecast</h3>
      <ForecastTable columns={compColumns} rows={compRows} format="gbp" />
    </Section>
  );
}
