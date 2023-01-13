import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import json
import datetime
from PIL import Image

########################################################################################################################################################################
########################################################################################################################################################################

df = pd.read_csv('./order_data.csv',encoding='utf-8') # 주문 데이터 불러오기
df['주문날짜'] = pd.to_datetime(df['주문날짜'])

with open("./GEOJSON/my_geojson.geojson", "r") as raw_json: # geojson 맵 파일 불러오기
    my_geojson = json.load(raw_json)
    
mfd_logo = Image.open('./IMG/MFD_logo.png') # 로고 불러오기
mfd_logo_2 = Image.open('./IMG/MFD_logo_2.png')
baemin_logo = Image.open('./IMG/baemin.png')
yogiyo_logo = Image.open('./IMG/yogiyo.jpg')
coupang_logo = Image.open('./IMG/coupang.jpg')

########################################################################################################################################################################
########################################################################################################################################################################

no_add = 0
temp_df = df[['추가100','추가200']].dropna().reset_index(drop=True)
for i in range(len(temp_df)):
    j = temp_df.loc[i]
    if sum(j) == 0:
        no_add += 1
temp_df = temp_df.sum().reset_index().rename(columns = {'index':'고기추가량',0:'주문건수'})
temp_df.loc[3] = ['추가없음',no_add]

temp_df2 = df['주문시간'].value_counts().loc[[15,16,17,18,19,20,21,22,23,24]].reset_index().rename(columns = {'index':'주문시간','주문시간':'주문건수(건)'})
temp_df2['주문시간'] = temp_df2.astype('str')['주문시간'] +'시'

temp_df3 = df[['주문시간','주문금액']].groupby('주문시간').sum().loc[[15,16,17,18,19,20,21,22,23,24]].reset_index()
temp_df3['주문시간'] = temp_df3.astype('str')['주문시간'] +'시'

yogiyo_date_list = df[df['플랫폼']=='요기요'].dropna(subset=['지방'])['주문날짜'].unique()
yogiyo_min_date=pd.to_datetime(yogiyo_date_list[-1])
yogiyo_max_date=pd.to_datetime(yogiyo_date_list[0])
temp_df4 = df[['주문날짜','지방','단백','황금','세트250','고기250','고기500','추가100','추가200',
               '쌈장','와사비','말돈소금','명이나물','쌈무','김치','된장찌개','편마늘','고추','공기밥','계란찜',
               '사이다500','콜라355','콜라500','제로콜라355','제로콜라500']].dropna(subset=['지방']).reset_index(drop=True)
temp_df4 = temp_df4[temp_df4['주문날짜']>=yogiyo_min_date]
temp_df4 = temp_df4[temp_df4['주문날짜']<=yogiyo_max_date].groupby('주문날짜').sum().mean().round(1).reset_index().rename(columns = {'index':'메뉴',0:'주문건수'})

########################################################################################################################################################################
########################################################################################################################################################################

총_매출 = format(df['주문금액'].sum(),',d') + '원'
최근_매출 = format(df[['주문날짜','주문금액']].groupby('주문날짜').sum()['주문금액'].to_list()[-1],',d') + '원'
총_주문건수 = format(df['주문금액'].count(),',d') + '건'
최근_주문건수 = format(df[['주문날짜','주문금액']].groupby('주문날짜').count()['주문금액'].to_list()[-1],',d') + '건'

배민_총_매출 = format(df[df['플랫폼']=='배달의민족']['주문금액'].sum(),',d') + '원'
배민_최근_매출 = format(df[df['플랫폼']=='배달의민족'][['주문날짜','주문금액']].groupby('주문날짜').sum()['주문금액'].to_list()[-1],',d') + '원'
배민_총_주문건수 = format(df[df['플랫폼']=='배달의민족']['주문금액'].count(),',d') + '건'
배민_최근_주문건수 = format(df[df['플랫폼']=='배달의민족'][['주문날짜','주문금액']].groupby('주문날짜').count()['주문금액'].to_list()[-1],',d') + '건'

요기요_총_매출 = format(df[df['플랫폼']=='요기요']['주문금액'].sum(),',d') + '원'
요기요_최근_매출 = format(df[df['플랫폼']=='요기요'][['주문날짜','주문금액']].groupby('주문날짜').sum()['주문금액'].to_list()[-1],',d') + '원'
요기요_총_주문건수 = format(df[df['플랫폼']=='요기요']['주문금액'].count(),',d') + '건'
요기요_최근_주문건수 = format(df[df['플랫폼']=='요기요'][['주문날짜','주문금액']].groupby('주문날짜').count()['주문금액'].to_list()[-1],',d') + '건'

