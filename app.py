import datetime
import streamlit as st
import pytz


def change_timezone():
    st.session_state.selected_timezone_withoffset = st.session_state.selectbox_timezone
    st.session_state.selected_timezone = st.session_state.selected_timezone_withoffset[
        : st.session_state.selected_timezone_withoffset.index(" ")
    ]
    if st.session_state.selected_timezone != "UTC":
        st.session_state.display_time = st.session_state.utc_time.astimezone(
            pytz.timezone(st.session_state.selected_timezone)
        )
        st.session_state.show_local_time = True
    else:
        st.session_state.show_local_time = False
        st.session_state.display_time = st.session_state.utc_time
    update_displaytime()


def change_time_utc_or_local():
    if st.session_state.selected_time == "UTC":
        st.session_state.show_local_time = False
        st.session_state.display_time = st.session_state.utc_time
    else:
        if st.session_state.selected_timezone != "UTC":
            st.session_state.show_local_time = True
            st.session_state.display_time = st.session_state.utc_time.astimezone(
                pytz.timezone(st.session_state.selected_timezone)
            )
    update_displaytime()


def update_displaytime():
    st.session_state.display_day = st.session_state.display_time.day
    st.session_state.display_month = st.session_state.display_time.strftime("%B")
    st.session_state.display_year = st.session_state.display_time.year
    st.session_state.display_hour = st.session_state.display_time.hour
    st.session_state.display_minute = st.session_state.display_time.minute
    if not st.session_state.now_positive_leapsecond:
        st.session_state.utc_second = st.session_state.utc_time.second


def update_display_time_now():
    st.session_state.utc_time = datetime.datetime.now(pytz.utc).replace(microsecond=0)
    st.session_state.display_time = st.session_state.utc_time.astimezone(
        pytz.timezone(st.session_state.selected_timezone)
    )
    update_displaytime_and_to_gps()


def update_display_time_zero():
    st.session_state.display_time = st.session_state.display_time.replace(
        minute=00, hour=00, second=00
    )
    st.session_state.utc_time = st.session_state.display_time.astimezone(pytz.utc)
    update_displaytime_and_to_gps()


def change_display_day():
    st.session_state.now_positive_leapsecond = False
    beginning_of_month_display_day = st.session_state.display_time.replace(day=1)
    daysofmonth_timedelta = datetime.timedelta(
        days=st.session_state.display_day - beginning_of_month_display_day.day
    )
    st.session_state.display_time = (
        beginning_of_month_display_day + daysofmonth_timedelta
    )
    st.session_state.utc_time = st.session_state.display_time.astimezone(pytz.utc)
    update_displaytime_and_to_gps()


def change_display_month():
    st.session_state.now_positive_leapsecond = False
    dayerror = True
    oneday_timedelta = datetime.timedelta(days=1)
    while dayerror:
        try:
            st.session_state.display_time = st.session_state.display_time.replace(
                month=month_list.index(st.session_state.display_month) + 1
            )
            dayerror = False
        except:
            st.session_state.display_time = (
                st.session_state.display_time - oneday_timedelta
            )
    st.session_state.utc_time = st.session_state.display_time.astimezone(pytz.utc)
    update_displaytime_and_to_gps()


def change_display_year():
    st.session_state.now_positive_leapsecond = False
    dayerror = True
    oneday_timedelta = datetime.timedelta(days=1)
    while dayerror:
        try:
            st.session_state.display_time = st.session_state.display_time.replace(
                year=st.session_state.display_year
            )
            dayerror = False
        except:
            st.session_state.display_time = (
                st.session_state.display_time - oneday_timedelta
            )
    st.session_state.utc_time = st.session_state.display_time.astimezone(pytz.utc)
    update_displaytime_and_to_gps()


def change_display_hour():
    st.session_state.now_positive_leapsecond = False
    beginning_of_day_display_hour = st.session_state.display_time.replace(hour=00)
    hoursofday_timedelta = datetime.timedelta(
        hours=st.session_state.display_hour - beginning_of_day_display_hour.hour
    )
    st.session_state.display_time = beginning_of_day_display_hour + hoursofday_timedelta
    st.session_state.utc_time = st.session_state.display_time.astimezone(pytz.utc)
    update_displaytime_and_to_gps()


