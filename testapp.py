import streamlit as st
import datetime
import time
import pytz

#-----Page Configuration
st.set_page_config(page_title="Test",
    page_icon='🛰️',#satellite emoji
    initial_sidebar_state="collapsed")

st.title("Title")
row1_col1,row1_col2,row1_col3=st.columns([6,1,5])





row2_col1,row2_col2,row2_col3,row2_col4,row2_col5,row2_col6=st.columns([2,2,2,1,3,2])


row1_col1.header("Column 1")

row2_col1.write("Column 1A")
row2_col2.write("Column 1B")
row2_col3.write("Column 1C")
pl=row1_col2.empty()
pl.header("Column 2")