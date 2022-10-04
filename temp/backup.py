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
	st.session_state.now_positive_leapsecond=False
	st.session_state.show_local_time=False
	beginning_of_month_utc_day=st.session_state.utc_time.replace(day=1)
	daysofmonth_timedelta=datetime.timedelta(days=st.session_state.utc_day-beginning_of_month_utc_day.day)
	st.session_state.utc_time=beginning_of_month_utc_day+daysofmonth_timedelta
	update_utc_and_to_gps()

def change_utc_month():
	st.session_state.now_positive_leapsecond=False
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
	st.session_state.now_positive_leapsecond=False
	st.session_state.show_local_time=False
	st.session_state.utc_time=st.session_state.utc_time.replace(year=st.session_state.utc_year)
	update_utc_and_to_gps()

def change_utc_hour():
	st.session_state.now_positive_leapsecond=False
	st.session_state.show_local_time=False
	beginning_of_day_utc_hour=st.session_state.utc_time.replace(hour=00)
	hoursofday_timedelta=datetime.timedelta(hours=st.session_state.utc_hour-beginning_of_day_utc_hour.hour)
	st.session_state.utc_time=beginning_of_day_utc_hour+hoursofday_timedelta
	update_utc_and_to_gps()

def change_utc_minute():
	st.session_state.now_positive_leapsecond=False
	st.session_state.show_local_time=False
	beginning_of_hour_utc_minute=st.session_state.utc_time.replace(minute=00)
	minutesofhour_timedelta=datetime.timedelta(minutes=st.session_state.utc_minute-beginning_of_hour_utc_minute.minute)
	st.session_state.utc_time=beginning_of_hour_utc_minute+minutesofhour_timedelta
	update_utc_and_to_gps()

def change_utc_second():
	st.session_state.now_positive_leapsecond=False
	st.session_state.show_local_time=False
	beginning_of_minute_utc_second=st.session_state.utc_time.replace(second=00) #utc datetime beginning of minute
	beginning_of_utc_minute_leap_seconds=calc_leapseconds_from_utctime(beginning_of_minute_utc_second)#leapseconds at beginning of minute
	beginning_of_minute_gps_time=beginning_of_minute_utc_second+datetime.timedelta(seconds=beginning_of_utc_minute_leap_seconds)
	secondsofminute_timedelta=datetime.timedelta(seconds=st.session_state.utc_second) #utc seconds entered
	st.session_state.gps_time=beginning_of_minute_gps_time+secondsofminute_timedelta
	st.session_state.gps_total_seconds=round((st.session_state.gps_time-gps_beginning_epoch).total_seconds())
	st.session_state.leapseconds=calc_leapseconds_from_gpstime(st.session_state.gps_time)
		
	if st.session_state.gps_total_seconds in positive_leapseconds_list: ###leapsecond
		if st.session_state.utc_second==-1:
			st.session_state.utc_second=60
		st.session_state.now_positive_leapsecond=True
		st.session_state.utc_time=st.session_state.gps_time-datetime.timedelta(seconds=st.session_state.leapseconds)
		#function update_utc_and_to_gps is not called because in this case st.session_state.utc_seconds needs to stay at 60 and differs from utc_time
		st.session_state.utc_day=st.session_state.utc_time.day
		st.session_state.utc_month=st.session_state.utc_time.strftime("%B")
		st.session_state.utc_year=st.session_state.utc_time.year
		st.session_state.utc_hour=st.session_state.utc_time.hour
		st.session_state.utc_minute=st.session_state.utc_time.minute

		st.session_state.gps_dayofyear=int(st.session_state.gps_time.strftime("%j"))
		st.session_state.gps_week=st.session_state.gps_total_seconds//604800
		st.session_state.gps_dayofweek=st.session_state.gps_time.strftime("%w")
		st.session_state.gps_seconds_per_week=int(st.session_state.gps_total_seconds%604800)
		st.session_state.gps_seconds_per_day=int(st.session_state.gps_total_seconds%86400)
		
	else:
		st.session_state.now_positive_leapsecond=False
		st.session_state.utc_time=st.session_state.gps_time-datetime.timedelta(seconds=st.session_state.leapseconds)
		update_utc_and_to_gps()


