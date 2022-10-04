def lbs_to_kg():
	st.session_state.kg=st.session_state.lbs/2.2046

def kg_to_lbs():
	st.session_state.lbs=st.session_state.kg*2.2046
#col1,col2=st.columns([2,2])

#"st.session_state object:",st.session_state
col1,buff,col2=st.columns([2,1,2])
with col1:
	pounds=st.number_input("Pounds:",key="lbs",on_change=lbs_to_kg)
	
	date_today=datetime.date.today()
	time_today=datetime.datetime.now()
	d = st.date_input(
	     "Date:",
	     date_today)
	#d2=st.date_input("Date:", date_today, min_value, max_value, key, help, on_change, args, kwargs)
	st.write('Date is:', d)
	t = st.time_input('Time:', time_today)
	st.write('Time is:', t)
with col2:
	kilogram=st.number_input("Kilograms:",key="kg",on_change=kg_to_lbs)

now = datetime.datetime.now()
st.write("Current Time =", now)
with st.empty():
	for seconds in range(10):
	while True:
		now = datetime.datetime.now()
		current_time = now.strftime("%H:%M:%S")
		st.write("Current Time =", now)
		time.sleep(1)

for key in st.session_state.keys():
	del st.session_state[key]
st.write(st.session_state)


for the_key in st.session_state.keys():
	st.write(the_key)
for the_values in st.session_state.values():
	st.write(the_values)
for item in st.session_state.items():
	st.write(item)
