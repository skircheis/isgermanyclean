from pandas import Series, Index, DataFrame, concat

from .utils import get_data, merge_data

# IPCC 2014 numbers
co2intensity_dict = {
    "Mixed": 600,
    "Generation": 600,
    "Load": 600,
    "Biomass": 230,
    "Fossil Brown coal/Lignite": 1200,
    "Fossil Coal-derived gas": 820,
    "Fossil Gas": 490,
    "Fossil Hard coal": 820,
    "Fossil Oil": 490,
    "Fossil Oil shale": 490,
    "Fossil Peat": 820,
    "Geothermal": 38,
    "Hydro Pumped Storage": 24,
    "Hydro Run-of-river and poundage": 24,
    "Hydro Water Reservoir": 24,
    "Marine": 24,
    "Nuclear": 12,
    "Other renewable": 30,
    "Solar": 48,
    "Waste": 230,
    "Wind Offshore": 12,
    "Wind Onshore": 11,
    "Other": 600,
}

co2intensity = Series({k: x for (k, x) in co2intensity_dict.items()})

column_names_raw = {
    "gen_tot": "Total generation [MWh]",
    "co2_tot": "Total emissions [kgCO2eq]",
    "co2_int": "Carbon intensity [gCO2eq/kWh]",
}

column_names = {k: Index([v]) for (k, v) in column_names_raw.items()}


def calculate_intensity(generation):
    gen_tot = DataFrame(generation.sum(axis=1))
    co2_tot = DataFrame(generation @ co2intensity[generation.columns])
    co2_int = DataFrame(co2_tot.div(gen_tot, axis="index"))
    gen_tot.columns = column_names["gen_tot"]
    co2_tot.columns = column_names["co2_tot"]
    co2_int.columns = column_names["co2_int"]
    return concat([generation, gen_tot, co2_tot, co2_int], axis=1)


def get_intensity(country, start, end):
    generation = get_data(country, start, end)
    return calculate_intensity(generation)


def get_merged_intensities(ccs, start, end):
    cname = column_names["co2_int"]
    return merge_data({cc: get_intensity(cc, start, end)[cname] for cc in ccs})


def show_intensity(opts):
    intensity = get_intensity(opts.country, opts.start, opts.end)
    print(intensity[column_names["co2_int"]])