쿠팡_총_매출 = format(df[df['플랫폼']=='쿠팡이츠']['주문금액'].sum(),',d') + '원'
쿠팡_최근_매출 = format(df[df['플랫폼']=='쿠팡이츠'][['주문날짜','주문금액']].groupby('주문날짜').sum()['주문금액'].to_list()[-1],',d') + '원'
쿠팡_총_주문건수 = format(df[df['플랫폼']=='쿠팡이츠']['주문금액'].count(),',d') + '건'
쿠팡_최근_주문건수 = format(df[df['플랫폼']=='쿠팡이츠'][['주문날짜','주문금액']].groupby('주문날짜').count()['주문금액'].to_list()[-1],',d') + '건'

총_일별_매출 = px.line(df[['주문날짜','주문금액']].groupby('주문날짜').sum(),
                  title='총 일별 매출',
                  markers=True,
                  labels={'variable':'플랫폼','value':'총 매출(원)'},
                  color_discrete_sequence=['rgb(32,75,155)'])
총_일별_매출.update_layout(yaxis_tickformat = ',d',
                      showlegend=False)

총_일별_주문건수 = px.line(df[['주문날짜','주문금액']].groupby('주문날짜').count(),
                  title='총 일별 주문건수',
                  markers=True,
                  labels={'variable':'플랫폼','value':'총 주문건수(건)'},
                  color_discrete_sequence=['rgb(32,75,155)'])
총_일별_주문건수.update_layout(yaxis_tickformat = 'd',
                      showlegend=False)

플랫폼_일별_매출 = px.line(pd.pivot_table(df[['플랫폼','주문날짜','주문금액']], values='주문금액', index='주문날짜',columns='플랫폼', aggfunc=np.sum, fill_value=0).reset_index(),
                    x="주문날짜", y=['배달의민족','요기요','쿠팡이츠'], 
                    title='플랫폼 일별 매출',
                    markers=True,
                    labels={'variable':'플랫폼','value':'매출(원)'},
                    color_discrete_sequence=['rgb(42,193,188)','rgb(250,0,80)','rgb(22,131,80)'])          
플랫폼_일별_매출.update_layout(yaxis_tickformat = ',d')

플랫폼_일별_주문건수 = px.line(pd.pivot_table(df[['플랫폼','주문날짜','주문금액']], values='주문금액', index='주문날짜',columns='플랫폼', aggfunc=len, fill_value=0).reset_index(),
                    x="주문날짜", y=['배달의민족','요기요','쿠팡이츠'], 
                    title='플랫폼 일별 주문건수',
                    markers=True,
                    labels={'variable':'플랫폼','value':'주문건수(건)'},
                    color_discrete_sequence=['rgb(42,193,188)','rgb(250,0,80)','rgb(22,131,80)'])          
플랫폼_일별_주문건수.update_layout(yaxis_tickformat = 'd')

요일별_평균_매출 = px.bar(df[['주문날짜','주문요일','주문금액']].groupby(['주문날짜','주문요일']).sum().reset_index()[['주문요일','주문금액']].groupby('주문요일').mean().loc[['월','화','수','목','금','토','일']].reset_index().round(-3),
                  x = '주문요일', y = '주문금액', title = '요일별 평균 매출',
                  labels={'x':'주문요일','주문금액':'주문금액(원)'},
                  color='주문금액',
                  text_auto=True,
                  color_continuous_scale=px.colors.sequential.Bluyl)
요일별_평균_매출.update_layout(yaxis_tickformat = ',d',
                      showlegend=False)

요일별_평균_주문건수 = px.bar(df[['주문날짜','주문요일','주문금액']].groupby(['주문날짜','주문요일']).count().reset_index()[['주문요일','주문금액']].groupby('주문요일').mean().loc[['월','화','수','목','금','토','일']].reset_index(),
                  x = '주문요일', y = '주문금액', title = '요일별 평균 주문건수',
                  labels={'x':'주문요일','주문금액':'주문건수(건)'},
                  color='주문금액',
                  text_auto=True,
                  color_continuous_scale=px.colors.sequential.Bluyl)
요일별_평균_주문건수.update_layout(yaxis_tickformat = 'd',
                      showlegend=False)

