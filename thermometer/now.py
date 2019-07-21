"""Print the current temp to the command line.

This is a command line tool, so run it like `python3 -m thermometer.now`.
"""

from .reader import get_temperature_strict


def main():
    """Now main function."""
    print(round(get_temperature_strict(), 5))


if __name__ == "__main__":
    main()