def update_utc_and_to_gps():
	if st.session_state.utc_time<gps_beginning_epoch:
		row1_col1.warning("GPS Time begins on 06-January-1980")
		st.session_state.utc_time=gps_beginning_epoch
	elif st.session_state.utc_time>datetime_limit:
		row1_col1.warning("Datetime limit currently set to 31-December-2030")
		st.session_state.utc_time=datetime_limit
	st.session_state.utc_day=st.session_state.utc_time.day
	st.session_state.utc_month=st.session_state.utc_time.strftime("%B")
	st.session_state.utc_year=st.session_state.utc_time.year
	st.session_state.utc_hour=st.session_state.utc_time.hour
	st.session_state.utc_minute=st.session_state.utc_time.minute
	st.session_state.utc_second=st.session_state.utc_time.second

	st.session_state.leapseconds=calc_leapseconds_from_utctime(st.session_state.utc_time)
	st.session_state.gps_time=st.session_state.utc_time+datetime.timedelta(seconds=st.session_state.leapseconds)
	st.session_state.gps_total_seconds=round((st.session_state.gps_time-gps_beginning_epoch).total_seconds())
	st.session_state.gps_dayofyear=int(st.session_state.gps_time.strftime("%j"))
	st.session_state.gps_week=st.session_state.gps_total_seconds//604800
	st.session_state.gps_dayofweek=st.session_state.gps_time.strftime("%w")
	st.session_state.gps_seconds_per_week=int(st.session_state.gps_total_seconds%604800)
	st.session_state.gps_seconds_per_day=int(st.session_state.gps_total_seconds%86400)

