# UK Spring Statement 2026 Analysis

PolicyEngine analysis of the Spring Statement 2026, focusing on changes to the OBR economic forecast and their impact on household net income. Includes a React dashboard for interactive visualisation.

## Setup

```bash
pip install -e .
cd dashboard && npm install
```

## Usage

1. Update the OBR forecast values in `uk_spring_statement_analysis/config.py` (`UPDATED_EARNINGS_GROWTH`, `UPDATED_CPI_INFLATION`)
2. Run `python -m uk_spring_statement_analysis` to generate JSON data and update the blog markdown
3. Start the dashboard: `cd dashboard && npm run dev`
4. Open http://localhost:5173

## Project structure

- `uk_spring_statement_analysis/` — Python package (microsimulation, data export)
- `dashboard/` — Vite + React dashboard
- `dashboard/public/data/` — JSON data files (written by Python, read by React)
- `spring-statement-2026-blog.md` — Markdown blog post (legacy)
