"""Chart generation."""

import matplotlib.pyplot as plt
import pandas as pd

from .config import YEAR, OUTPUT_DIR


def generate_hnet_chart(baseline_stats: pd.DataFrame):
    """Generate a bar chart of average hnet by household group."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(
        baseline_stats["group"],
        baseline_stats["mean_hnet"] / 1_000,
    )
    ax.set_xlabel("Average household net income (£k)")
    ax.set_title(f"Average household net income by family type ({YEAR})")
    ax.grid(True, alpha=0.3, axis="x")
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "hnet_by_group.png", dpi=150)
    plt.close(fig)
