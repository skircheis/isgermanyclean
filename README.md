isgermanyclean.today
==============

A [one-page website](https://isgermanyclean.today) to answer a very simple question:
Did Germany have cleaner electricity than France today?

This code downloads hourly generation data from [ENTSO-E](https://transparency.entsoe.eu/) and calculates the two countries's respective carbon intensities.
The website shows whether Germany was cleaner today (or yesterday, if there is no data for today).
It also shows how many hours so far during the current year Germany has had cleaner electricity than France.
Year-to-date data is also displayed graphically in a scatter plot.

## Operation
Every hour, using a `systemd` timer the program downloads generation data from ENTSO-E.
This data is processed and stored under `$XDG_DATA_HOME`, which by default is `~./local/share/`.
The program then prepares a "report" with the carbon intensities, number of cleaner hours for Germany, etc.
This report is stored as JSON in the same directory.
As part of the report, a scatter plot is also generated and stored.

The results are presented using a simple one-page Flask app, served with `uwsgi`.

Most functionality is accessible through the command line: try `isgermanyclean --help`.

## Contributing
Contribute via Github. Design improvements are appreciated.

## Forking etc
You can deploy this program on your own server.
The `pyproject.toml` and `requirements.txt` should tell you everything about dependencies, except that you will also need a LaTeX installation that `matplotlib` can find, and `uwsgi`.
The program expects to find an API key for ENTSO-E in `$XDG_CONFIG_HOME/isgermanyclean/APIKEY`.
It should be a JSON object with one key, `api_key`.
You will need to install and enable the `systemd` units.
Finally, because the `systemd` timer dowwloads one day's worth of data at most, you will need to manually seed the installation with year-to-date data.
