import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.markdown("form_analysis")
st.sidebar.markdown("📈 form_analysis")

# SQLite 데이터베이스 연결
conn = sqlite3.connect('user_data.db')

# 사용자 데이터 불러오기
df = pd.read_sql_query('SELECT * FROM user_data', conn)

# SQLite 연결 닫기
conn.close()

# 시각화
st.title('사용자 데이터 시각화')

# 나이별 분포
st.subheader('나이별 분포')
fig_age = px.histogram(df, x='age', title='나이별 분포')
st.plotly_chart(fig_age)

# 성별 분포
st.subheader('성별 분포')
fig_gender = px.pie(df, names='gender', title='성별 분포')
st.plotly_chart(fig_gender)

# 피부타입 분포
st.subheader('피부타입 분포')
fig_skin_type = px.pie(df, names='skin_type', title='피부타입 분포')
st.plotly_chart(fig_skin_type)

# 피부고민 분포
st.subheader('피부고민 분포')
fig_skin_concern = px.pie(df, names='skin_concern', title='피부고민 분포')
st.plotly_chart(fig_skin_concern)
