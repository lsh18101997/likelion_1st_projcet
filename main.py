import pandas as pd
import streamlit as st
import plotly.express as px
import statistics

# 화면 꽉 차게하기
st.set_page_config(layout="wide")

# 데이터 전처리
@st.cache_data
def load_data():
    df = pd.read_csv("Bank Target Marketing Dataset.csv")
    df['age_str'] = df['age'].apply(lambda x : 'yonth' if x <= 40 else 'middle age' if x <= 60 else 'old age')
    df['balance_str'] = df['balance'].apply(lambda x : 'minus' if x <= 0 else '1~5000' if x <= 5000 else 'above 5000')
    df['day_str'] = df['day'].apply(lambda x : '1~10' if x <= 10 else '11~20' if x <= 20 else '21~30')
    df['duration_str'] = df['duration'].apply(lambda x : '0~60' if x <= 60 else '61~600' if x <= 600 else 'above 600')
    df['campaign_str'] = df['campaign'].apply(lambda x : '1' if x <= 1 else '1~5' if x <= 5 else 'above 5')
    df['pdays_str'] = df['pdays'].apply(lambda x : 'less than one month' if x <= 30 else 'one month~one year' if x <= 365 else 'more than one year')
    df['previous_str'] = df['previous'].apply(lambda x : 'none' if x <= 0 else '1~10' if x <= 10 else 'above 10')
    return df
df = load_data()

# col1 data
profitable = df.loc[df['default'] == 'no', ['balance_str']]
profitable_num = len(profitable.loc[profitable['balance_str']=='above 5000', ['balance_str']])
non_profitable = df.loc[df['default'] == 'yes', ['loan']]
non_profitable_num = len(non_profitable.loc[non_profitable['loan']=='yes',['loan']])
non_profitable2 = df.loc[df['age_str'] == 'old age', ['balance_str']]
non_profitable_num2 = len(non_profitable2.loc[non_profitable2['balance_str']=='minus', ['balance_str']])


# col2 and col3 data
tab_name = []
tab_all = []
cnt1 = 1
other = ['age', 'balance', 'day', 'duration', 'campaign', 'pdays', 'previous']
for _ in df.columns[:17]:
    tab_name.append(_)
    tab_all.append(f'tab{cnt1}')
    cnt1 += 1

# col3 data
# total customer
total_customer = len(df)
# campaign열 데이터 전처리 => unknown과 other을 제외하기
campaign = df.loc[df['poutcome'] != 'unknown']
campaign = campaign.loc[campaign['poutcome'] != 'other']


# sidebox
add_selectbox = st.sidebar.selectbox(
    "Menu",
    ("Data Dashboard", "customized service", "About project")
)

# container
col1, col2, col3 = st.columns([0.2,0.5,0.3])

with col1:
    st.subheader("A profitable group")
    st.metric(label="No Credit Default & Enough Balane(above 5000)", value=profitable_num)
    st.subheader("A non-profitable group")
    st.metric(label="Credit Default & Loan", value=non_profitable_num)
    st.metric(label="Old Age & Minus Balane", value=non_profitable_num2)
    

with col2:
    cnt2 = 0
    col2.subheader("Distribution of customers according to label values")
    tab_all = st.tabs(tab_name)
    for tab in tab_all:
        if tab_name[cnt2] in other:
            fig = px.pie(df, names = f'{tab_name[cnt2]}_str', title= f'The Distribution of {tab_name[cnt2]} status')
            fig.update_layout(width=400, height=400)
            tab.plotly_chart(fig)
        else:
            fig = px.pie(df, names = tab_name[cnt2], title= f'The Distribution of {tab_name[cnt2]} status')
            fig.update_layout(width=400, height=400)
            tab.plotly_chart(fig)
        cnt2 += 1
      
with col3:
    st.subheader("Total Customer")
    st.metric(label="Number of Total Customer", value=total_customer)
    st.subheader("Number of Compain Successes according to label values")
    tab_all = st.tabs(tab_name)
    cnt3 = 0
    for tab in tab_all:
        if tab_name[cnt3] in other:
            two = campaign[[f'{tab_name[cnt3]}_str','poutcome']]
            three = two.loc[two['poutcome'] == 'success'].groupby(f'{tab_name[cnt3]}_str').count()
            four = two.loc[two['poutcome'] == 'failure'].groupby(f'{tab_name[cnt3]}_str').count()
            result = pd.concat([three,four],axis=1)
            result.columns = ['success', 'failure']
            tab.dataframe(result)   
        elif tab_name[cnt3] == 'poutcome':
            continue
        else:
            two = campaign[[tab_name[cnt3],'poutcome']]
            three = two.loc[two['poutcome'] == 'success'].groupby(f'{tab_name[cnt3]}').count()
            four = two.loc[two['poutcome'] == 'failure'].groupby(f'{tab_name[cnt3]}').count()
            result = pd.concat([three,four],axis=1)
            result.columns = ['success', 'failure']
            tab.dataframe(result)
        cnt3 += 1






    







