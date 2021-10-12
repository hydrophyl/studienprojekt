#a little high-end code
from  prettytable import PrettyTable
import time, os
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_particulate_matter import BrickletParticulateMatter

myTable = PrettyTable(["PM1.0", "PM2.5", "PM10.0"])

HOST = "localhost"
PORT = 4223
UID = "LdW" # Change XYZ to the UID of your Particulate Matter Bricklet

ipcon = IPConnection() # Create IP connection
pm = BrickletParticulateMatter(UID, ipcon) # Create device object
ipcon.connect(HOST, PORT) # Connect to brickd
# Don't use device before ipcon is connected
a = "press Ctrl+C to quit!"
print(a)

while True:
    pm10, pm25, pm100 = pm.get_pm_concentration()
    myTable.add_row([pm10,pm25,pm100])
    time.sleep(1) #wait for 1s
    os.system("cls")
    print(myTable)

ipcon.disconnect