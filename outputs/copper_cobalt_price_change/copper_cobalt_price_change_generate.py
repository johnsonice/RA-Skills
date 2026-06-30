from pathlib import Path
import os
import re

import pandas as pd

OUTPUT_DIR = Path(__file__).resolve().parent
os.environ.setdefault("MPLCONFIGDIR", str(OUTPUT_DIR / ".matplotlib-cache"))
os.environ.setdefault("XDG_CACHE_HOME", str(OUTPUT_DIR / ".cache"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager


# Chart metadata
INPUT_XLSX = Path("/Users/bellahao/Desktop/copper and cobalt prices .xlsx")
SHEET_NAME = "M"
PNG_PATH = OUTPUT_DIR / "copper_cobalt_price_change_index.png"
CHART_READY_CSV = OUTPUT_DIR / "copper_cobalt_price_change_chart_ready.csv"

CHART_TYPE = "Multi-line chart"
TITLE = "Copper and Cobalt Price Change"
SUBTITLE = "Monthly commodity price index, January 2015 = 100"
Y_AXIS_LABEL = "Index, Jan. 2015 = 100"
SOURCE = "Source: IMF Primary Commodity Price System (PCPS); user-provided workbook."
CAVEAT = (
    "Note: Raw prices use different units, so both series are indexed to their "
    "January 2015 values for comparison."
)

FUND_BLUE = "#004C97"
PANTONE_130 = "#F2A900"
PANTONE_424 = "#707372"
BORDER = "#B3B3B3"
BACKGROUND = "#F3F4F5"
BLACK = "#231F20"


def choose_chart_font():
    try:
        font_manager.findfont("Segoe UI", fallback_to_default=False)
        return "Segoe UI"
    except ValueError:
        return "Arial"


def parse_month(label):
    match = re.fullmatch(r"(\d{4})M(\d{1,2})", str(label))
    if not match:
        return None
    year, month = match.groups()
    return pd.Timestamp(int(year), int(month), 1)


def load_and_clean(path):
    raw = pd.read_excel(path, sheet_name=SHEET_NAME)
    required = {
        "DATASET",
        "SERIES_CODE",
        "COUNTRY",
        "INDICATOR",
        "DATA_TRANSFORMATION",
        "FREQUENCY",
    }
    missing = required.difference(raw.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    month_cols = [col for col in raw.columns if parse_month(col) is not None]
    if not month_cols:
        raise ValueError("No monthly columns like 2015M1 were found.")

    long = raw.melt(
        id_vars=list(required),
        value_vars=month_cols,
        var_name="period",
        value_name="price",
    )
    long["date"] = long["period"].map(parse_month)
    long["price"] = pd.to_numeric(long["price"], errors="coerce")
    long["commodity"] = long["INDICATOR"].str.extract(r"^([^,]+)", expand=False)
    long["commodity"] = long["commodity"].str.strip()
    long = long.dropna(subset=["date", "price", "commodity"]).copy()

    duplicate_count = long.duplicated(["date", "commodity"]).sum()
    if duplicate_count:
        raise ValueError(f"Found {duplicate_count} duplicate date/commodity rows.")

    base_date = long["date"].min()
    base = long.loc[long["date"].eq(base_date), ["commodity", "price"]].set_index("commodity")
    if base["price"].isna().any() or (base["price"] == 0).any():
        raise ValueError("Base-period prices are missing or zero.")

    long["base_price"] = long["commodity"].map(base["price"])
    long["price_index"] = long["price"] / long["base_price"] * 100
    long = long.sort_values(["commodity", "date"])

    chart_ready = long[
        [
            "date",
            "period",
            "commodity",
            "price",
            "price_index",
            "SERIES_CODE",
            "INDICATOR",
            "DATA_TRANSFORMATION",
            "FREQUENCY",
        ]
    ].copy()

    checks = {
        "rows": len(chart_ready),
        "commodities": sorted(chart_ready["commodity"].unique()),
        "start": chart_ready["date"].min().strftime("%Y-%m"),
        "end": chart_ready["date"].max().strftime("%Y-%m"),
        "missing_price": int(chart_ready["price"].isna().sum()),
        "missing_index": int(chart_ready["price_index"].isna().sum()),
        "duplicate_date_commodity": int(chart_ready.duplicated(["date", "commodity"]).sum()),
    }
    return raw, chart_ready, checks


def plot_chart(chart_ready, checks):
    chart_font = choose_chart_font()
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = [chart_font, "Arial", "Helvetica", "DejaVu Sans"]

    fig, ax = plt.subplots(figsize=(13.333, 7.5), dpi=150)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    color_map = {
        "Copper": FUND_BLUE,
        "Cobalt": PANTONE_130,
    }
    for commodity, group in chart_ready.groupby("commodity"):
        ax.plot(
            group["date"],
            group["price_index"],
            label=commodity,
            color=color_map.get(commodity, PANTONE_424),
            linewidth=2.8,
        )

    ax.axhline(100, color=BORDER, linewidth=1.0, linestyle="--", zorder=0)
    ax.set_ylabel(Y_AXIS_LABEL, fontsize=10, color=BLACK)
    ax.set_xlabel("")
    ax.grid(axis="y", color="#E0E0E0", linewidth=0.8)
    ax.grid(axis="x", visible=False)
    ax.tick_params(axis="both", labelsize=9, colors=BLACK, direction="in")

    for spine in ax.spines.values():
        spine.set_color(BORDER)
        spine.set_linewidth(0.9)

    legend = ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.11),
        ncol=2,
        frameon=False,
        fontsize=10,
    )
    for text in legend.get_texts():
        text.set_color(BLACK)

    fig.suptitle(TITLE, x=0.5, y=0.955, fontsize=24, fontweight="bold", color=FUND_BLUE)
    fig.text(0.5, 0.885, SUBTITLE, ha="center", fontsize=18, color=FUND_BLUE)
    fig.text(0.08, 0.045, SOURCE, ha="left", fontsize=9, color=PANTONE_424)
    fig.text(0.08, 0.022, CAVEAT, ha="left", fontsize=9, color=PANTONE_424)
    fig.subplots_adjust(left=0.08, right=0.96, top=0.82, bottom=0.18)

    fig.savefig(PNG_PATH, dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)

    if not PNG_PATH.exists() or PNG_PATH.stat().st_size == 0:
        raise RuntimeError("PNG output was not created or is empty.")

    return {
        **checks,
        "png_path": str(PNG_PATH),
        "png_bytes": PNG_PATH.stat().st_size,
    }


def main():
    if not INPUT_XLSX.exists():
        raise FileNotFoundError(INPUT_XLSX)

    _, chart_ready, checks = load_and_clean(INPUT_XLSX)
    if chart_ready.empty:
        raise ValueError("Chart-ready data is empty.")
    if sorted(chart_ready["commodity"].unique()) != ["Cobalt", "Copper"]:
        raise ValueError(f"Unexpected commodities: {sorted(chart_ready['commodity'].unique())}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    chart_ready.to_csv(CHART_READY_CSV, index=False)
    qa = plot_chart(chart_ready, checks)

    print("QA checks")
    for key, value in qa.items():
        print(f"{key}: {value}")
    print(f"chart_ready_csv: {CHART_READY_CSV}")


if __name__ == "__main__":
    main()
