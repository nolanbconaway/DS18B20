"""Utils to read the temperature off of the thermometer."""

import os
import time
import typing

# defaults for my raspi
DEFAULT_DEVICE_FOLDER = "/sys/bus/w1/devices/"
DEFAULT_DEVICE_SUFFIX = "/w1_slave"
DEFAULT_WAIT_INTERVAL = 0.2


def find_temperature_sensor(
    device_folder: str = DEFAULT_DEVICE_FOLDER,
    device_suffix: str = DEFAULT_DEVICE_SUFFIX,
) -> typing.Union[str, None]:
    """Try to guess the location of the sensor."""
    devices = os.listdir(device_folder)
    devices = [device for device in devices if device.startswith("28-")]
    if devices:
        return device_folder + devices[0] + device_suffix
    return None


def read_device_data(device: str = None) -> int:
    """Read the raw data off the device."""
    # find device if needed
    if device is None:
        device = find_temperature_sensor()
        if not device:
            raise OSError("Cannot find temperature sensor.")

    with open(device, "r") as sensor:
        raw_reading = sensor.readlines()

    return raw_reading


def get_temperature(
    device: str = None, wait_interval: float = DEFAULT_WAIT_INTERVAL
) -> float:
    """Read the temperature in fahrenheit."""
    lines = read_device_data(device)

    # Keep retrying till we get a YES from the thermometer
    # 1. Make sure that the response is not blank
    # 2. Make sure the response has at least 2 lines
    # 3. Make sure the first line has a "YES" at the end
    while not lines and len(lines) < 2 and lines[0].strip()[-3:] != "YES":
        # If we haven't got a valid response, wait for the WAIT_INTERVAL
        # (seconds) and try again.
        time.sleep(wait_interval)
        lines = read_device_data(device)

    # Split out the raw temperature number
    temperature = lines[1].split("t=")[1]

    # Check that the temperature is not invalid
    if temperature != -1:
        temperature_celsius = float(temperature) / 1000.0
        temperature_fahrenheit = (temperature_celsius * 1.8) + 32.0

    return temperature_fahrenheit


def check_accept(
    degrees: float,
    reference: float,
    min_val: float = 40.0,
    max_val: float = 110.0,
    max_delta: float = 1.0,
) -> bool:
    """Run acceptance tests for the temp reading. Used in the strict readiong.

    Temp must be:

    1. Not a huge change from just like a second before
    2. Not very high or very low.

    """
    # its been like 1 second the temp should not have shifted a lot.
    if abs(degrees - reference) > max_delta:
        return False

    # these are extremes that should never be met.
    if degrees < min_val:
        return False
    if degrees > max_val:
        return False

    return True


def get_temperature_strict(
    device: str = None, wait_interval: float = DEFAULT_WAIT_INTERVAL, attempts: int = 30
) -> float:
    """Strict version of get_temperature.

    Requires two consistent readings within a reasonable range of values.
    """
    # get one reading
    temperature_fahrenheit = get_temperature()

    # except if it never passes tests
    for attempt in range(1, attempts + 1):
        reference = get_temperature(device)
        if check_accept(temperature_fahrenheit, reference):
            break
        elif attempt == attempts:
            raise RuntimeError("Unable to obtain consistent valid readings.")
        else:
            temperature_fahrenheit = reference
            time.sleep(wait_interval)

    return temperature_fahrenheit
