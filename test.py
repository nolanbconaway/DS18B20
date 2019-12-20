"""Test the module."""
import argparse
import statistics
from pathlib import Path

import pytest

import thermometer
from thermometer import cli


@pytest.mark.parametrize(
    "folder, device, suffix, expected",
    [(Path("folder"), Path("device"), "suffix", Path("folder/device/suffix"))],
)
def test_find_device_when_exists(monkeypatch, folder, device, suffix, expected):
    """Test that the sensor is correctly found."""
    monkeypatch.setattr(Path, "glob", lambda *x: (i for i in [device]))
    device_path = thermometer.find_device(folder, suffix)
    assert device_path == expected


def test_find_device_when_not_exists(monkeypatch):
    """Test that the sensor is correctly found."""
    monkeypatch.setattr(Path, "glob", lambda *x: (i for i in []))
    with pytest.raises(thermometer.DeviceNotFoundError):
        thermometer.find_device(Path("folder"), "suffix")


def test_temperature_raw_valid_data():
    """Test that the expected data are returnd when valid data is passed in."""
    data = "58 01 4b 46 7f ff 08 10 f9 : crc=f9 YES\n58 01 4b 46 7f ff 08 10 f9 t=21500"
    assert thermometer.temperature_raw(data) == 21500


def test_temperature_raw_empty_data():
    """Test that an exception is raised if data are empty."""
    with pytest.raises(thermometer.UnexpectedDeviceData):
        thermometer.temperature_raw("") == 21500


def test_temperature_raw_no_yes():
    """Test that an exception is raised if data do not include a YES flag."""
    data = (
        "58 01 4b 46 7f ff 08 10 f9 : crc=f9 YES NOT"
        + "\n58 01 4b 46 7f ff 08 10 f9 t=21500"
    )
    with pytest.raises(thermometer.UnexpectedDeviceData):
        thermometer.temperature_raw(data)


def test_temperature_raw_no_temp():
    """Test that an exception is raised if data do not include a temp."""
    data = "58 01 4b 46 7f ff 08 10 f9 : crc=f9 YES\n58 01 4b 46 7f ff 08 10 f9 "
    with pytest.raises(thermometer.UnexpectedDeviceData):
        thermometer.temperature_raw(data)


def test_convert_raw_temp():
    """Test the temp converter. This is simple so putting it all in one test."""
    assert thermometer.convert_raw_temp(0, "C") == 0
    assert thermometer.convert_raw_temp(0, "F") == 32
    with pytest.raises(ValueError):
        thermometer.convert_raw_temp(0, "INVALID")


def test_temperature_valid_data(monkeypatch):
    """Test that the correct temperature is returned with valid data."""
    data = "58 01 4b 46 7f ff 08 10 f9 : crc=f9 YES\n58 01 4b 46 7f ff 08 10 f9 t=0"
    monkeypatch.setattr(Path, "read_text", lambda *x: data)
    assert thermometer.temperature(Path("device"), unit="C") == 0


def test_temperature_invalid_data(monkeypatch):
    """Test that an excpetion is raised if the data are always invalid."""
    monkeypatch.setattr(Path, "read_text", lambda *x: "")
    with pytest.raises(thermometer.UnexpectedDeviceData):
        thermometer.temperature(Path("device"), retries=0)


def test_sample_temperature(monkeypatch):
    """Test the sampler."""
    L = [0, 1, 0, 1, 0]
    expected = tuple(L)
    monkeypatch.setattr(thermometer, "temperature", lambda *x, **k: L.pop())
    samples = thermometer.sample_temperature(samples=5)
    assert samples == expected


def test_quantiles():
    """Test the quantiles function.
    
    I know this works bc its base lib but coverage y'know?
    """
    assert thermometer.quantiles([1, 2, 3]) == [1, 2, 3]

    with pytest.raises(statistics.StatisticsError):
        thermometer.quantiles([1, 2, 3], n=0)

    with pytest.raises(statistics.StatisticsError):
        thermometer.quantiles([1])


def test_temperature_strict(monkeypatch):
    """Test that the correct temperature is returned with valid data."""
    L = [70.0, 70.0, 70.1, 70.1, 70.2, 70.2]
    monkeypatch.setattr(thermometer, "temperature", lambda *x, **k: L.pop())
    assert thermometer.temperature_strict(samples=6) == 70.1


def test_temperature_strict_variable(monkeypatch):
    """Test that an exception is raised if a variable temperature is read."""
    L = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
    monkeypatch.setattr(thermometer, "temperature", lambda *x, **k: L.pop())
    with pytest.raises(thermometer.InconsistentTemperature):
        thermometer.temperature_strict(retries=1, samples=3)

    # should be fine if you increase the max iqr
    L = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
    thermometer.temperature_strict(retries=1, samples=3, max_iqr=10)


def test_cli(monkeypatch):
    """Just test that the cli runs."""
    monkeypatch.setattr(
        argparse.ArgumentParser,
        "parse_args",
        lambda *x: argparse.Namespace(
            unit=None,
            device=None,
            retries=None,
            device_folder=None,
            device_suffix=None,
            no_strict=None,
            max_iqr=None,
            samples=None,
        ),
    )
    monkeypatch.setattr(thermometer, "temperature", lambda *x, **k: 0)

    cli.main()
