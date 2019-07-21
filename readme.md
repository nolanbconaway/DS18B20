# thermometer

This is a python module for handling temperatures from my raspberry pi thermometer. This will be useful
to those who followed a tutorial for setting up a DS18B20 temperature sensor, [like this one](https://www.hackster.io/timfernando/a-raspberry-pi-thermometer-you-can-access-anywhere-33061c).

You can find a website showing my apartment's current temperature [here](https://temp-in-nolans-apartment.herokuapp.com/).

It is principally a bus reader to convert raw text from the thermometer device to a float value
specifying degrees Fahrenheit. It also has command line tools to:

1. print the current temp to the console.
2. save the current temp to a database.

I am able to hold all the complexity in my head and the whole thing is basically integration code
(bus reader, database code, etc), so there are no tests. Sorry.
