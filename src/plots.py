import matplotlib.pyplot as plt

BLUE = "#2a78d6"
INK = "#0b0b0b"
MUTED = "#52514e"
GRID = "#e4e3df"


def apply_style():
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.edgecolor": GRID,
            "axes.labelcolor": MUTED,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "text.color": INK,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "axes.grid.axis": "y",
            "grid.color": GRID,
            "grid.linewidth": 0.8,
            "axes.axisbelow": True,
            "font.size": 10,
            "axes.titlesize": 11,
            "axes.titleweight": "bold",
            "axes.titlelocation": "left",
            "figure.dpi": 110,
        }
    )


def default_rate_chart(summary, title, xlabel, overall_rate, rotate=0):
    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    positions = list(range(len(summary)))
    rates = summary["rate"] * 100
    errors = [
        (summary["rate"] - summary["low"]) * 100,
        (summary["high"] - summary["rate"]) * 100,
    ]
    ax.bar(
        positions,
        rates,
        yerr=errors,
        width=0.6,
        color=BLUE,
        error_kw={"ecolor": MUTED, "elinewidth": 1, "capsize": 3},
    )
    ax.axhline(overall_rate * 100, color=MUTED, linestyle="--", linewidth=1)
    ax.annotate(
        f"overall\n{overall_rate:.2%}",
        xy=(1.0, overall_rate * 100),
        xycoords=("axes fraction", "data"),
        xytext=(6, 0),
        textcoords="offset points",
        va="center",
        color=MUTED,
        fontsize=9,
        annotation_clip=False,
    )
    for position, rate, high in zip(positions, rates, summary["high"] * 100):
        ax.text(
            position,
            high + 0.25,
            f"{rate:.1f}%",
            ha="center",
            va="bottom",
            fontsize=9,
            bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.5},
            zorder=5,
        )
    ax.set_xticks(positions)
    ax.set_xticklabels(summary["label"], rotation=rotate, ha="right" if rotate else "center")
    ax.set_ylabel("Default rate (%)")
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    ax.set_ylim(0, summary["high"].max() * 100 * 1.15)
    fig.tight_layout()
    return fig
