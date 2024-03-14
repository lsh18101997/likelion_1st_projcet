import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_csv("Bank Target Marketing Dataset.csv")

# col1 data
tab_name = []
tab_all = []
cnt1 = 1
other = ['age', 'balance', 'day', 'duration', 'campaign', 'pdays', 'previous']
for _ in df.columns:
    tab_name.append(_)
    tab_all.append(f'tab{cnt1}')
    cnt1 += 1
    
# sidebox
add_selectbox = st.sidebar.selectbox(
    "Menu",
    ("Data Dashboard", "customized service", "etc")
)

# container
col1, col2, col3 = st.columns([1,2,1])

with col1:
    st.subheader("A narrow column with a chart")
    st.write("빈공간")

with col2:
    cnt2 = 0
    col2.subheader("Distribution of customers according to label values")
    tab_all = st.tabs(tab_name)
    for tab in tab_all:
        if tab_name[cnt2] in other:
            tab.write("빈공간")
        else:
            fig = px.pie(df, names = tab_name[cnt2], title= f'The Distribution of {tab_name[cnt2]} status')
            fig.update_layout(width=300, height=300)
            tab.plotly_chart(fig)
        cnt2 += 1
      
with col3:
    st.subheader("A narrow column with the data")
    st.write("빈공간")

    







