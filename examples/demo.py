"""Generate a sample dataset, summarize it with `communication`, and render visuals.

Running this script (from the repo root) will:

1. Create a reproducible sample dataset at ``examples/sample_sales.csv``.
2. Print a summary of it using the ``communication`` package.
3. Render four descriptive charts into ``examples/figures/``.

    python examples/demo.py
"""

from __future__ import annotations

import os

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")  # headless / no display
import matplotlib.pyplot as plt

import communication as comm

HERE = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(HERE, "figures")
CSV_PATH = os.path.join(HERE, "sample_sales.csv")

# --- Design tokens (validated light-mode palette from the dataviz method) -----
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_MUTED = "#52514e"
GRID = "#e4e3df"
SERIES = ["#2a78d6", "#eb6834", "#1baf7a"]  # blue, orange, aqua


def make_dataset(n: int = 240) -> pd.DataFrame:
    """Build a small, realistic sales dataset with a few missing values."""
    rng = np.random.default_rng(42)
    regions = ["North", "South", "East", "West"]
    products = ["Espresso", "Latte", "Cold Brew"]

    region = rng.choice(regions, size=n)
    product = rng.choice(products, size=n)
    units = rng.integers(5, 120, size=n)
    # Revenue loosely tracks units, with per-product price and noise.
    price = pd.Series(product).map(
        {"Espresso": 3.0, "Latte": 4.5, "Cold Brew": 5.0}
    ).to_numpy()
    revenue = np.round(units * price + rng.normal(0, 15, size=n), 2)
    rating = np.round(rng.normal(4.1, 0.6, size=n), 1).clip(1, 5)
    returns = rng.integers(0, 8, size=n).astype(float)

    df = pd.DataFrame(
        {
            "region": region,
            "product": product,
            "units_sold": units,
            "revenue": revenue,
            "customer_rating": rating,
            "returns": returns,
        }
    )

    # Sprinkle in missing values so the data-quality view has something to show.
    df.loc[rng.choice(n, size=28, replace=False), "customer_rating"] = np.nan
    df.loc[rng.choice(n, size=12, replace=False), "returns"] = np.nan
    return df


def _style_axes(ax) -> None:
    """Apply recessive, minimal chart chrome."""
    ax.set_facecolor(SURFACE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.tick_params(colors=INK_MUTED, length=0)
    ax.yaxis.label.set_color(INK_MUTED)
    ax.xaxis.label.set_color(INK_MUTED)
    ax.title.set_color(INK)
    ax.grid(axis="y", color=GRID, linewidth=1, zorder=0)
    ax.set_axisbelow(True)


def _new_fig():
    fig, ax = plt.subplots(figsize=(7.5, 4.6), dpi=140)
    fig.patch.set_facecolor(SURFACE)
    _style_axes(ax)
    return fig, ax


def _save(fig, name: str) -> None:
    path = os.path.join(FIG_DIR, name)
    fig.tight_layout()
    fig.savefig(path, facecolor=SURFACE, bbox_inches="tight")
    plt.close(fig)
    print(f"  wrote {os.path.relpath(path)}")


def chart_revenue_by_region(df: pd.DataFrame) -> None:
    totals = df.groupby("region")["revenue"].sum().sort_values(ascending=False)
    fig, ax = _new_fig()
    bars = ax.bar(totals.index, totals.values, color=SERIES[0], width=0.62, zorder=3)
    ax.set_title("Total revenue by region", fontsize=14, fontweight="bold", loc="left")
    ax.set_ylabel("Revenue ($)")
    for b, v in zip(bars, totals.values):
        ax.text(b.get_x() + b.get_width() / 2, v, f"${v:,.0f}",
                ha="center", va="bottom", fontsize=9, color=INK)
    _save(fig, "revenue_by_region.png")


def chart_units_distribution(df: pd.DataFrame) -> None:
    fig, ax = _new_fig()
    ax.hist(df["units_sold"], bins=18, color=SERIES[0], zorder=3, rwidth=0.92)
    ax.set_title("Distribution of units sold", fontsize=14, fontweight="bold", loc="left")
    ax.set_xlabel("Units sold per order")
    ax.set_ylabel("Number of orders")
    _save(fig, "units_distribution.png")


def chart_revenue_by_region_and_product(df: pd.DataFrame) -> None:
    pivot = df.pivot_table(index="region", columns="product",
                           values="revenue", aggfunc="sum")
    products = list(pivot.columns)
    x = np.arange(len(pivot.index))
    width = 0.8 / len(products)
    fig, ax = _new_fig()
    for i, product in enumerate(products):
        ax.bar(x + i * width, pivot[product].values, width * 0.9,
               label=product, color=SERIES[i % len(SERIES)], zorder=3)
    ax.set_xticks(x + width * (len(products) - 1) / 2)
    ax.set_xticklabels(pivot.index)
    ax.set_title("Revenue by region and product", fontsize=14, fontweight="bold", loc="left")
    ax.set_ylabel("Revenue ($)")
    leg = ax.legend(frameon=False, title="Product", loc="upper right")
    leg.get_title().set_color(INK_MUTED)
    for text in leg.get_texts():
        text.set_color(INK_MUTED)
    _save(fig, "revenue_by_region_and_product.png")


def chart_missing(df: pd.DataFrame) -> None:
    """Data-quality view driven directly by communication.missing()."""
    miss = comm.missing(df)
    miss = miss[miss["count"] > 0].sort_values("percent")
    fig, ax = _new_fig()
    ax.grid(axis="y", linewidth=0)
    ax.grid(axis="x", color=GRID, linewidth=1, zorder=0)
    bars = ax.barh(miss.index, miss["percent"], color=SERIES[0], height=0.55, zorder=3)
    ax.set_title("Missing values by column", fontsize=14, fontweight="bold", loc="left")
    ax.set_xlabel("% missing")
    for b, v in zip(bars, miss["percent"]):
        ax.text(v, b.get_y() + b.get_height() / 2, f" {v:.1f}%",
                ha="left", va="center", fontsize=9, color=INK)
    ax.set_xlim(0, max(miss["percent"].max() * 1.2, 1))
    _save(fig, "missing_values.png")


def main() -> None:
    os.makedirs(FIG_DIR, exist_ok=True)
    df = make_dataset()
    df.to_csv(CSV_PATH, index=False)
    print(f"Saved dataset: {os.path.relpath(CSV_PATH)}  ({len(df)} rows)\n")

    print("Numeric columns:", comm.numeric_columns(df))
    print("Categorical columns:", comm.categorical_columns(df))
    print("\nSummary (communication.summarize):")
    with pd.option_context("display.width", 120, "display.max_columns", None):
        print(comm.summarize(df).round(2))

    print("\nRendering figures:")
    chart_revenue_by_region(df)
    chart_units_distribution(df)
    chart_revenue_by_region_and_product(df)
    chart_missing(df)
    print("\nDone.")


if __name__ == "__main__":
    main()
