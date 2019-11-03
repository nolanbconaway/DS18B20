# thermometer

[![badge](https://github.com/nolanbconaway/thermometer/workflows/Main%20Workflow/badge.svg)](https://github.com/nolanbconaway/thermometer/actions)

This is a python (3.5+) module for reading temperatures from a raspberry pi thermometer. This will be useful to those who followed a tutorial for setting up a DS18B20 temperature sensor, [like this one](https://www.hackster.io/timfernando/a-raspberry-pi-thermometer-you-can-access-anywhere-33061c).

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

