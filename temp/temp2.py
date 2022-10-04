import streamlit as st
import datetime
import time


def update_utc_now():
	st.session_state.utc_time=datetime.datetime.utcnow().replace(microsecond=0)
	st.session_state.sess_local_time_now=datetime.datetime.now().replace(microsecond=0)
	st.session_state.show_local_time=True
	update_utc_and_to_gps()

def update_utc_time_zero():
	st.session_state.utc_time=st.session_state.utc_time.replace(minute=00, hour=00, second=00)
	#st.session_state.utc_hour=st.session_state.utc_time.hour
	#st.session_state.utc_minute=st.session_state.utc_time.minute
	#st.session_state.utc_second=st.session_state.utc_time.second
	st.session_state.show_local_time=False
	update_utc_and_to_gps()

def change_utc_day():
	st.session_state.show_local_time=False
	beginning_of_month_utc_day=st.session_state.utc_time.replace(day=1)
	daysofmonth_timedelta=datetime.timedelta(days=st.session_state.utc_day-beginning_of_month_utc_day.day)
	st.session_state.utc_time=beginning_of_month_utc_day+daysofmonth_timedelta
	update_utc_and_to_gps()

def change_utc_month():
	st.session_state.show_local_time=False
	dayerror=True
	oneday_timedelta=datetime.timedelta(days=1)
	while dayerror:
		try:
			st.session_state.utc_time=st.session_state.utc_time.replace(month=month_list.index(st.session_state.utc_month)+1)
			dayerror=False
		except:
			st.session_state.utc_time=st.session_state.utc_time-oneday_timedelta
	update_utc_and_to_gps()

def change_utc_year():
	st.session_state.show_local_time=False
	dayerror=True
	oneday_timedelta=datetime.timedelta(days=1)
	while dayerror:
		try:
			st.session_state.utc_time=st.session_state.utc_time.replace(year=int(st.session_state.utc_year))
			dayerror=False
		except:
			st.session_state.utc_time=st.session_state.utc_time-oneday_timedelta
	update_utc_and_to_gps()

def change_utc_hour():
	st.session_state.show_local_time=False
	beginning_of_day_utc_hour=st.session_state.utc_time.replace(hour=00)
	hoursofday_timedelta=datetime.timedelta(hours=st.session_state.utc_hour-beginning_of_day_utc_hour.hour)
	st.session_state.utc_time=beginning_of_day_utc_hour+hoursofday_timedelta
	update_utc_and_to_gps()

def change_utc_minute():
	st.session_state.show_local_time=False
	beginning_of_hour_utc_minute=st.session_state.utc_time.replace(minute=00)
	minutesofhour_timedelta=datetime.timedelta(minutes=st.session_state.utc_minute-beginning_of_hour_utc_minute.minute)
	st.session_state.utc_time=beginning_of_hour_utc_minute+minutesofhour_timedelta
	
	update_utc_and_to_gps()

