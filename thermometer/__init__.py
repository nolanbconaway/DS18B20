"""Utils to read temperatures off of a raspberry pi thermometer."""

import time
import typing
from pathlib import Path

# defaults for my raspi
DEVICE_FOLDER = Path("/sys/bus/w1/devices/")
DEVICE_SUFFIX = "w1_slave"
WAIT_INTERVAL = 0.05


class DeviceNotFoundError(Exception):
    """Raised when the device could not be found."""

    pass


class UnexpectedDeviceData(Exception):
    """Raised when the device data has an unexpected format."""

    pass


class InconsistentTemperature(Exception):
    """Raised when the consecutive reads are very different."""

    pass


def find_device(
    device_folder: Path = DEVICE_FOLDER, device_suffix: str = DEVICE_SUFFIX
) -> Path:
    """Try to guess the location of the sensor."""
    device = next(device_folder.glob("28-*"), None)

    if not device:
        raise DeviceNotFoundError

    return device_folder / device / device_suffix


def temperature_raw(text: str) -> int:
    """Read the raw (int) temperature, provided text from a device."""
    lines = text.strip().split("\n")

    # check for correct number of lines
    if len(lines) != 2:
        raise UnexpectedDeviceData(
            ("Expected 2 lines of text data, got %s:\n\n" % len(lines)) + text
        )

    # check YES signal
    if not lines[0].strip().endswith("YES"):
        raise UnexpectedDeviceData(
            "Did not find YES indicator on first line.\n\n" + text
        )

    try:
        return int(lines[1].split("t=")[1])
    except IndexError:
        raise UnexpectedDeviceData(
            "Unable to find temperature value (t=...) on second line.\n\n" + text
        )


def convert_raw_temp(raw: int, unit: str = "F") -> float:
    """Convert an int raw reading into degrees fahrenheit or celcius."""
    if unit not in ("F", "C"):
        raise ValueError("Unit must be F or C.")

    celsius = float(raw) / 1000.0

    if unit == "C":
        return celsius

    return (celsius * 1.8) + 32.0


def temperature(
    device: Path = None, unit: str = "F", retries: int = 20, **find_device_kw
) -> float:
    """Read the temperature off of a device.

    This is a wrapper around some of the elemental functions in this module, including
    ``find_device``, ``temperature_raw``, and ``convert_raw_temp``.
    
    It also includes handlers for retrying to read the device in the case that the data
    were not formatted as expected.

    :param device: Path to the device. If not provided, ``find_device()`` is used.
    :param unit: Unit of temperature to return, either F or C. Default F.
    :param retries: Number of times to retry reading on failure, with 0.05 second 
    timeout between attempts. Set to -1 for infinite. Default 20.
    :return: Temperature in unit specified by the user.
    """
    attempts = 0
    while True:
        try:
            text = (device or find_device(**find_device_kw)).read_text()
            raw = temperature_raw(text)
            return convert_raw_temp(raw, unit)
        except (DeviceNotFoundError, UnexpectedDeviceData):
            if attempts == retries:
                raise
            time.sleep(WAIT_INTERVAL)

        attempts += 1


def temperature_strict(
    device: Path = None,
    unit: str = "F",
    retries: int = 20,
    max_delta: float = 1,
    **find_device_kw,
):
    """Read the temperature off of a device strictly.

    This function is exactly the same as ``temperature`` except that it includes a 
    requirement that a similar temperature was obtained in consecutive readings.

    :param device: Path to the device. If not provided, ``find_device()`` is used.
    :param unit: Unit of temperature to return, either F or C. Default F.
    :param retries: Number of times to retry reading on failure. Set to -1 for infinite. 
    Default 20.
    :param max_delta: Maximum allowable difference in value between consecutive reads.
    timeout between attempts. Set to -1 for infinite. Default 20.
    :return: Temperature in unit specified by the user.
    """
    # function to read the device and get the temperature.
    def f():
        return temperature(device=device, unit=unit, retries=retries, **find_device_kw)

    attempts = 0
    t1 = f()

    while True:

        # get a new reading and compare. return if consistent
        t2 = f()
        if abs(t2 - t1) <= max_delta:
            return t2

        # stop looping if out of retries
        if attempts == retries:
            break

        # replace first temp with second
        t1 = t2
        attempts += 1

    raise InconsistentTemperature("Did not obtain two consistent readings.")
