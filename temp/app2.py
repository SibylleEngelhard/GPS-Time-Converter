import streamlit as st
import datetime
import time


def GPSseconds_to_GPStime2(row):
    ###function working for series = row
    datetimeformat = "%Y-%m-%d %H:%M:%S"
    beginning_epoch = datetime.datetime.strptime("1980-01-06 00:00:00",datetimeformat)
    elapsed = datetime.timedelta(days=(row["GPS_Week"]*7),seconds=(row["GPS_Seconds"]))
    gpstime=beginning_epoch + elapsed
    return gpstime   

def GPSseconds_to_GPStime(gpsweek,gpsseconds):
    datetimeformat = "%Y-%m-%d %H:%M:%S"
    beginning_epoch = datetime.datetime.strptime("1980-01-06 00:00:00",datetimeformat)
    elapsed = datetime.timedelta(days=(gpsweek*7),seconds=(gpsseconds))
    gpstime=beginning_epoch + elapsed
    return gpstime


def update_utc_now():
	utc_time_now=datetime.datetime.utcnow()
	st.session_state.utc_day=utc_time_now.day
	st.session_state.utc_month=utc_time_now.strftime("%B")
	st.session_state.utc_year=utc_time_now.strftime("%Y")
	st.session_state.utc_hour=utc_time_now.hour
	st.session_state.utc_minute=utc_time_now.minute
	st.session_state.utc_second=utc_time_now.second
	st.session_state.sess_local_time_now=datetime.datetime.now()
	st.session_state.show_local_time=True
	utc_to_gps()

def update_utc_time_zero():
	#utc_time_now=datetime.datetime.utcnow()
	#st.session_state.utc_day=utc_time_now.day
	#st.session_state.utc_month=utc_time_now.strftime("%B")
	#st.session_state.utc_year=utc_time_now.strftime("%Y")
	zerotimeformat = "%H:%M:%S"
	st.session_state.utc_hour=datetime.datetime.strptime("00:00:00",zerotimeformat).hour
	st.session_state.utc_minute=datetime.datetime.strptime("00:00:00",zerotimeformat).minute
	st.session_state.utc_second=datetime.datetime.strptime("00:00:00",zerotimeformat).second
	st.session_state.show_local_time=False
	utc_to_gps()

def utc_to_gps():
	
	utc_datetime_string=str(st.session_state.utc_day)+" "+st.session_state.utc_month+" "+st.session_state.utc_year+" "+str(st.session_state.utc_hour)+" "+str(st.session_state.utc_minute)+" "+str(st.session_state.utc_second)
	utc_datetime=datetime.datetime.strptime(utc_datetime_string, "%d %B %Y %H %M %S")
	gps_datetime=utc_datetime+leapseconds_timedelta
	gps_datetime_inseconds=(gps_datetime-gps_beginning_epoch).total_seconds()
		
	st.session_state.gps_dayofyear=int(gps_datetime.strftime("%j"))
	st.session_state.gps_week=int(gps_datetime_inseconds/604800)
	st.session_state.gps_dayofweek=gps_datetime.strftime("%w")
	st.session_state.gps_total_seconds=gps_datetime_inseconds
	st.session_state.gps_seconds_per_week=int(gps_datetime_inseconds%(86400*7))
	st.session_state.gps_seconds_per_day=int(gps_datetime_inseconds%86400)

def gps_to_utc():
	
	gps_datetime_inseconds=st.session_state.gps_total_seconds
	utc_datetime_inseconds=gps_datetime_inseconds-leapseconds
	temp_timedelta = datetime.timedelta(seconds=utc_datetime_inseconds)
	utc_datetime=gps_beginning_epoch+temp_timedelta
	#st.write(utc_datetime)
	st.session_state.utc_day=utc_datetime.day
	st.session_state.utc_month=utc_datetime.strftime("%B")
	st.session_state.utc_year=utc_datetime.strftime("%Y")
	st.session_state.utc_hour=utc_datetime.hour
	st.session_state.utc_minute=utc_datetime.minute
	st.session_state.utc_second=utc_datetime.second
	#st.session_state.gps_dayofyear=int(gps_datetime.strftime("%j"))
	#st.session_state.gps_week=int(gps_datetime_inseconds/604800)
	#st.session_state.gps_dayofweek=gps_datetime.strftime("%w")
	#st.session_state.gps_total_seconds=gps_datetime_inseconds
	#st.session_state.gps_seconds_per_week=int(gps_datetime_inseconds%(86400*7))

	#st.session_state.gps_seconds_per_day=int(gps_datetime_inseconds%86400)





