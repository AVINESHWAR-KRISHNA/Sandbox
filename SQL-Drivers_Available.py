print("\n\nChecking Available SQL Server Drivers.")

import pyodbc

drivers = pyodbc.drivers()

print("\nAvailable Drivers...\n")

for driver in drivers:

    print(driver) 