import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.header("📈 설문조사데이터 분석보고서")
st.markdown("입력해주신 기본정보를 바탕으로 현재의 서비스 유저들의 피부고민과 인기상품을 한 눈에 확인할 수 있어요!")

# SQLite 데이터베이스 연결
conn = sqlite3.connect('resource/data/user_data.db')

# 사용자 데이터 불러오기
df = pd.read_sql_query('SELECT * FROM user_data', conn)

# SQLite 연결 닫기
conn.close()

# 나이별 분포
st.subheader('나이별 분포')
fig_age = px.histogram(df, x='age')
st.plotly_chart(fig_age)

# 성별 분포
st.subheader('성별 분포')
fig_gender = px.pie(df, names='gender')
st.plotly_chart(fig_gender)

# 피부타입 분포
st.subheader('피부타입 분포')
fig_skin_type = px.pie(df, names='skin_type')
st.plotly_chart(fig_skin_type)

# 피부고민 분포
st.subheader('피부고민 분포')
fig_skin_concern = px.pie(df, names='skin_concern')
st.plotly_chart(fig_skin_concern)