시간별_총_매출 = px.bar(temp_df3,
                    x = '주문시간', y = '주문금액', title = '시간별 총 매출',
                    color='주문금액',
                    text_auto=True,
                    color_continuous_scale=px.colors.sequential.Bluyl)
시간별_총_매출.update_layout(yaxis_tickformat = ',d')

시간별_주문건수 = px.bar(temp_df2,
                    x = '주문시간', y = '주문건수(건)', title = '시간별 주문건수',
                    color='주문건수(건)',
                    text_auto=True,
                    color_continuous_scale=px.colors.sequential.Bluyl)

고기추가 = px.pie(temp_df,
              values='주문건수', names='고기추가량', title='고기추가량',
              hole=0.3,
              color_discrete_sequence=px.colors.qualitative.Vivid)

메인메뉴 = px.pie(df[['세트250','고기250','고기500']].sum().reset_index().rename(columns = {'index':'메인메뉴',0:'주문건수'}),
              values='주문건수', names='메인메뉴', title='메인메뉴',
              hole=0.3,
              color_discrete_sequence=px.colors.qualitative.Vivid)

살코기 = px.pie(df[['지방','단백','황금']].sum().reset_index().rename(columns = {'index':'살코기',0:'주문건수'}),
              values='주문건수', names='살코기', title='살코기',
              hole=0.3,
              color_discrete_sequence=px.colors.qualitative.Vivid)

소스 = px.pie(df[['쌈장','와사비','말돈소금']].sum().reset_index().rename(columns = {'index':'소스',0:'주문건수'}),
              values='주문건수', names='소스', title='소스',
              hole=0.3,
              color_discrete_sequence=px.colors.qualitative.Vivid)

일평균_메뉴별_주문량 = px.bar(temp_df4,
                    x = '메뉴', y = '주문건수', title = '일평균 메뉴별 주문량(요기요 영수증 기록이 입력된 날짜만 포함)',
                    color='주문건수',
                    text_auto=True,
                    color_continuous_scale=px.colors.sequential.Bluyl)

행정구별_주문건수 = px.pie(df['지역(구)'].value_counts().reset_index().rename(columns = {'index':'지역(구)','지역(구)':'주문건수'}),
                    values='주문건수', names='지역(구)', title='행정구별 주문건수',
                    hole=0.3,
                    color_discrete_sequence=px.colors.qualitative.Vivid)

행정동별_주문건수 = px.bar(df['지역(동)'].value_counts().reset_index().rename(columns = {'index':'지역(동)','지역(동)':'주문건수'}),
                    x = '지역(동)', y = '주문건수', title = '행정동별 주문건수',
                    color='주문건수',
                    text_auto=True,
                    color_continuous_scale=px.colors.sequential.Bluyl)

행정동별_주문건수_지도 = px.choropleth_mapbox(df['지역(동)'].value_counts().reset_index().rename(columns = {'index':'지역(동)','지역(동)':'주문건수'}),
                          geojson = my_geojson,
                          locations = '지역(동)', color = '주문건수', title = '행정동별 주문건수 지도(동작,관악)',
                          featureidkey = "properties.adm_nm",
                          color_continuous_scale=px.colors.sequential.Bluyl,
                          center = {"lat": 37.4782, "lon": 126.942}, zoom=12, opacity=0.5,
                          width = 800, height = 800,
                          mapbox_style="carto-positron") # open-street-map

#########################################################################################################################################################################
#######################################################################################################################################################################

st.set_page_config(page_title='MFD Dash Board', 
                    page_icon=mfd_logo, 
                    layout="wide", 
                    initial_sidebar_state="auto", 
                    menu_items=None)

st.write(str(df.iloc[0,3]).split()[0]+' 기준 (현장결제건 제외)')

_,c1,_, c2,_, c3,_, c4,_ = st.columns([2,10,2,10,2,10,2,10,2])
with c1:
    st.image(mfd_logo_2)
with c2:
    st.image(yogiyo_logo)
with c3:
    st.image(baemin_logo)
with c4:
    st.image(coupang_logo)

_,c1,_, c2,_, c3,_, c4,_ = st.columns([2,10,2,10,2,10,2,10,2])
with c1:
    st.metric(label="총 매출", value=총_매출, delta=최근_매출)
    st.metric(label="총 주문건수", value=총_주문건수, delta=최근_주문건수)