def change_display_minute():
    st.session_state.now_positive_leapsecond = False
    beginning_of_hour_display_minute = st.session_state.display_time.replace(minute=00)
    minutesofhour_timedelta = datetime.timedelta(
        minutes=st.session_state.display_minute
        - beginning_of_hour_display_minute.minute
    )
    st.session_state.display_time = (
        beginning_of_hour_display_minute + minutesofhour_timedelta
    )
    st.session_state.utc_time = st.session_state.display_time.astimezone(pytz.utc)
    update_displaytime_and_to_gps()


def change_utc_second():
    st.session_state.now_positive_leapsecond = False
    beginning_of_minute_utc_second = st.session_state.utc_time.replace(
        second=00
    )  # utc datetime beginning of minute
    beginning_of_utc_minute_leap_seconds = calc_leapseconds_from_utctime(
        beginning_of_minute_utc_second
    )  # leapseconds at beginning of minute
    beginning_of_minute_gps_time = beginning_of_minute_utc_second + datetime.timedelta(
        seconds=beginning_of_utc_minute_leap_seconds
    )
    secondsofminute_timedelta = datetime.timedelta(
        seconds=st.session_state.utc_second
    )  # utc seconds entered
    st.session_state.gps_time = beginning_of_minute_gps_time + secondsofminute_timedelta
    st.session_state.gps_total_seconds = round(
        (st.session_state.gps_time - gps_beginning_epoch).total_seconds()
    )
    st.session_state.leapseconds = calc_leapseconds_from_gpstime(
        st.session_state.gps_time
    )
    st.session_state.utc_time = st.session_state.gps_time - datetime.timedelta(
        seconds=st.session_state.leapseconds
    )
    st.session_state.display_time = st.session_state.utc_time.astimezone(
        pytz.timezone(st.session_state.selected_timezone)
    )
    if st.session_state.gps_total_seconds in positive_leapseconds_list:  ###leapsecond
        st.session_state.now_positive_leapsecond = True
        # function update_utc_and_to_gps is not called because in this case st.session_state.utc_seconds needs to stay at 60 and differs from utc_time
        if st.session_state.utc_second == -1:
            st.session_state.utc_second = 60
        st.session_state.display_day = st.session_state.display_time.day
        st.session_state.display_month = st.session_state.display_time.strftime("%B")
        st.session_state.display_year = st.session_state.display_time.year
        st.session_state.display_hour = st.session_state.display_time.hour
        st.session_state.display_minute = st.session_state.display_time.minute
        st.session_state.gps_dayofyear = int(st.session_state.gps_time.strftime("%j"))
        st.session_state.gps_week = st.session_state.gps_total_seconds // 604800
        st.session_state.gps_dayofweek = st.session_state.gps_time.strftime("%w")
        st.session_state.gps_seconds_per_week = int(
            st.session_state.gps_total_seconds % 604800
        )
        st.session_state.gps_seconds_per_day = int(
            st.session_state.gps_total_seconds % 86400
        )
        # st.session_state.selectbox_timezone=st.session_state.selected_timezone_withoffset
    else:
        st.session_state.now_positive_leapsecond = False
        update_displaytime_and_to_gps()


def update_displaytime_and_to_gps():
    if st.session_state.utc_time < gps_beginning_epoch:
        row0_col2.error("GPS Time begins on 06-January-1980", icon="⚠️")
        st.session_state.utc_time = gps_beginning_epoch
        st.session_state.display_time = st.session_state.utc_time.astimezone(
            pytz.timezone(st.session_state.selected_timezone)
        )
    elif st.session_state.utc_time > datetime_limit:
        row0_col2.error("Date limit currently set to 31-Dec-2030", icon="⚠️")
        st.session_state.utc_time = datetime_limit
        st.session_state.display_time = st.session_state.utc_time.astimezone(
            pytz.timezone(st.session_state.selected_timezone)
        )
    st.session_state.display_day = st.session_state.display_time.day
    st.session_state.display_month = st.session_state.display_time.strftime("%B")
    st.session_state.display_year = st.session_state.display_time.year
    st.session_state.display_hour = st.session_state.display_time.hour
    st.session_state.display_minute = st.session_state.display_time.minute
    st.session_state.utc_second = st.session_state.utc_time.second
    st.session_state.leapseconds = calc_leapseconds_from_utctime(
        st.session_state.utc_time
    )
    st.session_state.gps_time = st.session_state.utc_time + datetime.timedelta(
        seconds=st.session_state.leapseconds
    )
    st.session_state.gps_total_seconds = round(
        (st.session_state.gps_time - gps_beginning_epoch).total_seconds()
    )
    st.session_state.gps_dayofyear = int(st.session_state.gps_time.strftime("%j"))
    st.session_state.gps_year = st.session_state.gps_time.year
    st.session_state.gps_week = st.session_state.gps_total_seconds // 604800
    st.session_state.gps_dayofweek = st.session_state.gps_time.strftime("%w")
    st.session_state.gps_seconds_per_week = int(
        st.session_state.gps_total_seconds % 604800
    )
    st.session_state.gps_seconds_per_day = int(
        st.session_state.gps_total_seconds % 86400
    )


