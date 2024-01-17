# 가영님
import streamlit as st
import time
import sqlite3
import requests
import pandas as pd
from config import load
import json
from streamlit_lottie import st_lottie

config = load()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.prompt_state = []
    st.session_state.image_messages = []

def randing():
    
    st.header("✨깨끗하게 맑게 자신있게!✨")
    st.markdown("🧙‍♂️피부요정 뽀야미에게 맡겨만 주세요!")

    # SQLite 데이터베이스 연결
    conn = sqlite3.connect('resource/data/user_data.db')
    cursor = conn.cursor()

    # 테이블 생성 (첫 실행 시 한 번만 실행)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age TEXT,
            gender TEXT,
            skin_type TEXT,
            skin_concern TEXT
        )
    ''')
    conn.commit()

    st.markdown("""
    <style>
        hr {
            border: 1px solid #ddd;  # 구분선의 색상 및 굵기 설정
        }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True) 

    #폼 생성
    st.subheader("""
                 기본정보입력창""")
    st.markdown("""▶ 기본정보를 입력해주시면 더 정확한 상담을 진행해드려요!
                \n👈사이드바의 **📈form analysis**에서 나와 비슷한 사람들에게 인기있는 상품도 확인하실 수 있어요!""")
    with st.form(key='columns_in_form'):
        age, gender, skin_type, skin_concern = st.columns(4)

        age_selected = age.selectbox('나이', ['10대', '20대', '30대', '40대', '50대', '60대'], key='나이')
        gender_selected = gender.selectbox('성별', ['남', '여'], key='성별')
        skin_type_selected = skin_type.selectbox('피부타입', ['악건성', '건성', '중성·복합성', '지성', '민감성'], key='피부타입')
        skin_concern_selected = skin_concern.selectbox('피부고민', ['여드름', '홍조', '모공', '각질', '블랙헤드', '요철'], key='피부고민')

        submitted = st.form_submit_button('제출')

    # 제출 버튼이 눌렸을 때
    if submitted:
        # 데이터베이스에 데이터 추가
        cursor.execute('''
            INSERT INTO user_data (age, gender, skin_type, skin_concern)
            VALUES (?, ?, ?, ?)
        ''', (age_selected, gender_selected, skin_type_selected, skin_concern_selected))
        conn.commit()
        st.success('데이터가 성공적으로 저장되었습니다.')

    # SQLite 연결 닫기
    conn.close()

    #제품사용이력 받아서 제품 추천
    st.markdown("<hr>", unsafe_allow_html=True) 
    recommend = 'resource/data/recommend.json'
    with open(recommend, "r") as file:
        url = json.load(file)
    st_lottie(url, reverse=True, height=300, width=300, speed=1, loop=True, quality='high')
    st.subheader("""제품추천""") 
    st.markdown("""▶ 만족스럽게 사용했던 스킨케어 제품 3개를 선택해주세요.
                \nℹ️브랜드명을 먼저 입력하면 쉽게 검색할 수 있어요!""") 
     
    csv_file_path = 'resource/data/brand_ingredient_dataset.csv'
    df = pd.read_csv(csv_file_path)
    product = df['brand'].tolist()
    product_list = list(set(product))
    
    selected_products = st.multiselect('', product_list, placeholder = 'ex) 구달 맑은 어성초 진정 수분 토너')
    if st.button('추천받기'):
        #협업 필터링으로 추천상품 반환. 데이터 형태는 아래처럼 짰음
        rec_product = [
                    {"image_url": "https://image.oliveyoung.co.kr/uploads/images/goods/550/10/0000/0019/A00000019835702ko.jpg?l=ko",
                    'product_info': {"link_url": "https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000198357&dispCatNo=90000010009&trackingCd=Best_Sellingbest&t_page=%EB%9E%AD%ED%82%B9&t_click=%ED%8C%90%EB%A7%A4%EB%9E%AD%ED%82%B9_%EC%8A%A4%ED%82%A8%EC%BC%80%EC%96%B4_%EC%83%81%ED%92%88%EC%83%81%EC%84%B8&t_number=10",
                                    "caption": "라로슈포제 시카플라스트 밤"}},
                    {"image_url": "https://image.oliveyoung.co.kr/uploads/images/goods/550/10/0000/0017/A00000017131219ko.jpg?l=ko",
                    'product_info': {"link_url": "https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000171312&dispCatNo=90000010009&trackingCd=Best_Sellingbest&t_page=%EB%9E%AD%ED%82%B9&t_click=%ED%8C%90%EB%A7%A4%EB%9E%AD%ED%82%B9_%EC%8A%A4%ED%82%A8%EC%BC%80%EC%96%B4_%EC%83%81%ED%92%88%EC%83%81%EC%84%B8&t_number=22",
                                    "caption": "달바 화이트 트러플 퍼스트 스프레이 세럼 100ml"}},
                    {"image_url": "https://image.oliveyoung.co.kr/uploads/images/goods/550/10/0000/0019/A00000019067724ko.jpg?l=ko",
                    'product_info': {"link_url": "https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000190677&dispCatNo=90000010009&trackingCd=Best_Sellingbest&t_page=%EB%9E%AD%ED%82%B9&t_click=%ED%8C%90%EB%A7%A4%EB%9E%AD%ED%82%B9_%EC%8A%A4%ED%82%A8%EC%BC%80%EC%96%B4_%EC%83%81%ED%92%88%EC%83%81%EC%84%B8&t_number=27",
                                    "caption": "토리든 다이브인 저분자 히알루론산 수딩 크림 100ml"}}
                ]

        expander_columns = st.columns(len(rec_product))

        for index, (image_info, expander_column) in enumerate(zip(rec_product, expander_columns)):
            image_with_link = f'<a href="{image_info["product_info"]["link_url"]}" target="_blank"><img src="{image_info["image_url"]}" width="200"></a>'

            with expander_column:
                with st.expander(f"{image_info['product_info']['caption']}"):
                    st.markdown(image_with_link, unsafe_allow_html=True)
                    # 각 상품에 대한 추천 이유를 담은 답변 창 추가
                    explanation = st.text_area(f"상품 {index + 1}에 대한 추천 이유", f"이 상품은 {image_info['product_info']['caption']}의 특징 때문에 추천합니다.")

        # explanations = []

        # for index, image_info in enumerate(rec_product):
        #     image_with_link = f'<a href="{image_info["product_info"]["link_url"]}" target="_blank"><img src="{image_info["image_url"]}" width="200"></a>'
            
        #     with st.expander(f"{image_info['product_info']['caption']}"):
        #         st.markdown(image_with_link, unsafe_allow_html=True)
                
        #         # 각 상품에 대한 추천 이유를 담은 답변 창 추가. 답변 받아오는 것 추가 필요
        #         explanation = st.text_area("추천 이유", f"이 상품은 {image_info['product_info']['caption']}의 특징 때문에 추천합니다.")
        #         explanations.append(explanation)

        # #Expand 창 생성
        # for image_info in rec_product:
        #     image_with_link = f'<a href="{image_info["product_info"]["link_url"]}" target="_blank"><img src="{image_info["image_url"]}" width="200"></a>'
        #     with st.expander(f"{image_info['product_info']['caption']}"):
        #         st.markdown(image_with_link, unsafe_allow_html=True)


    st.markdown("<hr>", unsafe_allow_html=True)
    chatbot_startanime = 'resource/data/chatbot_start.json'
    with open(chatbot_startanime, "r") as file:
        url = json.load(file)
    st_lottie(url, reverse=True, height=200, width=200, speed=1, loop=True, quality='high')
    st.subheader("""챗봇""")
    st.markdown("""▶ 무엇이든 물어봐요! 당신만을 위한 챗봇서비스입니다.
                \n🤩'스킨케어 추천'이라는 키워드와 함께 질문하면 추천상품소개를 바로 받아보실 수 있어요!""") 

    # Display chat messages from history on app rerun
    for message in st.session_state["messages"]:
        avatar = '👩🏻' if message["role"] == "user" else '🧙‍♂️'
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("말만 해요! 이 뽀야미가 해결해줄게요:)"):

        # Add user message to chat history
        st.session_state["messages"].append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user", avatar = '👩🏻'):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant", avatar = '🧙‍♂️'): 
            assistant_response = ""
            with st.spinner("답변을 기다리는 중입니다..."):
                
                api_config = config["api"]
                
                chat_api_config = api_config["chat"]
                recommend_api_config = api_config["recommend"]
                
                data = {
                    "state": st.session_state.prompt_state,
                    "text": prompt
                }
                
                assistant_response = "답변"

                # response = requests.post(url=f"http://{chat_api_config['host']}:{chat_api_config['port']}/prompt", json=data)
                
                # if response.status_code == 200:
                #     response_json = response.json()
                #     state = response_json["state"]
                #     answer = response_json["answer"]
                #     st.session_state.prompt_state.append(state[-1])
                #     st.session_state.prompt_state.append({"role":"ANSWER", "content":answer})
                    
                # else:
                #     answer = "서비스 오류가 발생했습니다. 다시 시도해주세요."


            if "스킨케어 추천" in prompt:
                #이미지 3개
                rec_product = [
                    {"image_url": "https://image.oliveyoung.co.kr/uploads/images/goods/550/10/0000/0019/A00000019835702ko.jpg?l=ko",
                    'product_info': {"link_url": "https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000198357&dispCatNo=90000010009&trackingCd=Best_Sellingbest&t_page=%EB%9E%AD%ED%82%B9&t_click=%ED%8C%90%EB%A7%A4%EB%9E%AD%ED%82%B9_%EC%8A%A4%ED%82%A8%EC%BC%80%EC%96%B4_%EC%83%81%ED%92%88%EC%83%81%EC%84%B8&t_number=10",
                                    "caption": "라로슈포제 시카플라스트 밤"}},
                    {"image_url": "https://image.oliveyoung.co.kr/uploads/images/goods/550/10/0000/0017/A00000017131219ko.jpg?l=ko",
                    'product_info': {"link_url": "https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000171312&dispCatNo=90000010009&trackingCd=Best_Sellingbest&t_page=%EB%9E%AD%ED%82%B9&t_click=%ED%8C%90%EB%A7%A4%EB%9E%AD%ED%82%B9_%EC%8A%A4%ED%82%A8%EC%BC%80%EC%96%B4_%EC%83%81%ED%92%88%EC%83%81%EC%84%B8&t_number=22",
                                    "caption": "달바 화이트 트러플 퍼스트 스프레이 세럼 100ml"}},
                    {"image_url": "https://image.oliveyoung.co.kr/uploads/images/goods/550/10/0000/0019/A00000019067724ko.jpg?l=ko",
                    'product_info': {"link_url": "https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000190677&dispCatNo=90000010009&trackingCd=Best_Sellingbest&t_page=%EB%9E%AD%ED%82%B9&t_click=%ED%8C%90%EB%A7%A4%EB%9E%AD%ED%82%B9_%EC%8A%A4%ED%82%A8%EC%BC%80%EC%96%B4_%EC%83%81%ED%92%88%EC%83%81%EC%84%B8&t_number=27",
                                    "caption": "토리든 다이브인 저분자 히알루론산 수딩 크림 100ml"}}
                ]
                
                # 이미지를 채팅 메세지로 추가
                for product in rec_product:
                    st.session_state.image_messages.append({"role": "assistant", "content": product, "avatar": "🧙‍♂️"})

                # 채팅컨테이너 내 이미지 나오게
                if st.session_state.image_messages:
                    for message in st.session_state.image_messages:
                        if message["role"] == "assistant" and "content" in message and isinstance(message["content"], dict):
                            with st.container():
                                image_html = f'<a href="{message["content"]["product_info"]["link_url"]}" target="_blank"><img src="{message["content"]["image_url"]}" width="200" /></a>'
                                product_info = f"**{message['content']['product_info']['caption']}**"
                                st.image(message["content"]["image_url"], width=200)
                                st.write(product_info)
                                st.empty()
                        

                else:
                    # Display assistant response in chat message container
                    message_placeholder = st.empty()

                    # Simulate stream of response with milliseconds delay
                    full_response = ""
                    for chunk in assistant_response.split():
                        full_response += chunk + " "
                        time.sleep(0.08)
                        # Add a blinking cursor to simulate typing
                        message_placeholder.markdown(full_response + "▌")
                        
                    message_placeholder.markdown(full_response)

                # Add assistant response to chat history
                st.session_state["messages"].append({"role":    "assistant", "content": assistant_response})
    
randing()
