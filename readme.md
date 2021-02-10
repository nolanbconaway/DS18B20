# DS18B20 Thermometer

> **2020-02-10**: My DS18B20 busted and I started using a DHT22, so this repo is no longer under development.

This is a python module for reading temperatures from a raspberry pi thermometer. It is tested on python 3.5-3.8 and has zero dependencies.

This will be useful to those who followed a tutorial for setting up a DS18B20 temperature sensor, [like this one](https://www.hackster.io/timfernando/a-raspberry-pi-thermometer-you-can-access-anywhere-33061c).

## Install

After you've installed your python 3.5+ environment with pip, run:

```sh
pip3 install git+https://github.com/nolanbconaway/DS18B20.git
```

## Python API

Usually you just want to know what the temperature reading is. Do:

```python
import thermometer

temp_f = thermometer.temperature()

# or

temp_c = thermometer.temperature(unit='C')
```

Under the hood, `thermometer` identified your thermometer device, then parsed and validated its output.

My thermometer occasionally generates highly variable temperature measurements, like shooting from 75F to 95F in a minute. I have included a strict reading function which takes the median
of multiple samples from the device and raises an error if the measurements are too variable.

```python
temp_f = thermometer.temperature_strict(unit='F', samples=10, max_iqr=0.5)
```

## CLI

The `temperature` command line tool is also installed. Use it like:

```txt
$ temperature
70.36160000000001

$ temperature -h
usage: temperature [-h] [-u {C,F}] [-d DEVICE] [-r RETRIES]
              [--device-folder DEVICE_FOLDER] [--device-suffix DEVICE_SUFFIX]
              [--no-strict] [--max-iqr MAX_IQR] [--samples SAMPLES]

Print the current temperature.

optional arguments:
  -h, --help            show this help message and exit
  -u {C,F}, --unit {C,F}
                        Celsius or Fahrenheit choice. Default Fahrenheit.
  -d DEVICE, --device DEVICE
                        Optional path to the thermometer device. Will attempt
                        to find it if not provided.
  -r RETRIES, --retries RETRIES
                        Number of read attempts (in case data are not as
                        expected). Default 20.
  --device-folder DEVICE_FOLDER
                        Optional path to the system bus devices. Used as kwarg
                        to ``find_device``. Ignored if device is provided.
  --device-suffix DEVICE_SUFFIX
                        Optional suffix of slave file found within the device
                        folder. Used as kwarg to ``find_device``. Ignored if
                        device is provided.
  --no-strict           Turn off the strict reading handler.
  --max-iqr MAX_IQR     Maximum interquartile range allowable in a strict
                        reading. Ignored if --no-strict.
  --samples SAMPLES     Number of samples to take for strict reading. Ignored
                        if --no-strict.
```

This can be useful for one-liners to record the temperature in e.g., a cron job--

```sh
$ echo $(date) ',' $(temperature --unit C) >> temps.csv
```

A more practical example: I run a cron job to record the temperature every minute and store the result in my postgres database. Here is that cron:

```sh
DEGREES=$(temperature) && psql -c "insert into temperatures (fahrenheit) values ($DEGREES);" > /dev/null
```
