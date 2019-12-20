"""Print the current temp to the command line.

This is a command line tool, so run it like `python3 -m thermometer.now`.
"""
import argparse
from pathlib import Path

from . import temperature, temperature_strict

# make the parser
parser = argparse.ArgumentParser(description="Print the current temperature.")
parser.add_argument(
    "-u",
    "--unit",
    type=str,
    choices={"C", "F"},
    help="Celsius or Fahrenheit choice. Default Fahrenheit.",
)
parser.add_argument(
    "-d",
    "--device",
    type=Path,
    help="Optional path to the thermometer device."
    + " Will attempt to find it if not provided.",
)
parser.add_argument(
    "-r",
    "--retries",
    type=int,
    help="Number of read attempts (in case data are not as expected). Default 20.",
)
parser.add_argument(
    "--device-folder",
    type=Path,
    help="Optional path to the system bus devices. Used as kwarg to ``find_device``. "
    + "Ignored if device is provided.",
)

parser.add_argument(
    "--device-suffix",
    type=Path,
    help="Optional suffix of slave file found within the device folder. "
    + "Used as kwarg to ``find_device``. Ignored if device is provided.",
)
parser.add_argument(
    "--no-strict", action="store_true", help="Turn off the strict reading handler."
)
parser.add_argument(
    "--max-iqr",
    type=float,
    help="Maximum interquartile range allowable in a strict reading. "
    + "Ignored if --no-strict.",
)
parser.add_argument(
    "--samples",
    type=int,
    default=10,
    help="Number of samples to take for strict reading. Ignored if --no-strict.",
)


def main():
    """Print the temperature to the console."""
    args = parser.parse_args()
    kwargs = {
        k: v
        for k, v in vars(args).items()
        if v is not None and k not in ("no_strict", "max_iqr", "samples")
    }

    # add max delta if strict and specified.
    if not args.no_strict:
        if args.max_iqr is not None:
            kwargs["max_iqr"] = args.max_iqr
        if args.samples is not None:
            kwargs["samples"] = args.samples

    f = temperature if args.no_strict else temperature_strict

    temp = f(**kwargs)

    print(temp)


if __name__ == "__main__":
    main()
