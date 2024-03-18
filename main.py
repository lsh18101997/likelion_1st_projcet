import streamlit as st
from pages import *
import time

# 상태 저장
if 'page' not in st.session_state:
    st.session_state['page'] = 'HOME'

# sidebar
with st.sidebar:
    if st.button("HOME", type='primary', use_container_width=True): st.session_state['page']='HOME'
    if st.button("Data Dashboard", use_container_width=True): st.session_state['page']='dashboard'
    if st.button("Campaign Target", use_container_width=True): st.session_state['page']='service'
    empty_maker(6)
    st.image('img/github.png', width=50)
    st.link_button("GitHub", "https://github.com/lsh18101997?tab=repositories",use_container_width=True)

if st.session_state['page']=='HOME':
    home()
elif st.session_state['page']=='dashboard':
    loader(5)
    dashboard()
    time.sleep(2)
    st.toast('Page is ready', icon='👍')

elif st.session_state['page']=='service':
    service()