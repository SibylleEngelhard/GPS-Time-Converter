# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 10:12:33 2022

@author: Sibylle
"""


import datetime
import time

gpsweek=0
gpsseconds=0

datetimeformat = "%Y-%m-%d %H:%M:%S"
beginning_epoch = datetime.datetime.strptime("1980-01-06 00:00:00",datetimeformat)



#elapsed = datetime.timedelta(days=(gpsweek*7),seconds=(gpsseconds))
#gpstime=beginning_epoch + elapsed
#print(gpstime)
weekinsec=60*60*24*7
print(weekinsec)
#604800
calc_epoch = datetime.datetime.strptime("2022-09-19 00:00:00",datetimeformat)
gps_now=datetime.datetime.utcnow()+datetime.timedelta(seconds=18)


diff=gps_now-beginning_epoch
print(diff.total_seconds())
print(diff.total_seconds()/604800)
tt=diff.total_seconds()
week=int(diff.total_seconds()/604800)
print(week)
sec_day=tt/86400
print(sec_day)
utc_time_now=datetime.datetime.utcnow()

print(utc_time_now.strftime("%Y-%m-%d %H:%M:%S %w"))
print(utc_time_now.strftime("%Y-%m-%d %H:%M:%S %j"))
print(utc_time_now.strftime("%Y-%m-%d %H:%M:%S"))

#local_time_now=datetime.datetime.now()
#d=local_time_now-utc_time_now
#print(d)#print(utc_time_now)
#print(datetime.datetime.utcnow())

#print(datetime.timezone(d))

#print(utc_time_now.astimezone())
#print(local_time_now.astimezone())


#print(utc_time_now.day)
#print(utc_time_now.strftime("%B"))
#print(utc_time_now.strftime("%Y"))
#print(utc_time_now.hour)
#print(utc_time_now.minute)
#print(utc_time_now.second)

#tz=utc_time_now.tzinfo
#print(utc_time_now.tzinfo.tzname)
#print(local_time.tzinfo.tzname)
#print(datetime.datetime.now(datetime.timezone(datetime.timedelta(0))).astimezone().tzinfo)
#print(datetime.datetime.utcnow().astimezone().tzinfo)
"""
import datetime
import pytz

dtObject_utc = datetime.datetime.now(pytz.utc)

dtObject_asia = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
dtObject_usc = datetime.datetime.now(pytz.timezone('US/Central'))
dtObject_turkey = datetime.datetime.now(pytz.timezone('Turkey'))
dtObject_eoslo = datetime.datetime.now(pytz.timezone('Europe/Oslo'))
dtObject_abelem = datetime.datetime.now(pytz.timezone('America/Belem'))

print(dtObject_utc)

print(dtObject_asia)
print(dtObject_usc)
print(dtObject_turkey)
print(dtObject_eoslo)
print(dtObject_abelem)
"""