import streamlit as st
import pandas as pd
st.header("📖 성분알리미")
st.markdown('')

df1 = pd.read_csv('resource/data/cosmetic_ingredients.csv', encoding='euc-kr')
search1 = st.text_input("궁금했던 성분이 있나요? 제게 물어보세요!", value='')
m1 = df1['성분명'].str.contains(search1)
df_search1 = df1[m1]

if search1 and not df_search1.empty:
    # 선택할 칼럼들 지정
    selected_columns = ['성분명', '기원 및 정의', '배합목적']

    # 화면 가로 길이에 맞춰서 데이터프레임 출력
    st.dataframe(df_search1[selected_columns].style.set_properties(**{'max-width': '800px'}))
elif df_search1.empty:
    st.warning('검색 결과가 없습니다.')


df2 = pd.read_csv('resource/data/brand_ingredient_dataset.csv')
df2_unique = df2.drop_duplicates(subset=['brand'])
search2 = st.text_input("특정 성분이 포함된 스킨케어제품을 찾고 계신가요? 원하는 성분을 알려주시면 제품을 찾아드릴게요!", value='')
m2 = df2_unique['ingredients_list'].str.contains(search2, na=False)
df_search2 = df2_unique[m2]

if search2 and not df_search2.empty:
    # 선택할 칼럼들 지정
    selected_columns = ['brand', 'product_image_url']

    # 이미지를 4개씩 한 줄에 나열
    num_columns = 4
    num_rows = (len(df_search2) - 1) // num_columns + 1

    # 이미지가 들어갈 컬럼 생성
    cols = st.columns(num_columns)

    for i, (_, row) in enumerate(df_search2[selected_columns].iterrows()):
        col_index = i % num_columns
        with cols[col_index]:
            st.image(row['product_image_url'], caption=row['brand'], use_column_width=True)
elif df_search2.empty:
    st.warning('검색 결과가 없습니다.')