# Create DbLog device in FHEM

Make sure that the history table is already defined in the MySQL DB.

```text
define myDbLog DbLog ./configDb.conf .*:(Temperature|Humidity|Pressure|ValvePosition|desired-temp|batteryLevel).*
```