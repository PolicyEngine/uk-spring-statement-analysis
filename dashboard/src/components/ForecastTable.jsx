function formatChange(value) {
  if (value == null) return "—";
  const sign = value > 0 ? "+" : "";
  const cls =
    value > 0
      ? "change-positive"
      : value < 0
        ? "change-negative"
        : "change-zero";
  return (
    <span className={cls}>
      {sign}
      {value.toFixed(1)}pp
    </span>
  );
}

function formatPct(value) {
  if (value == null) return "—";
  return `${value.toFixed(1)}%`;
}

function formatGbp(value) {
  if (value == null) return "—";
  return `£${value.toLocaleString("en-GB", { maximumFractionDigits: 0 })}`;
}

function formatGbpChange(value) {
  if (value == null) return "—";
  const sign = value > 0 ? "+" : "";
  const cls =
    value > 0
      ? "change-positive"
      : value < 0
        ? "change-negative"
        : "change-zero";
  return (
    <span className={cls}>
      {sign}£
      {Math.abs(value).toLocaleString("en-GB", { maximumFractionDigits: 0 })}
    </span>
  );
}

export default function ForecastTable({ columns, rows, format = "pct" }) {
  const fmt = format === "gbp" ? formatGbp : formatPct;
  const fmtChange = format === "gbp" ? formatGbpChange : formatChange;

  return (
    <div className="forecast-table-wrapper">
      <table className="forecast-table">
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={col}>{col}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, i) => (
            <tr key={i}>
              {row.map((cell, j) => (
                <td key={j}>
                  {j === 0
                    ? cell
                    : j === columns.length - 1
                      ? fmtChange(cell)
                      : fmt(cell)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
