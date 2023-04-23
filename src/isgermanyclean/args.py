from argparse import ArgumentParser, Action, BooleanOptionalAction
from pandas import Timestamp, Timedelta

from .compare import show_comparison
from .download import download
from .intensity import show_intensity
from .plot import plot
from .report import report
from .web import launch_server

from .utils import today

argparser = ArgumentParser(prog="isgermanyclean")
subparsers = argparser.add_subparsers(title="Tasks", required=True)


download_parser = subparsers.add_parser(
    "download",
    help="Download and store data",
    description="""
    Download generation data with a country-code and a date range
    """,
)
download_parser.set_defaults(func=download)

intensity_parser = subparsers.add_parser(
    "intensity",
    help="Display intensity for a country",
)
intensity_parser.set_defaults(func=show_intensity)

for subparser in [download_parser, intensity_parser]:
    subparser.add_argument(
        "country", metavar="CC", type=str, help="Two-letter country code, e.g. DE, FR"
    )

plot_parser = subparsers.add_parser(
    "plot",
    help="Make a scatter plot comparing two countries",
)
plot_parser.set_defaults(func=plot)
plot_parser.add_argument(
    "countryX",
    metavar="CC",
    type=str,
    help="Country to put on the X axis (two-letter country code, e.g. DE, FR)",
)
plot_parser.add_argument(
    "countryY",
    metavar="CC",
    type=str,
    help="Country to put on the Y axis (two-letter country code, e.g. DE, FR)",
)
plot_parser.add_argument(
    "output",
    nargs="?",
    type=str,
    help="Output filename. If omitted, display the plot on the screen.",
)

compare_parser = subparsers.add_parser(
    "compare",
    help="Display intensity for a country",
)
compare_parser.set_defaults(func=show_comparison)
compare_parser.add_argument(
    "countryX",
    metavar="CC",
    type=str,
    help="Country #1 to compare",
)
compare_parser.add_argument(
    "countryY",
    metavar="CC",
    type=str,
    help="Country #2 to compare",
)

hourago = (Timestamp.today() - Timedelta(hours=1)).floor("1H")
dayago = (Timestamp.today() - Timedelta(hours=24)).floor("1H")
ytd = Timestamp(str(Timestamp.today().year))

for subparser in [download_parser, intensity_parser, plot_parser, compare_parser]:
    time_opts = subparser.add_argument_group(
        "Time", description="Options to control the time range of data collected."
    )
    time_opts.add_argument(
        "--start",
        help="Start timestamp. Default: %s"
        % (
            "start of the current year"
            if subparser in [plot_parser, compare_parser]
            else "24 hours ago"
        ),
        default=ytd if subparser in [plot_parser, compare_parser] else dayago,
        type=Timestamp,
    )
    time_opts.add_argument(
        "--end",
        help="End timestamp. Default: 1 hour ago",
        default=hourago,
        type=Timestamp,
    )
    time_opts.add_argument(
        "--timezone",
        "--tz",
        help="Timezone for the start and end timestamps",
        default="Europe/Brussels",
    )

web_parser = subparsers.add_parser(
    "web",
    help="Start a development server",
    description="""Start web interface. Intended only for development. For
    production, use the provided systemd service.""",
)
web_parser.set_defaults(func=launch_server)
web_parser.add_argument("--port", help="Port to bind to. Default: 5000", type=int)
web_parser.add_argument("--host", help="Host to bind to. Default: localhost", type=str)
web_parser.add_argument(
    "--debug",
    action="store_true",
    help="""
    Enable Flask's debug mode. Major security risk, never use in production!
    """,
)

report_parser = subparsers.add_parser(
    "report",
    help="Generate a report comparing two countries",
)
report_parser.set_defaults(func=report)
report_parser.add_argument(
    "countryX",
    metavar="CC",
    type=str,
    help="Country #1 to report on",
)
report_parser.add_argument(
    "countryY",
    metavar="CC",
    type=str,
    help="Country #2 to report on",
)
report_parser.add_argument(
    "--datadir",
    action=BooleanOptionalAction,
    help="Save files to data directory instead of the working directory.",
)
report_parser.add_argument(
    "--plot",
    action=BooleanOptionalAction,
    help="Generate a plot",
    default=True,
)
report_parser.add_argument(
    "--output",
    type=str,
    help="Output filename for the report. If not present, print to stdout",
)
report_parser.add_argument(
    "--plot-output",
    type=str,
    help="Output filename for the plot. If not present, display the plot on the screen.",
)