def update_gps_and_to_utc():
	if st.session_state.gps_time<gps_beginning_epoch:
		row1_col3.warning("GPS Time begins on 06-January-1980")
		st.session_state.gps_time=gps_beginning_epoch
	elif (st.session_state.gps_time-datetime.timedelta(seconds=calc_leapseconds_from_gpstime(st.session_state.gps_time)))>datetime_limit:
		row1_col3.warning("Datetime limit currently set to 31-December-2030")
		st.session_state.gps_time=datetime_limit+datetime.timedelta(seconds=calc_leapseconds_from_gpstime(st.session_state.gps_time))

	st.session_state.gps_total_seconds=round((st.session_state.gps_time-gps_beginning_epoch).total_seconds())
	st.session_state.gps_dayofyear=int(st.session_state.gps_time.strftime("%j"))
	st.session_state.gps_week=round(st.session_state.gps_total_seconds//604800)
	st.session_state.gps_dayofweek=st.session_state.gps_time.strftime("%w")
	st.session_state.gps_seconds_per_week=int(st.session_state.gps_total_seconds%604800)
	st.session_state.gps_seconds_per_day=int(st.session_state.gps_total_seconds%86400)

	st.session_state.leapseconds=calc_leapseconds_from_gpstime(st.session_state.gps_time)
	st.session_state.utc_time=st.session_state.gps_time-datetime.timedelta(seconds=st.session_state.leapseconds)
	st.session_state.utc_day=st.session_state.utc_time.day
	st.session_state.utc_month=st.session_state.utc_time.strftime("%B")
	st.session_state.utc_year=st.session_state.utc_time.year
	st.session_state.utc_hour=st.session_state.utc_time.hour
	st.session_state.utc_minute=st.session_state.utc_time.minute
	
	if st.session_state.gps_total_seconds in positive_leapseconds_list:
		st.session_state.utc_second=60
		st.session_state.now_positive_leapsecond=True
	else:
		st.session_state.utc_second=st.session_state.utc_time.second
		st.session_state.now_positive_leapsecond=False

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
	st.session_state.gps_time=gps_beginning_epoch+datetime.timedelta(seconds=st.session_state.gps_total_seconds)
	update_gps_and_to_utc()

def change_gps_seconds_per_week():	
	gps_datetime_week_zero=gps_beginning_epoch+datetime.timedelta(seconds=st.session_state.gps_week*604800)
	gps_seconds_per_week_timedelta=datetime.timedelta(seconds=st.session_state.gps_seconds_per_week)
	st.session_state.gps_time=gps_datetime_week_zero+gps_seconds_per_week_timedelta
	update_gps_and_to_utc()

def change_gps_seconds_per_day():	
	gps_datetime_zero=st.session_state.gps_time.replace(hour=00, minute=00, second=00)
	gps_seconds_per_day_timedelta=datetime.timedelta(seconds=st.session_state.gps_seconds_per_day)
	st.session_state.gps_time=gps_datetime_zero+gps_seconds_per_day_timedelta
	update_gps_and_to_utc()


def calc_leapseconds_from_utctime(utc_datetime):
	lp=0
	totalseconds=round((utc_datetime-gps_beginning_epoch).total_seconds())
	for i in positive_leapseconds_list:
		if (totalseconds+positive_leapseconds_list.index(i))>=i:
			lp+=1
	return lp

def calc_leapseconds_from_gpstime(gps_datetime):
	lp=0
	totalseconds=(gps_datetime-gps_beginning_epoch).total_seconds()
	for i in positive_leapseconds_list:
		if totalseconds>=i:
			lp+=1
	return lp


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


#setting variables
positive_leapseconds_list = [46828800, 78364801, 109900802, 173059203, 252028804, 315187205, 346723206, 393984007, 425520008, 457056009, 504489610, 551750411, 599184012, 820108813, 914803214, 1025136015, 1119744016, 1167264017]

month_list=["January","February","March","April","May","June","July","August","September","October","November","December"]

dayofweek_list=["0","1","2","3","4","5","6"]
gps_beginning_epoch = datetime.datetime.strptime("1980-01-06 00:00:00","%Y-%m-%d %H:%M:%S")
datetime_limit = datetime.datetime.strptime("2030-12-31 23:59:59","%Y-%m-%d %H:%M:%S")


if "utc_time" not in st.session_state:
	st.session_state.utc_time=datetime.datetime.utcnow().replace(microsecond=0)

local_time_now=datetime.datetime.now().replace(microsecond=0)

utc_difference=datetime.timezone(datetime.datetime.now().replace(microsecond=0)-datetime.datetime.utcnow().replace(microsecond=0))

if "leapseconds" not in st.session_state:
	st.session_state.leapseconds=calc_leapseconds_from_utctime(st.session_state.utc_time)
if "now_positive_leapsecond" not in st.session_state:
	st.session_state.now_positive_leapsecond=False

if "gps_time" not in st.session_state:
	st.session_state.gps_time=st.session_state.utc_time+datetime.timedelta(seconds=st.session_state.leapseconds)

if "utc_day" not in st.session_state:
	st.session_state.utc_day=st.session_state.utc_time.day
if "utc_month" not in st.session_state:	
	st.session_state.utc_month=st.session_state.utc_time.strftime("%B")
if "utc_year" not in st.session_state:	
	st.session_state.utc_year=st.session_state.utc_time.year
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

if "gps_total_seconds" not in st.session_state:
	st.session_state.gps_total_seconds=round((st.session_state.gps_time-gps_beginning_epoch).total_seconds())
if "gps_dayofyear" not in st.session_state:
	st.session_state.gps_dayofyear=int(st.session_state.gps_time.strftime("%j"))
if "gps_week" not in st.session_state:
	st.session_state.gps_week=round(st.session_state.gps_total_seconds//604800)
if "gps_dayofweek" not in st.session_state:
	st.session_state.gps_dayofweek=st.session_state.gps_time.strftime("%w")
if "gps_seconds_per_week" not in st.session_state:
	st.session_state.gps_seconds_per_week=int(st.session_state.gps_total_seconds%604800)
if "gps_seconds_per_day" not in st.session_state:
	st.session_state.gps_seconds_per_day=int(st.session_state.gps_total_seconds%86400)


#columns for subtitle
st.write("&nbsp;")
row1_col1,row1_col2,row1_col3=st.columns([8,1,7])
with row1_col1:
	st.markdown(f'<h2 style="margin-bottom:0rem;margin-top:0rem;text-align: center">UTC Time</h3>', unsafe_allow_html=True)
with row1_col3:
	st.markdown(f'<h2 style="margin-bottom:0rem;margin-top:0rem;text-align: center">GPS Time</h3>', unsafe_allow_html=True)




row2_col1,row2_col2,row2_col3,row2_col4,row2_col5,row2_col6=st.columns([5,6,6,4,5,4])	

with row2_col1:		
	utc_day=st.number_input("Day",key="utc_day",min_value=0,max_value=32,format="%02d",on_change=change_utc_day)
with row2_col2:
	utc_month=st.selectbox("Month", month_list, key="utc_month",on_change=change_utc_month)
with row2_col3:
	utc_year=st.number_input("Year", key="utc_year",min_value=1980, max_value=2030, on_change=change_utc_year)
with row2_col5:
	gps_dayofyear=st.number_input("GPS Day of Year",key="gps_dayofyear",min_value=0,max_value=367,on_change=change_gps_dayofyear)
with row2_col6:
	st.write("&nbsp;")
	placeholder_gpsyear=st.empty()
	if st.session_state.gps_time.year !=st.session_state.utc_time.year:
		placeholder_gpsyear.markdown(f"<p style='color: #f63366'>{st.session_state.gps_time.year}<br></p>", unsafe_allow_html=True) 
	else:
		placeholder_gpsyear.markdown(f"<p>{st.session_state.gps_time.year}<br></p>", unsafe_allow_html=True) 


container = st.container()
container.row3_col1.number_input("Day",key="utc_day",min_value=0,max_value=32,format="%02d",on_change=change_utc_day)




row3_col1,row3_col2,row3_col3,row3_col4,row3_col5,row3_col6,row3_col7=st.columns([5,5,5,4,7,3,1])	
with row3_col1:
	st.subheader("")
	st.write("Set Time:")
with row3_col2:
	st.write("")
	st.button("Now",key="but1",help="settings of your PC clock",on_click=update_utc_now)
with row3_col3:
	st.write("")
	st.button("0:00:00",key="but2",on_click=update_utc_time_zero)
with row3_col5:
	gps_week=st.number_input("GPS Week",key="gps_week",min_value=0,max_value=3000,on_change=change_gps_week)
with row3_col6:
	gps_dayofweek=st.selectbox("Weekday",dayofweek_list,key="gps_dayofweek",help="Sunday = 0",on_change=change_gps_dayofweek)


row4_col1,row4_col2,row4_col3,row4_col4,row4_col5,row4_col6,row4_col7=st.columns([6,6,6,2,3,10,2])
with row4_col1:
	st.number_input("Hours",key="utc_hour",min_value=-1,max_value=24,format="%02d",on_change=change_utc_hour)
with row4_col2:
	st.number_input("Minutes",key="utc_minute",min_value=-1,max_value=60,format="%02d",on_change=change_utc_minute)
with row4_col3:
	st.number_input("Seconds",key="utc_second",min_value=-1,max_value=61,format="%02d",on_change=change_utc_second)
with row4_col6:
	gps_total_seconds=st.number_input("GPS Time (total seconds)",key="gps_total_seconds",min_value=0,on_change=change_gps_total_seconds)


row5_col1,row5_col2,row5_col3,row5_col4,row5_col5,row5_col6,row5_col7=st.columns([9,5,1,2,1,7,7])	
with row5_col1:
	placeholder_localtime=st.empty()
	if st.session_state.show_local_time:
		local_time_now=st.session_state.sess_local_time_now
		placeholder_localtime.write(f"Local Time ({utc_difference}) :")
	else:
		placeholder_localtime.write("&nbsp;")
	st.write("Leap Seconds at UTC Time:")	
with row5_col2:
	pl=st.empty()
	if st.session_state.show_local_time:
		pl.write(f"{local_time_now.strftime('%H:%M:%S')}")
	elif st.session_state.now_positive_leapsecond:
		#pl.write(f"Leap second!!!")
		pl.markdown("<small style='color: #f63366'>Leap second !!!<br></small>", unsafe_allow_html=True) 
	else:
		pl.write("&nbsp;")
	st.write(str(st.session_state.leapseconds))
with row5_col6:
	gps_seconds_per_week=st.number_input("Seconds of Week",key="gps_seconds_per_week",min_value=0,max_value=604800,on_change=change_gps_seconds_per_week)
with row5_col7:
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
- **UTC Time**: (Coordinated Universal Time) is the world's time standard. Local times have their appropriate UTC offsets according to timezones.
- **Time Now:**  Local date/time and corresponding UTC time are based on the setting of your PC clock.
- **Leap seconds:**  To keep the UTC time synchronised with the Earth’s rotation, additional leap seconds are added or subtracted from time to time. Leap seconds are applied either on 31-December or 30-June. The last leap second was added on 31-December-2016 23:59:60   https://maia.usno.navy.mil/products/leap-second
- **GPS Time**: The GPS system uses GPS time which was zero on 06-January-1980 00:00:00. GPS time does not include leap seconds and is currently (2022) ahead of UTC time by 18 seconds.
- for problems and suggestions contact: s.engelhard@gmx.net
- last updated in 2022
''')
#---------------------------------#