leapsecondscont = [46828800, 78364801, 109900802, 173059203, 252028804, 315187205, 346723206, 393984007, 425520008, 457056009, 504489610, 551750411, 599184012, 820108813, 914803214, 1025136015, 1119744016, 1167264017]
month_list=["January","February","March","April","May","June","Juli","August","September","October","November","December"]
year_list=["1980","1981","1982","1983","1984","1985","1986","1987","1988","1988","1989","1990",
"1991","1992","1993","1994","1995","1996","1997","1998","1999","2000",
"2001","2002","2003","2004","2005","2006","2007","2008","2009","2010",
"2011","2012","2013","2014","2015","2016","2017","2018","2019","2020",
"2021","2022","2023","2024","2025","2026","2027","2028","2029","2030"]
dayofweek_list=["0","1","2","3","4","5","6"]
datetimeformat = "%Y-%m-%d %H:%M:%S"
gps_beginning_epoch = datetime.datetime.strptime("1980-01-06 00:00:00",datetimeformat)


utc_time_now=datetime.datetime.utcnow()
local_time_now=datetime.datetime.now()
utc_difference=datetime.timezone(datetime.datetime.now()-datetime.datetime.utcnow())

#utc_year_index=year_list.index(utc_time_now.strftime("%Y"))
#utc_month_index=month_list.index(utc_time_now.strftime("%B"))
####!!!!change with leapsecondsfuction
leapseconds=18
leapseconds_timedelta = datetime.timedelta(seconds=leapseconds)
current_leapseconds=leapseconds

   
gps_time_now=utc_time_now+leapseconds_timedelta
gps_time_now_inseconds=(gps_time_now-gps_beginning_epoch).total_seconds()

#gps_year_index=year_list.index(gps_time_now.strftime("%Y"))
#gps_month_index=month_list.index(gps_time_now.strftime("%B"))

if "utc_day" not in st.session_state:
	st.session_state.utc_day=utc_time_now.day
if "utc_month" not in st.session_state:	
	st.session_state.utc_month=utc_time_now.strftime("%B")
if "utc_year" not in st.session_state:	
	st.session_state.utc_year=utc_time_now.strftime("%Y")
if "utc_hour" not in st.session_state:	
	st.session_state.utc_hour=utc_time_now.hour
if "utc_minute" not in st.session_state:	
	st.session_state.utc_minute=utc_time_now.minute
if "utc_second" not in st.session_state:
	st.session_state.utc_second=utc_time_now.second

if "show_local_time" not in st.session_state:
	st.session_state.show_local_time=True
if "sess_local_time_now" not in st.session_state:
	st.session_state.sess_local_time_now=local_time_now

if "gps_dayofyear" not in st.session_state:
	st.session_state.gps_dayofyear=int(gps_time_now.strftime("%j"))
if "gps_week" not in st.session_state:
	st.session_state.gps_week=int(gps_time_now_inseconds/604800)
if "gps_dayofweek" not in st.session_state:
	st.session_state.gps_dayofweek=gps_time_now.strftime("%w")
if "gps_total_seconds" not in st.session_state:
	st.session_state.gps_total_seconds=gps_time_now_inseconds
if "gps_seconds_per_week" not in st.session_state:
	st.session_state.gps_seconds_per_week=int(gps_time_now_inseconds%(86400*7))
if "gps_seconds_per_day" not in st.session_state:
	st.session_state.gps_seconds_per_day=int(gps_time_now_inseconds%86400)



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







#columns for subtitle
row1_col1,row1_col2=st.columns([6,6])
with row1_col1:
	st.markdown(f'<h3 style="margin-bottom:0rem;margin-top:0rem;text-align: center">UTC Time</h3>', unsafe_allow_html=True)