def update_gps_and_to_utc():
    if st.session_state.gps_time < gps_beginning_epoch:
        row0_col2.error("GPS Time begins on 06-January-1980", icon="⚠️")
        st.session_state.gps_time = gps_beginning_epoch
    elif (
        st.session_state.gps_time
        - datetime.timedelta(
            seconds=calc_leapseconds_from_gpstime(st.session_state.gps_time)
        )
    ) > datetime_limit:
        row0_col2.error("Date limit currently set to 31-Dec-2030", icon="⚠️")
        st.session_state.gps_time = datetime_limit + datetime.timedelta(
            seconds=calc_leapseconds_from_gpstime(st.session_state.gps_time)
        )
    st.session_state.gps_total_seconds = round(
        (st.session_state.gps_time - gps_beginning_epoch).total_seconds()
    )
    st.session_state.gps_dayofyear = int(st.session_state.gps_time.strftime("%j"))
    st.session_state.gps_year = st.session_state.gps_time.year
    st.session_state.gps_week = round(st.session_state.gps_total_seconds // 604800)
    st.session_state.gps_dayofweek = st.session_state.gps_time.strftime("%w")
    st.session_state.gps_seconds_per_week = int(
        st.session_state.gps_total_seconds % 604800
    )
    st.session_state.gps_seconds_per_day = int(
        st.session_state.gps_total_seconds % 86400
    )
    st.session_state.leapseconds = calc_leapseconds_from_gpstime(
        st.session_state.gps_time
    )
    st.session_state.utc_time = st.session_state.gps_time - datetime.timedelta(
        seconds=st.session_state.leapseconds
    )
    st.session_state.display_time = st.session_state.utc_time.astimezone(
        pytz.timezone(st.session_state.selected_timezone)
    )
    st.session_state.display_day = st.session_state.display_time.day
    st.session_state.display_month = st.session_state.display_time.strftime("%B")
    st.session_state.display_year = st.session_state.display_time.year
    st.session_state.display_hour = st.session_state.display_time.hour
    st.session_state.display_minute = st.session_state.display_time.minute
    if st.session_state.gps_total_seconds in positive_leapseconds_list:
        st.session_state.utc_second = 60
        st.session_state.now_positive_leapsecond = True
    else:
        st.session_state.utc_second = st.session_state.utc_time.second
        st.session_state.now_positive_leapsecond = False


def change_gps_dayofyear():
    beginning_of_year_gps_time = st.session_state.gps_time.replace(day=1, month=1)
    doy_timedelta = datetime.timedelta(days=st.session_state.gps_dayofyear - 1)
    st.session_state.gps_time = beginning_of_year_gps_time + doy_timedelta
    update_gps_and_to_utc()


def change_gps_year():
    beginning_of_year_gps_time = st.session_state.gps_time.replace(
        day=1, month=1, year=st.session_state.gps_year
    )
    doy_timedelta = datetime.timedelta(days=st.session_state.gps_dayofyear - 1)
    st.session_state.gps_time = beginning_of_year_gps_time + doy_timedelta
    # leap years offest the date by 366 days for one year change
    # if the offset is bigger than one year it is corrected
    if beginning_of_year_gps_time.year != st.session_state.gps_time.year:
        doy_timedelta = datetime.timedelta(days=st.session_state.gps_dayofyear - 2)
        st.session_state.gps_time = beginning_of_year_gps_time + doy_timedelta
    update_gps_and_to_utc()


def change_gps_week():
    gps_weeks_timedelta = datetime.timedelta(seconds=st.session_state.gps_week * 604800)
    gps_seconds_per_week_timedelta = datetime.timedelta(
        seconds=st.session_state.gps_seconds_per_week
    )
    st.session_state.gps_time = (
        gps_beginning_epoch + gps_weeks_timedelta + gps_seconds_per_week_timedelta
    )
    update_gps_and_to_utc()


def change_gps_dayofweek():
    gps_weeks_timedelta = datetime.timedelta(seconds=st.session_state.gps_week * 604800)
    gps_days_of_week_timedelta = datetime.timedelta(
        seconds=int(st.session_state.gps_dayofweek) * 86400
    )
    gps_seconds_per_day_timedelta = datetime.timedelta(
        seconds=st.session_state.gps_seconds_per_day
    )
    st.session_state.gps_time = (
        gps_beginning_epoch
        + gps_weeks_timedelta
        + gps_days_of_week_timedelta
        + gps_seconds_per_day_timedelta
    )
    update_gps_and_to_utc()


def change_gps_total_seconds():
    st.session_state.gps_time = gps_beginning_epoch + datetime.timedelta(
        seconds=st.session_state.gps_total_seconds
    )
    update_gps_and_to_utc()


def change_gps_seconds_per_week():
    gps_datetime_week_zero = gps_beginning_epoch + datetime.timedelta(
        seconds=st.session_state.gps_week * 604800
    )
    gps_seconds_per_week_timedelta = datetime.timedelta(
        seconds=st.session_state.gps_seconds_per_week
    )
    st.session_state.gps_time = gps_datetime_week_zero + gps_seconds_per_week_timedelta
    update_gps_and_to_utc()


def change_gps_seconds_per_day():
    gps_datetime_zero = st.session_state.gps_time.replace(hour=00, minute=00, second=00)
    gps_seconds_per_day_timedelta = datetime.timedelta(
        seconds=st.session_state.gps_seconds_per_day
    )
    st.session_state.gps_time = gps_datetime_zero + gps_seconds_per_day_timedelta
    update_gps_and_to_utc()


def calc_leapseconds_from_utctime(utc_datetime):
    lp = 0
    totalseconds = round((utc_datetime - gps_beginning_epoch).total_seconds())
    for i in positive_leapseconds_list:
        if (totalseconds + positive_leapseconds_list.index(i)) >= i:
            lp += 1
    return lp


def calc_leapseconds_from_gpstime(gps_datetime):
    lp = 0
    totalseconds = (gps_datetime - gps_beginning_epoch).total_seconds()
    for i in positive_leapseconds_list:
        if totalseconds >= i:
            lp += 1
    return lp


def update_dict_timezones_with_offsets():
    list_of_timezone_dicts = []
    for tzname in common_timezones_list:
        dict1 = {}
        # each timezone gets added to dictionary together with offset
        dict1["tzname"] = tzname
        offset_timedelta = st.session_state.utc_time.astimezone(
            pytz.timezone(tzname)
        ).utcoffset()
        offset_float = offset_timedelta.total_seconds() / 60 / 60  # float in hours
        dict1["offset_float"] = offset_float
        offset_hours = int(offset_float)
        offset_minutes = abs(int((offset_float % 1) * 60))
        offset_string = (
            "{:+02d}".format(offset_hours) + ":" + "{:02d}".format(offset_minutes)
        )
        dict1["offset_string"] = offset_string
        dict1["tzname_with_offset"] = tzname + " - UTC" + offset_string
        list_of_timezone_dicts.append(dict1)
    return list_of_timezone_dicts


# -----Page Configuration
st.set_page_config(
    page_title="GPS Time Converter",
    page_icon="🛰️",  # satellite emoji
    initial_sidebar_state="collapsed",
)

# ----menu button invisible
st.markdown(
    """ <style>#MainMenu {visibility: hidden;}footer {visibility: hidden;}</style> """,
    unsafe_allow_html=True,
)


# setting variables
positive_leapseconds_list = [
    46828800,
    78364801,
    109900802,
    173059203,
    252028804,
    315187205,
    346723206,
    393984007,
    425520008,
    457056009,
    504489610,
    551750411,
    599184012,
    820108813,
    914803214,
    1025136015,
    1119744016,
    1167264017,
]
month_list = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]
dayofweek_list = ["0", "1", "2", "3", "4", "5", "6"]
gps_beginning_epoch = datetime.datetime.strptime(
    "1980-01-06 00:00:00", "%Y-%m-%d %H:%M:%S"
).replace(tzinfo=datetime.timezone.utc)
datetime_limit = datetime.datetime.strptime(
    "2030-12-31 23:59:59", "%Y-%m-%d %H:%M:%S"
).replace(tzinfo=datetime.timezone.utc)
# pytz list of all common timezones, ca. 439:
common_timezones_list = pytz.common_timezones


