import streamlit as st
import time
import sqlite3
import requests
import pandas as pd
from config import load
from bs4 import BeautifulSoup
import json
from streamlit_lottie import st_lottie
from urllib.parse import quote
from streamlit import session_state
from requests.exceptions import ConnectionError

# 성분알리미 페이지 전환목적
if 'page' not in st.session_state:
    st.session_state.page = "home"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.prompt_state = []
    st.session_state.image_messages = []

config = load()
api_config = config["api"]
chat_api_config = api_config["chat"]
recommend_api_config = api_config["recommend"]

def request_chat(text: str, product_names: list[str] = []) -> tuple[str, list]:
    
    print(f"Start request chat:\n{text}")
    data = {
        "state": st.session_state.prompt_state,
        "text": text,
        "product_list": product_names
    }
    
    try:
        response = requests.post(url=f"http://{chat_api_config['host']}:{chat_api_config['port']}/prompt", json=data)
        if response.status_code == 200:
            response_json = response.json()
            state = response_json["state"]
            answer = response_json["answer"]
            product_list = response_json["products"]
            print(f"### state:\n{state}")
            print(f"### product_list:\n{product_list}")
            if not product_list:
                st.session_state.prompt_state.append(state[-1])
                st.session_state.prompt_state.append({"role":"답변", "content":answer})
            print(f"Success request chat")
            return answer, product_list
        else:
            print(f"Faile request chat")
            return "매칭되는 추천상품이 없어서 대신 누구나 사용하기 좋은 상품을 추천드려요.", []
    except ConnectionError:
        return "서버와의 연결이 원활하지 않아요. 잠시 후 다시 시도해주세요.", []
                
    

def randing():
    
    st.header("✨깨끗하게 맑게 자신있게!✨")
    st.markdown("🧙‍♂️피부요정 뽀야미에게 맡겨만 주세요!")

    # SQLite 데이터베이스 연결
    print(f"Start Connect Databse")
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
    print(f"End Connect Databse")

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

        age_selected = age.selectbox('나이', ['10대', '20대', '30대', '40대', '50대', '60대'], key='나이', label_visibility="collapsed")
        gender_selected = gender.selectbox('성별', ['남', '여'], key='성별', label_visibility="collapsed")
        skin_type_selected = skin_type.selectbox('피부타입', ['악건성', '건성', '중성·복합성', '지성', '민감성'], key='피부타입', label_visibility="collapsed")
        skin_concern_selected = skin_concern.selectbox('피부고민', ['여드름', '홍조', '모공', '각질', '블랙헤드', '요철'], key='피부고민', label_visibility="collapsed")

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
    
    selected_products = st.multiselect('선택된 상품들', product_list, placeholder = 'ex) 구달 맑은 어성초 진정 수분 토너', label_visibility="collapsed")
    
    if st.button('추천받기'):
        
        if not selected_products:
            st.info("1개이상 제품을 선택해주세요.")
        else:
            with st.spinner("추천과 답변을 기다리는 중입니다..."):
                #request_chat으로 추천상품 반환하기
                answer, product_list = request_chat(text="", product_names=selected_products)
                
            #이미지 none인 경우
            default_image = "https://www.generationsforpeace.org/wp-content/uploads/2018/03/empty.jpg"

            if not product_list:
                product_list = [
                    {
                        "id": 10,
                        "name": "라로슈포제 시카플라스트 밤",
                        "category": "밤",
                        "skin_type": "지성에 좋아요",
                        "contents": ["지성에 좋아요", "진정에 좋아요", "자극적이에요"],
                        "image_url": "https://image.oliveyoung.co.kr/uploads/images/goods/550/10/0000/0019/A00000019835702ko.jpg?l=ko", # None 일 수도 있음 (없을 경우)
                        "ingredients": "정제수, 약모밀추출물(15%), 글리세린, 판테놀, 소듐레불리네이트" # None 일 수도 있음 (없을 경우)
                    },
                    {
                        "id": 20,
                        "name": "달바 화이트 트러플 퍼스트 스프레이 세럼 100ml",
                        "category": "세럼",
                        "skin_type": "복합성에 좋아요",
                        "contents": ["복합성에 좋아요", "여드름에 좋아요", "자극없이 순해요"],
                        "image_url": "https://image.oliveyoung.co.kr/uploads/images/goods/550/10/0000/0017/A00000017131219ko.jpg?l=ko", # None 일 수도 있음 (없을 경우)
                        "ingredients": "글리세린, 판테놀, 소듐레불리네이트" # None 일 수도 있음 (없을 경우)
                    },
                    {
                        "id": 30,
                        "name": "토리든 다이브인 저분자 히알루론산 수딩 크림 100ml",
                        "category": "크림",
                        "skin_type": "건성에 좋아요",
                        "contents": ["건성에 좋아요", "보습에 좋아요", "자극이 조금 있어요"],
                        "image_url": "https://image.oliveyoung.co.kr/uploads/images/goods/550/10/0000/0019/A00000019067724ko.jpg?l=ko", # None 일 수도 있음 (없을 경우)
                        "ingredients": "소듐레불리네이트" # None 일 수도 있음 (없을 경우)
                    }
                ]
            
            print(f"product_list:", product_list)
            print(f"product list counts: {len(product_list)}")
            expander_columns = st.columns(len(product_list))

            print(f"Start rendering products")
            for index, (product_info, expander_column) in enumerate(zip(product_list, expander_columns)):
                print("product_info type ", type(product_info))
                print("product_info", product_info)
                product_name = product_info.get("name", "")
                encoded_product_name = quote(product_name)  # 띄어쓰기를 %20으로 인코딩
                product_image = product_info.get("image_url","")
                image_url = product_image if product_image is not None else default_image
                search_url = f'https://www.oliveyoung.co.kr/store/search/getSearchMain.do?query={encoded_product_name}&giftYn=N&t_page=홈&t_click=검색창&t_search_name={encoded_product_name}'
                        
                # 제품 이미지에 하이퍼링크를 추가하여 출력
                image_with_link = f'<a href="{search_url}" target="_blank"><img src="{image_url}" width="200"></a>'
                with expander_column:
                    with st.expander(f"{product_name}"):
                        st.markdown(image_with_link, unsafe_allow_html=True)
            print(f"End rendering products")
            explanation = st.text_area(f"상품 추천 이유", answer)
        
            #성분알리미로 넘어가기
            if st.button('잘 모르겠는 성분이 있나요? 성분알리미에게 물어보세요!'):
                session_state.active_page = "ingredient_dict"
                #안넘어감...

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
        print("Start prompt")
        # Add user message to chat history
        st.session_state["messages"].append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user", avatar = '👩🏻'):
            st.markdown(prompt)
        print("display prompt")
        # Display assistant response in chat message container
        with st.chat_message("assistant", avatar = '🧙‍♂️'): 
            assistant_response = ""
            with st.spinner("답변을 기다리는 중입니다..."):
                answer, _ = request_chat(text=prompt) # 추천안받을거라서 product_list 대신 _
                assistant_response = answer
                print("End chat request")
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
                assistant_response = "서버에서 응답을 받지 못했어요. 다시 시도해주세요." if not assistant_response else assistant_response
                for chunk in assistant_response.split():
                    full_response += chunk + " "
                    time.sleep(0.08)
                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(full_response + "▌")
                    
                message_placeholder.markdown(full_response)

                # Add assistant response to chat history
                st.session_state["messages"].append({"role":    "assistant", "content": assistant_response})
    
randing()
