from json import dump, dumps, load
import matplotlib.pyplot as plt
from pandas import Timestamp, Timedelta
from pathlib import Path

from .compare import cleaner_hours, averages
from .intensity import get_intensity, get_merged_intensities, column_names_raw
from .plot import plot_from_intensities
from .utils import get_data_dir


def load_report(fname):
    fname = get_data_dir() / fname
    with open(fname, "r") as f:
        report = load(f)
    return report


def make_report(opts):
    report = {}
    ccs = [opts.countryX, opts.countryY]
    end = Timestamp.today().tz_localize("Europe/Brussels")
    start = end.floor("1D")
    while "co2_int" not in report.keys():
        intensities = {cc: get_intensity(cc, start, end) for cc in ccs}
        if any(len(i) == 0 for i in intensities.values()):
            # No data from today, try one day before
            start -= Timedelta("1D")
        else:
            report["co2_int"] = averages(intensities)
            report["date"] = str(start)
            # For serialisation as JSON
    ytd = Timestamp(str(end.year)).tz_localize("Europe/Brussels")
    intensities = {cc: get_intensity(cc, ytd, end) for cc in ccs}
    report["cleaner_hours"] = cleaner_hours(intensities)
    cname = column_names_raw["co2_int"]
    report["extrema"] = {
        cc: (i[cname].min(), i[cname].max()) for cc, i in intensities.items()
    }

    intensities = get_merged_intensities(ccs, ytd, end)
    report["hours"] = len(intensities)
    if not opts.plot:
        return report

    vs = vars(opts)
    vs["start"] = start
    vs["end"] = end
    title = opts.plot_title.format(**vs)
    plot_from_intensities(intensities, ccs, title)

    if opts.plot_output is None:
        plt.show()
    else:
        fig = plt.gcf()
        w = fig.get_figwidth()  # Width in inches
        pxs = [2400, 1600, 1200, 800, 600, 400, 300]  # Desired widths in pixels
        out_path = Path(opts.plot_output)
        stem = out_path.stem
        report["plots"] = {}
        for p in pxs:
            out = out_path.with_stem(f"{stem}-{p}")
            fig.savefig(out, dpi=p / w * 100 / 72 * 32 / 33, bbox_inches="tight")
            report["plots"][p] = out.name
        bbox = fig.get_tightbbox()
        dims = bbox.max - bbox.min
        report["plot_ar"] = round(dims[0] / dims[1] * 100) / 100

    return report


def report(opts):
    data_dir = get_data_dir()
    if opts.datadir:
        if opts.output is not None:
            opts.output = data_dir / opts.output
        if opts.plot_output is not None:
            opts.plot_output = data_dir / opts.plot_output
    report = make_report(opts)
    if opts.output is None:
        print(dumps(report))
    else:
        with open(opts.output, "w") as f:
            dump(report, f)