# setting session states
if "utc_time" not in st.session_state:
    st.session_state.utc_time = datetime.datetime.now(pytz.utc).replace(microsecond=0)
if "display_time" not in st.session_state:
    st.session_state.display_time = st.session_state.utc_time
if "selected_time" not in st.session_state:
    st.session_state.selected_time = "UTC"
if "selected_timezone" not in st.session_state:
    st.session_state.selected_timezone = "UTC"
if "selected_timezone_withoffset" not in st.session_state:
    st.session_state.selected_timezone_withoffset = "UTC - UTC+0:00"
if "show_local_time" not in st.session_state:
    st.session_state.show_local_time = False
if "leapseconds" not in st.session_state:
    st.session_state.leapseconds = calc_leapseconds_from_utctime(
        st.session_state.utc_time
    )
if "now_positive_leapsecond" not in st.session_state:
    st.session_state.now_positive_leapsecond = False
if "gps_time" not in st.session_state:
    st.session_state.gps_time = st.session_state.utc_time + datetime.timedelta(
        seconds=st.session_state.leapseconds
    )
if "display_day" not in st.session_state:
    st.session_state.display_day = st.session_state.display_time.day
if "display_month" not in st.session_state:
    st.session_state.display_month = st.session_state.display_time.strftime("%B")
