from .intensity import (
    column_names,
    column_names_raw,
    get_intensity,
    get_merged_intensities,
)
from .utils import merge_data


def show_comparison(opts):
    ccs = [opts.countryX, opts.countryY]
    intensities = {cc: get_intensity(cc, opts.start, opts.end) for cc in ccs}
    cleaner = cleaner_hours(intensities)
    avgs = averages(intensities)
    nhrs = min([len(i) for i in intensities.values()])
    print(f"Between {opts.start} and {opts.end},")
    print(f"{ccs[0]} was cleaner than {ccs[1]} for {cleaner} out of {nhrs} hours.")
    print("The average carbon intensity was")
    print("\n".join([f"{k}: {v:3.0f} gCO2eq/kWh" for k, v in avgs.items()]))
    vs = list(avgs.values())
    print(
        f"The average emissions of {ccs[0]} were {vs[0]/vs[1]:.2f} times those of {ccs[1]}"
    )


def cleaner_hours(intensities):
    ccs = intensities.keys()
    merged = merge_data(intensities)
    cols = [column_names_raw["co2_int"] + " " + cc for cc in ccs]
    return len(merged.query(f"`{cols[0]}` < `{cols[1]}`"))


def averages(intensities):
    cols = [column_names_raw["co2_tot"], column_names_raw["gen_tot"]]
    sums = {k: i[cols].sum() for k, i in intensities.items()}
    return {k: i[cols[0]] / i[cols[1]] for k, i in sums.items()}
