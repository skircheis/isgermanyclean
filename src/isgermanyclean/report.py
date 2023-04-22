from json import dump, dumps, load
import matplotlib.pyplot as plt
from pandas import Timestamp, Timedelta
from pathlib import Path

from .compare import cleaner_hours, averages
from .intensity import get_intensity, get_merged_intensities
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

    intensities = get_merged_intensities(ccs, ytd, end)
    report["hours"] = len(intensities)
    if not opts.plot:
        return report
    plot_from_intensities(intensities, ccs)
    if opts.plot_output is None:
        plt.show()
    else:
        fig = plt.gcf()
        fig.savefig(opts.plot_output, dpi=300, bbox_inches="tight")
        report["plot_fname"] = Path(opts.plot_output).name

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

