from .args import argparser


def main():
    args = argparser.parse_args()
    try:
        if args.start.tz is None:
            args.start = args.start.tz_localize(args.timezone)
        if args.end.tz is None:
            args.end = args.end.tz_localize(args.timezone)
    except AttributeError:
        pass
    args.func(args)
