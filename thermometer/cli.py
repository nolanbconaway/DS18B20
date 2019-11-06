"""Print the current temp to the command line.

This is a command line tool, so run it like `python3 -m thermometer.now`.
"""
import argparse
from pathlib import Path

import thermometer

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
    "--nostrict", action="store_true", help="Turn off the stict reading handler."
)


def main():
    """Print the temperature to the console."""
    args = parser.parse_args()
    kwargs = {k: v for k, v in vars(args).items() if v is not None}

    f = thermometer.temperature if args.nostrict else thermometer.temperature_strict
    temp = f(**kwargs)
    print(temp)


if __name__ == "__main__":
    main()
