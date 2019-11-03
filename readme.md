# thermometer

[![badge](https://github.com/nolanbconaway/thermometer/workflows/Main%20Workflow/badge.svg)](https://github.com/nolanbconaway/thermometer/actions)

This is a python module for reading temperatures from a raspberry pi thermometer. It has been tested on python 3.5+ and has zero dependencies.

This will be useful to those who followed a tutorial for setting up a DS18B20 temperature sensor, [like this one](https://www.hackster.io/timfernando/a-raspberry-pi-thermometer-you-can-access-anywhere-33061c).

## Install

After you've installed your python 3.5+ environment with pip, run:

``` sh
pip3 install git+https://github.com/nolanbconaway/thermometer.git
```

## Python API

Usually you just want to know what the temperature reading is. Do:

``` python
import thermometer

temp_f = thermometer.temperature()

# or

temp_c = thermometer.temperature(unit='C')
```

Under the hood, `thermometer` identified your thermometer device, then parsed and validated its output.

## CLI

The `temperature` command line tool is also installed. Use it like:

``` txt
$ temperature
70.36160000000001

$ temperature -h
usage: temperature [-h] [-u {F,C}] [-d DEVICE] [-r RETRIES]
                   [--device-folder DEVICE_FOLDER]
                   [--device-suffix DEVICE_SUFFIX]

Print the current temperature.

optional arguments:
  -h, --help            show this help message and exit
  -u {F,C}, --unit {F,C}
                        Celsius or Fahrenheit choice. Default Fahrenheit.
  -d DEVICE, --device DEVICE
                        Optional path to the thermometer device. Will attempt
                        to find it if not provided.
  -r RETRIES, --retries RETRIES
                        Number of read attempts (in case data are not as
                        expected). Default 20.
  --device-folder DEVICE_FOLDER
                        Path to the system bus devices. Used as kwarg to
` ` find_device ` ` . Ignored if device is provided.
  --device-suffix DEVICE_SUFFIX
                        Suffix of slave file found within the device folde.
                        Used as kwarg to ` ` find_device ` ` . Ignored if device is
                        provided.
```

This can be useful for one-liners to record the temperature in e.g., a cron job--

``` sh
$ echo $(date) ',' $(temperature --unit C) >> temps.csv
```

