import streamlit as st
import pandas as pd
import plotly.express as px
import time

time.sleep(1)

# 화면 꽉 차게하기
st.set_page_config(layout="wide")

# 은행 데이터 전처리
# 그래프를 그리기위해 문자열 행을 추가해주기
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

# 로지스틱 데이터
@st.cache_data
def load_logistic():
    logi = pd.read_csv("logistic.csv")
    return logi
logi = load_logistic()

def loader(num):
    with st.spinner('Wait for it...'):
        time.sleep(num)

def empty_maker(num):
    for _ in range(num):
        st.markdown('####')

def stream_data(txt):
    for word in txt.split(" "):
        yield word + " "
        time.sleep(0.02)

# 홈 화면
def home():
    st.title("Project : Providing Optimal Customization Solutuins")
    st.divider()

    content = """본 프로젝트는 은행을 이용하는 고객들의 데이터를 분석하여, 은행에서 제공하는 캠페인의 성공 확률을 증가시키는 것을 목표로 합니다.
    \n이를 위해 데이터 분석 기법 중 하나인 로지스틱 회귀법을 적용하여 데이터의 각 요인이 캠페인의 성공여부에 미치는 영향을 산술적으로 도출합니다.
    \n이후, 결과에 따라 캠페인 시행 대상을 추천합니다.\n
    페이지 목록\n
    1. Data Dashboard : 다양한 기준이 적용된 데이터 시각화 차트들이 배치된 화면을 제공합니다.\n 
    2. Campaign Target : 캠페인 시행 추천 대상 고객을 확인할 수 있는 화면을 제공합니다.
    """
    st.write_stream(stream_data(content))



# 대시보드 화면
def dashboard():
    st.title("📊Bank Data Dashboard")
    st.divider()
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


    # container
    col1, col2, col3 = st.columns([0.2,0.5,0.3])

    with col1:
        # 이익 그룹의 수
        st.subheader("A profitable group")
        st.metric(label="No Credit Default & Enough Balane(above 5000)", value=profitable_num)

        st.divider()

        # 이익 되지 않는 그룹의 수
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

        st.divider()

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
                tab.dataframe(result,width=250)   
            elif tab_name[cnt3] == 'poutcome':
                continue
            else:
                two = campaign[[tab_name[cnt3],'poutcome']]
                three = two.loc[two['poutcome'] == 'success'].groupby(f'{tab_name[cnt3]}').count()
                four = two.loc[two['poutcome'] == 'failure'].groupby(f'{tab_name[cnt3]}').count()
                result = pd.concat([three,four],axis=1)
                result.columns = ['success', 'failure']
                tab.dataframe(result,width=250)
            cnt3 += 1


# 서비스 화면
def service():
    st.title("💡Recommend Campaign Target")
    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("DataFrame for labels that affect compaign success")
        st.dataframe(logi, width=500)

    with col2:
        st.subheader("Campaign Target Recommendation")

        content = """
        캠페인 타겟\n
        1. Balance : 연평균 계좌 잔액이 많은 고객\n 
        2. Housing : 주택 대출을 받은 고객
        3. Loan : 주택 이외의 대출을 받은 고객
        4. Campaign : 이번 캠페인 동안 은행과의 컨택이 빈번했던 고객 
        5. Previous : 이 캠페인 이전에 은행과의 컨택 수가 빈번했던 고객
        6. Deposit : 정기예금에 가입한 고객
        """
        st.write_stream(stream_data(content))