def change_utc_second():
	st.session_state.now_leapsecond=False
	st.session_state.show_local_time=False
	beginning_of_minute_utc_second=st.session_state.utc_time.replace(second=00) #utc datetime beginning of minute
	
	beginning_of_utc_minute_leap_seconds=calc_leapseconds_from_utctime(beginning_of_minute_utc_second)#leapseconds at beginning of minute
	beginning_of_minute_gps_time=beginning_of_minute_utc_second+datetime.timedelta(seconds=beginning_of_utc_minute_leap_seconds)

	st.write(f"Beginning of minute utc time: {beginning_of_minute_utc_second}")
	st.write(f"current leap seconds: {beginning_of_utc_minute_leap_seconds}")
	st.write(f"Beginning of minute gps time: {beginning_of_minute_gps_time}")
	secondsofminute_timedelta=datetime.timedelta(seconds=st.session_state.utc_second) #utc seconds entered
	st.write(f"seconds entered: {secondsofminute_timedelta}")
	temp_gps_time=beginning_of_minute_gps_time+secondsofminute_timedelta
	temp_total_gps_seconds=round((temp_gps_time-gps_beginning_epoch).total_seconds())
	st.write(f"total gps seconds: {temp_total_gps_seconds}")
	st.write(f"gps time: {temp_gps_time}")
	
	
	#todo: rename variables
	
	
	if temp_total_gps_seconds in leapseconds_list:
		if st.session_state.utc_second==-1:
			st.session_state.utc_second=60
		st.session_state.now_leapsecond=True
		st.session_state.leapseconds=calc_leapseconds_from_gpstime(temp_gps_time)
		#st.write(f"here now leap seconds: {st.session_state.leapseconds}")
	
		st.session_state.utc_time=temp_gps_time-datetime.timedelta(seconds=st.session_state.leapseconds)
		#st.write(f" here utc time: {st.session_state.utc_time}")
		
		st.session_state.utc_day=st.session_state.utc_time.day
		st.session_state.utc_month=st.session_state.utc_time.strftime("%B")
		st.session_state.utc_year=st.session_state.utc_time.strftime("%Y")
		st.session_state.utc_hour=st.session_state.utc_time.hour
		st.session_state.utc_minute=st.session_state.utc_time.minute
		#st.session_state.utc_second=st.session_state.utc_time.second

		#st.session_state.gps_time=st.session_state.utc_time+datetime.timedelta(seconds=st.session_state.leapseconds)
		st.session_state.gps_dayofyear=int(st.session_state.gps_time.strftime("%j"))
		st.session_state.gps_week=gps_datetime_to_totalseconds(st.session_state.gps_time)//604800
		st.session_state.gps_dayofweek=st.session_state.gps_time.strftime("%w")
		st.session_state.gps_total_seconds=gps_datetime_to_totalseconds(st.session_state.gps_time)
		st.session_state.gps_seconds_per_week=int(gps_datetime_to_totalseconds(st.session_state.gps_time)%604800)
		st.session_state.gps_seconds_per_day=int(gps_datetime_to_totalseconds(st.session_state.gps_time)%86400)


		
	else:
		st.session_state.now_leapsecond=False
		st.session_state.leapseconds=calc_leapseconds_from_gpstime(temp_gps_time)
		#st.write(f"now leap seconds: {st.session_state.leapseconds}")
		st.session_state.utc_time=temp_gps_time-datetime.timedelta(seconds=st.session_state.leapseconds)
		#st.write(f" utc time: {st.session_state.utc_time}")
		update_utc_and_to_gps()

def utc_datetime_to_totalseconds(utc_datetime):
	return (utc_datetime-gps_beginning_epoch).total_seconds()


def gps_datetime_to_totalseconds(gps_datetime):
	return (gps_datetime-gps_beginning_epoch).total_seconds()

def gps_totalseconds_to_datetime(gps_totalseconds):
	gps_timedelta = datetime.timedelta(seconds=gps_totalseconds)
	return gps_beginning_epoch+gps_timedelta

def update_utc_and_to_gps():
	st.session_state.utc_day=st.session_state.utc_time.day
	st.session_state.utc_month=st.session_state.utc_time.strftime("%B")
	st.session_state.utc_year=st.session_state.utc_time.strftime("%Y")
	st.session_state.utc_hour=st.session_state.utc_time.hour
	st.session_state.utc_minute=st.session_state.utc_time.minute
	st.session_state.utc_second=st.session_state.utc_time.second

	st.session_state.leapseconds=calc_leapseconds_from_utctime(st.session_state.utc_time)
	st.session_state.gps_time=st.session_state.utc_time+datetime.timedelta(seconds=st.session_state.leapseconds)
	st.session_state.gps_dayofyear=int(st.session_state.gps_time.strftime("%j"))
	st.session_state.gps_week=gps_datetime_to_totalseconds(st.session_state.gps_time)//604800
	st.session_state.gps_dayofweek=st.session_state.gps_time.strftime("%w")
	st.session_state.gps_total_seconds=gps_datetime_to_totalseconds(st.session_state.gps_time)
	st.session_state.gps_seconds_per_week=int(gps_datetime_to_totalseconds(st.session_state.gps_time)%604800)
	st.session_state.gps_seconds_per_day=int(gps_datetime_to_totalseconds(st.session_state.gps_time)%86400)
	#st.session_state.leapseconds=calc_leapseconds(st.session_state.utc_time)