with row1_col2:
	st.markdown(f'<h3 style="margin-bottom:0rem;margin-top:0rem;text-align: center">GPS Time</h3>', unsafe_allow_html=True)




row2_col1,row2_col2,row2_col3,row2_col4,row2_col5,row2_col6,row2_col7=st.columns([5,6,4,1,5,6,3])	
		
#with row2_col1:		
#	utc_day=st.number_input("Day",key="utc_day",value=utc_time_now.day,min_value=0,max_value=31,format="%02d",on_change=utc_to_gps)
#with row2_col2:
#	utc_month=st.selectbox("Month", month_list, index=utc_month_index, key="utc_month",on_change=utc_to_gps)
#with row2_col3:
#	utc_year=st.selectbox("Year", year_list, index=utc_year_index,key="utc_year",on_change=utc_to_gps)

with row2_col1:		
	utc_day=st.number_input("Day",key="utc_day",min_value=1,max_value=31,format="%02d",on_change=utc_to_gps)
with row2_col2:
	utc_month=st.selectbox("Month", month_list, key="utc_month",on_change=utc_to_gps)
with row2_col3:
	utc_year=st.selectbox("Year", year_list, key="utc_year",on_change=utc_to_gps)

with row2_col5:
	gps_dayofyear=st.number_input("GPS Day of Year",key="gps_dayofyear",min_value=1,max_value=366)
with row2_col6:
	gps_week=st.number_input("GPS Week",key="gps_week",min_value=0,max_value=3000)
with row2_col7:
	gps_dayofweek=st.selectbox("Weekday",dayofweek_list,key="gps_dayofweek",help="Sunday = 0")


row3_col1,row3_col2,row3_col3,row3_col4,row3_col5,row3_col6,row3_col7=st.columns([5,6,4,2,8,2,5])	
		
with row3_col1:
	st.write("")
	st.button("Now",key="but1",on_click=update_utc_now)
with row3_col2:
	st.write("")
	st.button("0:00:00",key="but2",on_click=update_utc_time_zero)
with row3_col5:
		st.write("")
		st.write("Leap Seconds at Date:")
		#temp=st.number_input("Leap Seconds at date",key="gps_leapseconds",min_value=0,max_value=20)
with row3_col6:
		st.write("")
		st.write(str(current_leapseconds))
		#temp=st.number_input("Leap Seconds at date",key="gps_leapseconds",min_value=0,max_value=20)


row4_col1,row4_col2,row4_col3,row4_col4,row4_col5,row4_col6,row4_col7=st.columns([5,5,5,2,10,2,3])

with row4_col1:
	st.number_input("Hours",key="utc_hour",min_value=0,max_value=23,format="%02d",on_change=utc_to_gps)
with row4_col2:
	st.number_input("Minutes",key="utc_minute",min_value=0,max_value=59,format="%02d",on_change=utc_to_gps)
with row4_col3:
	st.number_input("Seconds",key="utc_second",min_value=0,max_value=59,format="%02d",on_change=utc_to_gps)

with row4_col5:
	gps_total_seconds=st.number_input("GPS Time (total seconds)",key="gps_total_seconds",min_value=0,on_change=gps_to_utc)


row5_col1,row5_col2,row5_col3,row5_col4,row5_col5,row5_col6,row5_col7=st.columns([13,1,1,2,7,7,1])	
with row5_col1:
	if st.session_state.show_local_time:
		local_time_now=st.session_state.sess_local_time_now
		st.write(f"Local Time ({utc_difference}) :  {local_time_now.strftime('%H:%M:%S')}")


with row5_col5:
	gps_seconds_per_week=st.number_input("Seconds of Week",key="gps_seconds_per_week",min_value=0,max_value=604800)
with row5_col6:
	gps_seconds_per_day=st.number_input("Seconds of Day",key="gps_seconds_per_day",min_value=0,max_value=86400)


#row6_col1,row6_col2,row6_col3,row6_col4,row6_col5,row6_col6,row6_col7=st.columns([8,5,2,2,5,5,5])	



st.markdown("---")


