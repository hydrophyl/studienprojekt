#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOST = "localhost"
PORT = 4223
UID = "LdW" # Change XYZ to the UID of your Particulate Matter Bricklet

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_particulate_matter import BrickletParticulateMatter

#setting up packages
import pandas as pd
import datetime
from time import strftime,localtime

#Erstellung ein pandas dataframe
df = pd.DataFrame({'Datum': [],
                   'Zeit': [],
                   'PM10': [],
                   'PM25': [],
                   'PM100': []})

# Callback function for PM concentration callback
def cb_pm_concentration(pm10, pm25, pm100):
    #Wiederholungen
    time_only = datetime.datetime.now().time().strftime("%H:%M:%S")
    date_local = strftime("%d%b%Y", localtime())

    #Messungsdaten einfuegen
    df.loc[len(df.index)] = [date_local,time_only,pm10,pm25,pm100]

    #Update .csv Datei
    df.to_csv(date_local + ".csv", index=False, encoding='utf8')


if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    pm = BrickletParticulateMatter(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    # Register PM concentration callback to function cb_pm_concentration
    pm.register_callback(pm.CALLBACK_PM_CONCENTRATION, cb_pm_concentration)

    # Set period for PM concentration callback to 1s (1000ms)
    pm.set_pm_concentration_callback_configuration(1000, False)

    input("Press key to exit\n") # Use raw_input() in Python 2
    ipcon.disconnect()