def update_gps_and_to_utc():
	st.session_state.gps_dayofyear=int(st.session_state.gps_time.strftime("%j"))
	st.session_state.gps_week=round(gps_datetime_to_totalseconds(st.session_state.gps_time)//604800)
	st.session_state.gps_dayofweek=st.session_state.gps_time.strftime("%w")
	st.session_state.gps_total_seconds=round(gps_datetime_to_totalseconds(st.session_state.gps_time))
	st.session_state.gps_seconds_per_week=int(gps_datetime_to_totalseconds(st.session_state.gps_time)%604800)
	st.session_state.gps_seconds_per_day=int(gps_datetime_to_totalseconds(st.session_state.gps_time)%86400)

	st.session_state.leapseconds=calc_leapseconds_from_gpstime(st.session_state.gps_time)

	st.session_state.utc_time=st.session_state.gps_time-datetime.timedelta(seconds=st.session_state.leapseconds)
	
	st.session_state.utc_day=st.session_state.utc_time.day
	st.session_state.utc_month=st.session_state.utc_time.strftime("%B")
	st.session_state.utc_year=st.session_state.utc_time.strftime("%Y")
	st.session_state.utc_hour=st.session_state.utc_time.hour
	st.session_state.utc_minute=st.session_state.utc_time.minute
	
	if st.session_state.gps_total_seconds in leapseconds_list:
		st.session_state.utc_second=60
		st.session_state.now_leapsecond=True
	else:
		st.session_state.utc_second=st.session_state.utc_time.second
		st.session_state.now_leapsecond=False

	st.session_state.show_local_time=False


def change_gps_dayofyear():
	beginning_of_year_gps_time=st.session_state.gps_time.replace(day=1,month=1)
	doy_timedelta=datetime.timedelta(days=st.session_state.gps_dayofyear-1)
	st.session_state.gps_time=beginning_of_year_gps_time+doy_timedelta
	update_gps_and_to_utc()

def change_gps_week():
	gps_weeks_timedelta=datetime.timedelta(seconds=st.session_state.gps_week*604800)
	gps_seconds_per_week_timedelta=datetime.timedelta(seconds=st.session_state.gps_seconds_per_week)
	st.session_state.gps_time=gps_beginning_epoch+gps_weeks_timedelta+gps_seconds_per_week_timedelta
	update_gps_and_to_utc()

def change_gps_dayofweek():	
	gps_weeks_timedelta=datetime.timedelta(seconds=st.session_state.gps_week*604800)
	gps_days_of_week_timedelta=datetime.timedelta(seconds=int(st.session_state.gps_dayofweek)*86400)
	gps_seconds_per_day_timedelta=datetime.timedelta(seconds=st.session_state.gps_seconds_per_day)
	st.session_state.gps_time=gps_beginning_epoch+gps_weeks_timedelta+gps_days_of_week_timedelta+gps_seconds_per_day_timedelta
	update_gps_and_to_utc()

def change_gps_total_seconds():	
	st.session_state.gps_time=gps_totalseconds_to_datetime(st.session_state.gps_total_seconds)
	update_gps_and_to_utc()

def change_gps_seconds_per_week():	
	gps_datetime_week_zero=gps_totalseconds_to_datetime(st.session_state.gps_week*604800)
	gps_seconds_per_week_timedelta=datetime.timedelta(seconds=st.session_state.gps_seconds_per_week)
	st.session_state.gps_time=gps_datetime_week_zero+gps_seconds_per_week_timedelta
	update_gps_and_to_utc()

def change_gps_seconds_per_day():	
	gps_datetime_zero=st.session_state.gps_time.replace(hour=00, minute=00, second=00)
	gps_seconds_per_day_timedelta=datetime.timedelta(seconds=st.session_state.gps_seconds_per_day)
	st.session_state.gps_time=gps_datetime_zero+gps_seconds_per_day_timedelta
	update_gps_and_to_utc()





#-----Page Configuration
st.set_page_config(page_title="GPS Time Converter",
	initial_sidebar_state="collapsed")

#---- Title 
st.markdown('<h1 style="margin-bottom:0rem;margin-top:0rem;text-align: center">GPS Time Converter</h1>', unsafe_allow_html=True)
#st.markdown(f'<h3 style="margin-bottom:0rem;margin-top:0rem;text-align: center">Last update: Text to add</h3>', unsafe_allow_html=True)

#----menu button invisible
#st.markdown(""" <style>#MainMenu {visibility: hidden;}footer {visibility: hidden;}</style> """, unsafe_allow_html=True)
#App Description
#col1a.markdown('''
#This app converts and transforms between different coordinate systems in the Namibian Schwarzeck datum and WGS84 datum.
#''')






leapseconds_list = [46828800, 78364801, 109900802, 173059203, 252028804, 315187205, 346723206, 393984007, 425520008, 457056009, 504489610, 551750411, 599184012, 820108813, 914803214, 1025136015, 1119744016, 1167264017]



def calc_leapseconds_from_utctime(utc_datetime):
	lp=0
	totalseconds=round((utc_datetime-gps_beginning_epoch).total_seconds())
	for i in leapseconds_list:
		if (totalseconds+leapseconds_list.index(i))>=i:
			lp+=1
	return lp

def calc_leapseconds_from_gpstime(gps_datetime):
	lp=0
	totalseconds=(gps_datetime-gps_beginning_epoch).total_seconds()
	for i in leapseconds_list:
		if totalseconds>=i:
			lp+=1
	return lp

month_list=["January","February","March","April","May","June","July","August","September","October","November","December"]
year_list=["1980","1981","1982","1983","1984","1985","1986","1987","1988","1988","1989","1990",
"1991","1992","1993","1994","1995","1996","1997","1998","1999","2000",
"2001","2002","2003","2004","2005","2006","2007","2008","2009","2010",
"2011","2012","2013","2014","2015","2016","2017","2018","2019","2020",
"2021","2022","2023","2024","2025","2026","2027","2028","2029","2030"]
dayofweek_list=["0","1","2","3","4","5","6"]
gps_beginning_epoch = datetime.datetime.strptime("1980-01-06 00:00:00","%Y-%m-%d %H:%M:%S")


if "utc_time" not in st.session_state:
	st.session_state.utc_time=datetime.datetime.utcnow().replace(microsecond=0)

local_time_now=datetime.datetime.now().replace(microsecond=0)

utc_difference=datetime.timezone(datetime.datetime.now()-datetime.datetime.utcnow())


####!!!!change with leapsecondsfuction
#leapseconds=18
#leapseconds_timedelta = datetime.timedelta(seconds=leapseconds)
#current_leapseconds=leapseconds
if "leapseconds" not in st.session_state:
	st.session_state.leapseconds=calc_leapseconds_from_utctime(st.session_state.utc_time)
if "now_leapsecond" not in st.session_state:
	st.session_state.now_leapsecond=False

if "gps_time" not in st.session_state:
	st.session_state.gps_time=st.session_state.utc_time+datetime.timedelta(seconds=st.session_state.leapseconds)

if "utc_day" not in st.session_state:
	st.session_state.utc_day=st.session_state.utc_time.day
if "utc_month" not in st.session_state:	
	st.session_state.utc_month=st.session_state.utc_time.strftime("%B")
if "utc_year" not in st.session_state:	
	st.session_state.utc_year=st.session_state.utc_time.strftime("%Y")
if "utc_hour" not in st.session_state:	
	st.session_state.utc_hour=st.session_state.utc_time.hour
if "utc_minute" not in st.session_state:	
	st.session_state.utc_minute=st.session_state.utc_time.minute
if "utc_second" not in st.session_state:
	st.session_state.utc_second=st.session_state.utc_time.second

if "show_local_time" not in st.session_state:
	st.session_state.show_local_time=True
if "sess_local_time_now" not in st.session_state:
	st.session_state.sess_local_time_now=local_time_now

if "gps_dayofyear" not in st.session_state:
	st.session_state.gps_dayofyear=int(st.session_state.gps_time.strftime("%j"))
if "gps_week" not in st.session_state:
	st.session_state.gps_week=round(gps_datetime_to_totalseconds(st.session_state.gps_time)//604800)
if "gps_dayofweek" not in st.session_state:
	st.session_state.gps_dayofweek=st.session_state.gps_time.strftime("%w")
if "gps_total_seconds" not in st.session_state:
	st.session_state.gps_total_seconds=round(gps_datetime_to_totalseconds(st.session_state.gps_time))
if "gps_seconds_per_week" not in st.session_state:
	st.session_state.gps_seconds_per_week=int(gps_datetime_to_totalseconds(st.session_state.gps_time)%604800)
if "gps_seconds_per_day" not in st.session_state:
	st.session_state.gps_seconds_per_day=int(gps_datetime_to_totalseconds(st.session_state.gps_time)%86400)




#columns for subtitle
row1_col1,row1_col2=st.columns([6,6])
with row1_col1:
	st.markdown(f'<h3 style="margin-bottom:0rem;margin-top:0rem;text-align: center">UTC Time</h3>', unsafe_allow_html=True)
with row1_col2:
	st.markdown(f'<h3 style="margin-bottom:0rem;margin-top:0rem;text-align: center">GPS Time</h3>', unsafe_allow_html=True)




row2_col1,row2_col2,row2_col3,row2_col4,row2_col5,row2_col6,row2_col7=st.columns([5,6,4,1,5,6,3])	
with row2_col1:		
	utc_day=st.number_input("Day",key="utc_day",min_value=0,max_value=32,format="%02d",on_change=change_utc_day)
with row2_col2:
	utc_month=st.selectbox("Month", month_list, key="utc_month",on_change=change_utc_month)
with row2_col3:
	utc_year=st.selectbox("Year", year_list, key="utc_year",on_change=change_utc_year)
with row2_col5:
	gps_dayofyear=st.number_input("GPS Day of Year",key="gps_dayofyear",min_value=0,max_value=367,on_change=change_gps_dayofyear)
with row2_col6:
	gps_week=st.number_input("GPS Week",key="gps_week",min_value=0,max_value=3000,on_change=change_gps_week)
with row2_col7:
	gps_dayofweek=st.selectbox("Weekday",dayofweek_list,key="gps_dayofweek",help="Sunday = 0",on_change=change_gps_dayofweek)


row3_col1,row3_col2,row3_col3,row3_col4,row3_col5,row3_col6,row3_col7=st.columns([4,4,4,5,10,2,3])	
with row3_col1:
	st.subheader("")
	st.write("Set Time:")
with row3_col2:
	st.write("")
	st.button("Now",key="but1",help="according to settings of your PC",on_click=update_utc_now)
with row3_col3:
	st.write("")
	st.button("0:00:00",key="but2",on_click=update_utc_time_zero)
#with row3_col5:
#	gps_total_seconds=st.number_input("GPS Time (total seconds)",key="gps_total_seconds",min_value=0,on_change=change_gps_total_seconds)


row4_col1,row4_col2,row4_col3,row4_col4,row4_col5,row4_col6,row4_col7=st.columns([5,5,5,2,10,2,3])
with row4_col1:
	st.number_input("Hours",key="utc_hour",min_value=-1,max_value=24,format="%02d",on_change=change_utc_hour)
with row4_col2:
	st.number_input("Minutes",key="utc_minute",min_value=-1,max_value=60,format="%02d",on_change=change_utc_minute)
with row4_col3:
	st.number_input("Seconds",key="utc_second",min_value=-1,max_value=61,format="%02d",on_change=change_utc_second)
with row4_col5:
	gps_total_seconds=st.number_input("GPS Time (total seconds)",key="gps_total_seconds",min_value=0,on_change=change_gps_total_seconds)




row5_col1,row5_col2,row5_col3,row5_col4,row5_col5,row5_col6,row5_col7=st.columns([9,5,1,2,7,7,1])	
with row5_col1:
	pl=st.empty()
	if st.session_state.show_local_time:
		local_time_now=st.session_state.sess_local_time_now
		pl.write(f"Local Time ({utc_difference}) :")
	
	else:
		pl.write("&nbsp;")

	st.write("Leap Seconds at UTC Time:")	
with row5_col2:
	pl=st.empty()
	if st.session_state.show_local_time:
		pl.write(f"{local_time_now.strftime('%H:%M:%S')}")
	elif st.session_state.now_leapsecond:
		#pl.write(f"Leap second!!!")
		pl.markdown("<small style='color: #f63366'>Leap second !!!<br></small>", unsafe_allow_html=True) 
	
	else:
		pl.write("&nbsp;")
	st.write(str(st.session_state.leapseconds))


with row5_col5:
	gps_seconds_per_week=st.number_input("Seconds of Week",key="gps_seconds_per_week",min_value=0,max_value=604800,on_change=change_gps_seconds_per_week)
with row5_col6:
	gps_seconds_per_day=st.number_input("Seconds of Day",key="gps_seconds_per_day",min_value=0,max_value=86400,on_change=change_gps_seconds_per_day)


#row6_col1,row6_col2,row6_col3=st.columns([17,1,16])	
#with row6_col1:
#	st.markdown("---")

#with row6_col3:
#	st.markdown("---")

######################################################################
#---------------------------------#
# About
st.subheader("  ")
expander_bar = st.expander('About this app')
expander_bar.markdown('''
- **UTC Time**: (Coordinated Universal Time) is the global time standard. Local times have their appropriate UTC offsets.
- **Time Now:**  Local date/time and corresponding UTC time are based on the setting of your PC clock.
- **Leap seconds:**  To keep the UTC time synchronised with the Earth’s rotation, additional leap seconds are added from time to time. Leap seconds are applied either on 31-December or 30-June. The last leap second was added on 31-December-2016 23:59:60   https://maia.usno.navy.mil/products/leap-second
- **GPS Time**: The GPS system uses GPS time which was zero on 06-January-1980 00:00:00. GPS time does not include leap seconds and is currently (2022) ahead of UTC time by 18 seconds.
- No warranty is given that the information provided in this app is free of errors.
- for problems and suggestions contact: s.engelhard@gmx.net
- last updated in 2022
''')
#---------------------------------#