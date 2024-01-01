import matplotlib.pyplot as plt
from pandas import Timestamp

from .intensity import get_merged_intensities, column_names


def plot(opts):
    ccs = [opts.countryX, opts.countryY]
    intensities = get_merged_intensities(ccs, opts.start, opts.end)
    title = opts.title.format(**vars(opts))
    plot_from_intensities(intensities, ccs, title)
    if opts.output is None:
        plt.show()
    else:
        fig = plt.gcf()
        fig.savefig(opts.output, dpi=300, bbox_inches="tight")


def plot_from_intensities(intensities, ccs, title):
    max_intensity = max(intensities.max())

    # Adjusting the plot
    plt.rcParams.update({"text.usetex": True, "font.family": "Computer Modern"})
    ax = plt.gca()
    plot_range_padding = 0.05
    ax.set_ylim(0, max_intensity * (1 + plot_range_padding))
    ax.set_xlim(0, max_intensity * (1 + plot_range_padding))

    # Plotting
    cname = column_names["co2_int"]
    plt.scatter(
        intensities[cname + " " + ccs[0]],
        intensities[cname + " " + ccs[1]],
        s=6,
        c="#5e81b5",
    )
    linps = [0, max_intensity * (1 + plot_range_padding)]
    plt.plot(
        linps,
        linps,
        "k",
    )

    def scaled(xy):
        return (xy[0] * max_intensity, xy[1] * max_intensity)

    # Labels, captions, annotations
    ax.set_title(title)
    plt.xlabel(f"Carbon intensity {ccs[0]} [gCO2eq/kWh]")
    plt.ylabel(f"Carbon intensity {ccs[1]} [gCO2eq/kWh]")
    ann_xy = scaled((0.75, 0.35))
    ann_yx = (ann_xy[1], ann_xy[0])
    ax.annotate(f"{ccs[0]} more carbon intensive", xy=ann_xy, ha="center")
    ax.annotate(f"{ccs[1]} more carbon intensive", xy=ann_yx, ha="center")
    now = Timestamp.today().floor("1s")
    plt.figtext(
        0.13,
        -0.05,
        "Data: ENTSO-E\nCarbon intensities: IPCC 2014\nGenerated: " + str(now),
        ha="left",
        va="bottom",
    )
    plt.figtext(
        0.83, -0.05, "\\texttt{https://isgermanyclean.today}", ha="right", va="bottom"
    )

    ax.set_aspect(1)
    plt.tight_layout()
