"""Utils to read temperatures off of a raspberry pi thermometer."""

import statistics
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


def sample_temperature(*args, samples: int = 10, **kwargs) -> typing.Tuple[float]:
    """Return a tuple of temperature samples from the device.
    
    With the exception of ``samples``, all args and kwargs are passed directly to 
    ``temperature``.

    :param samples: Number of samples to take. Default 10.
    """
    return tuple(temperature(*args, **kwargs) for i in range(samples))


# Literal copy from base lib 3.8. i am the worst
def quantiles(data, n=4):
    """Divide *data* into *n* continuous intervals with equal probability.

    Returns a list of (n - 1) cut points separating the intervals.

    Set *n* to 4 for quartiles (the default).  Set *n* to 10 for deciles.
    Set *n* to 100 for percentiles which gives the 99 cuts points that
    separate *data* in to 100 equal sized groups.

    The *data* can be any iterable containing sample.
    The cut points are linearly interpolated between data points.
    """
    if n < 1:
        raise statistics.StatisticsError("n must be at least 1")

    data = sorted(data)
    ld = len(data)

    if ld < 2:
        raise statistics.StatisticsError("must have at least two data points")

    m = ld + 1
    result = []
    for i in range(1, n):
        j = i * m // n  # rescale i to m/n
        j = 1 if j < 1 else ld - 1 if j > ld - 1 else j  # clamp to 1 .. ld-1
        delta = i * m - j * n  # exact integer math
        interpolated = (data[j - 1] * (n - delta) + data[j] * delta) / n
        result.append(interpolated)
    return result


def temperature_strict(
    retries: int = 20, samples: int = 10, max_iqr: float = 0.5, **kwargs
):
    """Read the temperature off of a device strictly.

    This function is exactly the same as ``temperature`` except that it includes a 
    requirement that readings are consistent. Multiple samples are read from the device
    and the reading is consistent if the interquartile range of the observations is 
    less than or equal to the ``max_iqr`` set. The median of the samples is returned.

    :param retries: Number of times to retry reading on failure. Set to -1 for infinite. 
    Default 20.
    :param samples: Number of samples to take at each attempt. Default 10.
    :param max_iqr: Maximum allowable interquartile range. Default 0.5.
    """
    attempts = 0
    while True:
        readings = sample_temperature(samples=samples, retries=retries, **kwargs)

        qs = quantiles(readings)
        iqr = qs[-1] - qs[0]

        if iqr <= max_iqr:
            return statistics.median(readings)

        # stop looping if out of retries
        if attempts == retries:
            break

        attempts += 1

    raise InconsistentTemperature("Did not obtain two consistent readings.")
