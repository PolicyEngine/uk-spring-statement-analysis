# UK Spring Statement 2026 blog post

Generates a PolicyEngine blog post analysing the Spring Statement 2026, focusing on changes to the OBR economic forecast and their impact on household net income.

## Setup

```bash
pip install policyengine-uk matplotlib pandas numpy
```

## Usage

1. Update the OBR forecast values in `generate_blog_data.py` (`UPDATED_EARNINGS_GROWTH`, `UPDATED_CPI_INFLATION`)
2. Run `python generate_blog_data.py`
3. Charts saved to `output/`, blog post updated in `spring-statement-2026-blog.md`
