# GPS Time Converter
Convert between UTC/Local Time and GPS Time
- **UTC**: UTC (Coordinated Universal Time) is the primary time standard by which the world regulates clocks and time. Local times have their appropriate UTC offsets according to timezones.
- **Local Time**: The Local time can be shown if the correct timezone is selected. Timezones can be selected from a list of all common and currently used time zones which are derived from the Python module **pytz** - https://pypi.org/project/pytz/
- **Leap seconds:**  To keep UTC synchronised with the Earth’s rotation, additional leap seconds are added or subtracted from time to time. Leap seconds are applied either on 31-December or 30-June. The last leap second was added on 31-December-2016 23:59:60.   https://maia.usno.navy.mil/products/leap-second
- **GPS Time**: The GPS system uses GPS time which was zero on 06-January-1980 00:00:00. GPS time does not include leap seconds and is currently (2023) ahead of UTC by 18 seconds.
- for problems and suggestions contact: s.engelhard@gmx.net