with c2:
    st.metric(label="요기요 총 매출", value=요기요_총_매출, delta=요기요_최근_매출)
    st.metric(label="요기요 총 주문건수", value=요기요_총_주문건수, delta=요기요_최근_주문건수)   
with c3:
    st.metric(label="배달의민족 총 매출", value=배민_총_매출, delta=배민_최근_매출)
    st.metric(label="배달의민족 총 주문건수", value=배민_총_주문건수, delta=배민_최근_주문건수)   
with c4:
    st.metric(label="쿠팡이츠 총 매출", value=쿠팡_총_매출, delta=쿠팡_최근_매출)
    st.metric(label="쿠팡이츠 총 주문건수", value=쿠팡_총_주문건수, delta=쿠팡_최근_주문건수)   

c1, c2 = st.columns([1,1])
with c1:
    st.plotly_chart(총_일별_매출, use_container_width=True)
    st.plotly_chart(플랫폼_일별_매출, use_container_width=True)
    st.plotly_chart(요일별_평균_매출, use_container_width=True)
    st.plotly_chart(시간별_총_매출, use_container_width=True)
with c2:
    st.plotly_chart(총_일별_주문건수, use_container_width=True)
    st.plotly_chart(플랫폼_일별_주문건수, use_container_width=True)
    st.plotly_chart(요일별_평균_주문건수, use_container_width=True)
    st.plotly_chart(시간별_주문건수, use_container_width=True)

c1, c2, c3, c4 = st.columns([1,1,1,1])
with c1:
    st.plotly_chart(메인메뉴, use_container_width=True)
with c2:
    st.plotly_chart(살코기, use_container_width=True)
with c3:
    st.plotly_chart(소스, use_container_width=True)
with c4:
    st.plotly_chart(고기추가, use_container_width=True)
    
st.plotly_chart(일평균_메뉴별_주문량, use_container_width=True)

c1, c2 = st.columns([3,4])
with c1:
    st.plotly_chart(행정동별_주문건수_지도, use_container_width=True)
with c2:
    st.plotly_chart(행정동별_주문건수, use_container_width=True)
    st.plotly_chart(행정구별_주문건수, use_container_width=True)

#########################################################################################################################################################################
#######################################################################################################################################################################

days = st.date_input("기간을 입력해주세요.", 
                    value = [datetime.date(2022, 10, 19), datetime.datetime.today()],
                    min_value=datetime.date(2022, 10, 19), 
                    max_value=datetime.datetime.today())
df_days = df[df['주문날짜']>=np.datetime64(days[0])][df['주문날짜']<=np.datetime64(days[1])] 

배민_삼만원_건수 = df_days[df_days['플랫폼'] == '배달의민족']
배민_삼만원_건수 = str(len(배민_삼만원_건수[배민_삼만원_건수['주문금액'] >= 30000]))+'건'
배민_쿠폰_지출 = format(df_days[df_days['플랫폼'] == '배달의민족']['매장부담금액'].sum(),',d') + '원'
요기요_쿠폰_지출 = format(df_days[df_days['플랫폼'] == '요기요']['매장부담금액'].sum(),',d') + '원'
쿠팡이츠_쿠폰_광고_지출 = format(df_days[df_days['플랫폼'] == '쿠팡이츠']['매장부담금액'].sum(),',d') + '원'

#########################################################################################################################################################################
#######################################################################################################################################################################

c1, c2, c3, c4 = st.columns([1,1,1,1])
with c1:
    st.metric(label="배달의민족 3만원 이상 주문건수", value=배민_삼만원_건수)
with c2:
    st.metric(label="배달의민족 쿠폰 지출 금액", value=배민_쿠폰_지출)
with c3:
    st.metric(label="요기요 쿠폰 지출 금액", value=요기요_쿠폰_지출)
with c4:
    st.metric(label="쿠팡이츠 쿠폰 및 광고 지출 금액", value=쿠팡이츠_쿠폰_광고_지출)

st.subheader('원본 주문 데이터')
st.dataframe(df_days)

@st.cache
def convert_df(df_days):
    return df_days.to_csv().encode('utf-8') # IMPORTANT: Cache the conversion to prevent computation on every rerun
csv = convert_df(df_days)

st.download_button(
    label="csv파일 다운로드",
    data=csv,
    file_name=f'MFD_order_data_{str(df.iloc[0,2]).split()[0]}.csv',
    mime='text/csv')