if "display_year" not in st.session_state:
    st.session_state.display_year = st.session_state.display_time.year
if "display_hour" not in st.session_state:
    st.session_state.display_hour = st.session_state.display_time.hour
if "display_minute" not in st.session_state:
    st.session_state.display_minute = st.session_state.display_time.minute
if "utc_second" not in st.session_state:
    st.session_state.utc_second = st.session_state.utc_time.second
if "gps_total_seconds" not in st.session_state:
    st.session_state.gps_total_seconds = round(
        (st.session_state.gps_time - gps_beginning_epoch).total_seconds()
    )
if "gps_dayofyear" not in st.session_state:
    st.session_state.gps_dayofyear = int(st.session_state.gps_time.strftime("%j"))
if "gps_year" not in st.session_state:
    st.session_state.gps_year = st.session_state.gps_time.year
if "gps_week" not in st.session_state:
    st.session_state.gps_week = round(st.session_state.gps_total_seconds // 604800)
if "gps_dayofweek" not in st.session_state:
    st.session_state.gps_dayofweek = st.session_state.gps_time.strftime("%w")
if "gps_seconds_per_week" not in st.session_state:
    st.session_state.gps_seconds_per_week = int(
        st.session_state.gps_total_seconds % 604800
    )
if "gps_seconds_per_day" not in st.session_state:
    st.session_state.gps_seconds_per_day = int(
        st.session_state.gps_total_seconds % 86400
    )


######################################################################

# ---- Title and Description
st.markdown(
    '<h1 style="margin-bottom:0rem;margin-top:-4rem;text-align: center">GPS Time Converter</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    '<h5 style="color:grey;margin-bottom:0rem;margin-top:-1rem;text-align: center">Convert between UTC/Local Time and GPS Time</h5>',
    unsafe_allow_html=True,
)
# st.title('GPS Time Converter')
# st.text('Convert between UTC/Local Time and GPS Time')


row0_col1, row0_col2, row0_col3 = st.columns([6, 10, 5])
with row0_col1:
    radiobuttontime = st.radio(
        "Convert to/from:",
        ("UTC", "Local Time"),
        key="selected_time",
        on_change=change_time_utc_or_local,
        horizontal=True,
    )
    if radiobuttontime == "UTC":
        st.session_state.show_local_time = False
    st.write("&nbsp;")  # space in order following rows don't move
with row0_col3:
    if radiobuttontime == "Local Time":
        sort_option = st.radio(
            "Sort Timezone List", ("by Name", "by UTC offset"), key="sort_option"
        )
with row0_col2:
    if radiobuttontime == "Local Time":
        ######this must be done again for every time change!!!
        list_of_timezone_dicts = update_dict_timezones_with_offsets()
        timezone_list = [
            d["tzname_with_offset"] for d in list_of_timezone_dicts
        ]  # list for display in selectbox sorted by name
        # list of dictionaries is sorted by offset_float:
        list_of_timezone_dicts_sorted_offset = sorted(
            list_of_timezone_dicts, key=lambda d: d["offset_float"]
        )
        timezone_list_sorted_offset = [
            d["tzname_with_offset"] for d in list_of_timezone_dicts_sorted_offset
        ]  # list for display in selectbox sorted by offset
        filtered_list = list(
            filter(
                lambda list_of_timezone_dicts: list_of_timezone_dicts["tzname"]
                == st.session_state.selected_timezone,
                list_of_timezone_dicts,
            )
        )
        st.session_state.selected_timezone_withoffset = filtered_list[0][
            "tzname_with_offset"
        ]
        st.session_state.selectbox_timezone = (
            st.session_state.selected_timezone_withoffset
        )
        placeholder_selectbox_timezone = st.empty()
        if sort_option == "by Name":
            placeholder_selectbox_timezone.selectbox(
                "Select Timezone:",
                timezone_list,
                key="selectbox_timezone",
                on_change=change_timezone,
            )
        else:
            placeholder_selectbox_timezone.selectbox(
                "Select Timezone:",
                timezone_list_sorted_offset,
                key="selectbox_timezone",
                on_change=change_timezone,
            )

col1, col2 = st.columns([11, 8],gap="medium")

with col1:
    col1_row1_c1, col1_row1_c2 = st.columns([5, 4])
    with col1_row1_c1:
        placeholder_title = st.empty()
        if not st.session_state.show_local_time:
            placeholder_title.markdown(
                f'<h2 style="margin-bottom:0rem;margin-top:-1rem;text-align: center">UTC</h2>',
                unsafe_allow_html=True,
            )
        else:
            placeholder_title.markdown(
                f'<h2 style="margin-bottom:0rem;margin-top:-1rem;text-align: center">Local Time</h2>',
                unsafe_allow_html=True,
            )
    with col1_row1_c2:
        placeholder_showselectedoffset = st.empty()
        if st.session_state.show_local_time:
            i = st.session_state.selected_timezone_withoffset.index(" ")
            text = st.session_state.selected_timezone_withoffset[i + 3 :]
            placeholder_showselectedoffset.markdown(
                f'<h4 style="color: blue;margin-bottom:0rem;margin-top:-0.2rem;text-align: center">'
                + text
                + "</h4>",
                unsafe_allow_html=True,
            )
    col1_row2_c1, col1_row2_c2, col1_row2_c3 = st.columns([5, 6, 6])
    with col1_row2_c1:
        st.number_input(
            "Day",
            key="display_day",
            min_value=0,
            max_value=32,
            format="%02d",
            on_change=change_display_day,
        )
    with col1_row2_c2:
        st.selectbox(
            "Month", month_list, key="display_month", on_change=change_display_month
        )
    with col1_row2_c3:
        st.number_input(
            "Year",
            key="display_year",
            min_value=1980,
            max_value=2030,
            on_change=change_display_year,
        )
    col1_row3_c1, col1_row3_c2, col1_row3_c3 = st.columns(3)
    with col1_row3_c1:
        st.text(" ")
        st.text(" ")
        st.write("Set Time:")
    with col1_row3_c2:
        st.text(" ")
        st.text(" ")
        st.button(
            "Now",
            key="but1",
            help="Set time to current time",
            on_click=update_display_time_now,
        )
    with col1_row3_c3:
        st.text(" ")
        st.text(" ")
        st.button(
            "0:00:00",
            key="but2",
            help="Set time to 0:00:00",
            on_click=update_display_time_zero,
        )
    col1_row4_c1, col1_row4_c2, col1_row4_c3 = st.columns(3)
    with col1_row4_c1:
        st.number_input(
            "Hours",
            key="display_hour",
            min_value=-1,
            max_value=24,
            format="%02d",
            on_change=change_display_hour,
        )
    with col1_row4_c2:
        st.number_input(
            "Minutes",
            key="display_minute",
            min_value=-1,
            max_value=60,
            format="%02d",
            on_change=change_display_minute,
        )
    with col1_row4_c3:
        st.number_input(
            "Seconds",
            key="utc_second",
            min_value=-1,
            max_value=61,
            format="%02d",
            on_change=change_utc_second,
        )
    col1_row5_c1, col1_row5_c2, col1_row5_c3 = st.columns([9, 2, 5])
    with col1_row5_c1:
        st.write("Leap Seconds at this time:")
    with col1_row5_c2:
        st.write(str(st.session_state.leapseconds))
    with col1_row5_c3:
        placeholder_now_leapsecond = st.empty()
        if st.session_state.now_positive_leapsecond:
            placeholder_now_leapsecond.markdown(
                "<small style='color: #f63366'>Leap second!!!<br></small>",
                unsafe_allow_html=True,
            )
        else:
            placeholder_now_leapsecond.write("")

with col2:
    st.markdown(
        f'<h2 style="margin-bottom:0rem;margin-top:-1rem;text-align: center">GPS Time</h2>',
        unsafe_allow_html=True,
    )
    placeholder_col2error = st.empty()
    col2_row2_c1, col2_row2_c2, col2_row2_c3, col2_row2_c4 = st.columns([1,10,10,1])
    with col2_row2_c2:
        st.number_input(
            "GPS Day of Year",
            key="gps_dayofyear",
            min_value=0,
            max_value=367,
            on_change=change_gps_dayofyear,
        )
    with col2_row2_c3:
        st.number_input(
            "GPS Year",
            key="gps_year",
            min_value=1980,
            max_value=2031,
            on_change=change_gps_year,
        )
    col2_row3_c1, col2_row3_c2, col2_row3_c3, col2_row3_c4 = st.columns([1, 6, 4, 1])
    with col2_row3_c2:
        st.number_input(
            "GPS Week",
            key="gps_week",
            min_value=0,
            max_value=3000,
            on_change=change_gps_week,
        )
    with col2_row3_c3:
        st.selectbox(
            "Weekday",
            dayofweek_list,
            key="gps_dayofweek",
            help="Sunday = 0",
            on_change=change_gps_dayofweek,
        )
    col2_row4_c1, col2_row4_c2, col2_row4_c3 = st.columns([1,4,1])
    with col2_row4_c2:
        st.number_input(
            "GPS Time (total seconds)",
            key="gps_total_seconds",
            min_value=0,
            on_change=change_gps_total_seconds,
        )
    col2_row5_c1, col2_row5_c2 = st.columns(2)
    with col2_row5_c1:
        gps_seconds_per_week = st.number_input(
            "Seconds of Week",
            key="gps_seconds_per_week",
            min_value=0,
            max_value=604800,
            on_change=change_gps_seconds_per_week,
        )
    with col2_row5_c2:
        gps_seconds_per_day = st.number_input(
            "Seconds of Day",
            key="gps_seconds_per_day",
            min_value=0,
            max_value=86400,
            on_change=change_gps_seconds_per_day,
        )


######################################################################
# ---------------------------------#
st.write("")
expander_bar = st.expander("About this app")
expander_bar.markdown(
    """
- **UTC**: UTC (Coordinated Universal Time) is the primary time standard by which the world regulates clocks and time. Local times have their appropriate UTC offsets according to timezones.
- **Local Time**: The Local time can be shown if the correct timezone is selected. Timezones can be selected from a list of all common and currently used time zones which are derived from the Python module **pytz** - https://pypi.org/project/pytz/
- **Leap seconds:**  To keep UTC synchronised with the Earth’s rotation, additional leap seconds are added or subtracted from time to time. Leap seconds are applied either on 31-December or 30-June. The last leap second was added on 31-December-2016 23:59:60.   https://maia.usno.navy.mil/products/leap-second
- **GPS Time**: The GPS system uses GPS time which was zero on 06-January-1980 00:00:00. GPS time does not include leap seconds and is currently (2023) ahead of UTC by 18 seconds.
- for problems and suggestions contact: s.engelhard@gmx.net
- last updated in 2023
"""
)
# ---------------------------------#
