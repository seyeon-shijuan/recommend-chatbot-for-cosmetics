# 가영님
import streamlit as st
import random
import time
import sqlite3
import requests
from config import load

config = load()

def randing():
    
    with st.sidebar:
        openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
        "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
        "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
        "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

    st.title("깨끗하게 맑게 자신있게!")
    st.caption("피부요정 뽀야미에게 맡겨만 주세요!")

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

    #폼 생성
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

    # Display chat messages from history on app rerun
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
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
                
                response = requests.post(url=f"http://{chat_api_config['host']}:{chat_api_config['port']}/prompt", json=data)
                
                if response.status_code == 200:
                    response_json = response.json()
                    state = response_json["state"]
                    answer = response_json["answer"]
                    st.session_state.prompt_state.append(state[-1])
                    st.session_state.prompt_state.append({"role":"ANSWER", "content":answer})
                    
                else:
                    answer = "서비스 오류가 발생했습니다. 다시 시도해주세요."
                
                assistant_response = answer

            if "스킨케어 추천" in prompt:
                #이미지 3개
                bot_response_images = [
                    {"image_url": "https://image.oliveyoung.co.kr/uploads/images/goods/550/10/0000/0019/A00000019835702ko.jpg?l=ko",
                        "link_url": "https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000198357&dispCatNo=90000010009&trackingCd=Best_Sellingbest&t_page=%EB%9E%AD%ED%82%B9&t_click=%ED%8C%90%EB%A7%A4%EB%9E%AD%ED%82%B9_%EC%8A%A4%ED%82%A8%EC%BC%80%EC%96%B4_%EC%83%81%ED%92%88%EC%83%81%EC%84%B8&t_number=10", 
                        "caption": "라로슈포제 시카플라스트 밤"},
                    {"image_url": "https://image.oliveyoung.co.kr/uploads/images/goods/550/10/0000/0017/A00000017131219ko.jpg?l=ko",
                        "link_url": "https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000171312&dispCatNo=90000010009&trackingCd=Best_Sellingbest&t_page=%EB%9E%AD%ED%82%B9&t_click=%ED%8C%90%EB%A7%A4%EB%9E%AD%ED%82%B9_%EC%8A%A4%ED%82%A8%EC%BC%80%EC%96%B4_%EC%83%81%ED%92%88%EC%83%81%EC%84%B8&t_number=22", 
                        "caption": "달바 화이트 트러플 퍼스트 스프레이 세럼 100ml"},
                    {"image_url": "https://image.oliveyoung.co.kr/uploads/images/goods/550/10/0000/0019/A00000019067724ko.jpg?l=ko",
                        "link_url": "https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000190677&dispCatNo=90000010009&trackingCd=Best_Sellingbest&t_page=%EB%9E%AD%ED%82%B9&t_click=%ED%8C%90%EB%A7%A4%EB%9E%AD%ED%82%B9_%EC%8A%A4%ED%82%A8%EC%BC%80%EC%96%B4_%EC%83%81%ED%92%88%EC%83%81%EC%84%B8&t_number=27", 
                        "caption": "토리든 다이브인 저분자 히알루론산 수딩 크림 100ml"} 
                    ]
                
                #Expand 창 생성
                for image_info in bot_response_images:
                    image_with_link = f'<a href="{image_info["link_url"]}" target="_blank"><img src="{image_info["image_url"]}" width="200"></a>'
                    with st.expander(f"{image_info['caption']}"):
                        st.markdown(image_with_link, unsafe_allow_html=True)
            
            else:
                # assistant_response = random.choice(
                #     [
                #     "Hello there! How can I assist you today?",
                #     "Hi, human! Is there anything I can help you with?",
                #     "Do you need help?",
                #     ]
                #     )

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
            
            # 예1) response = requests.get(url="http://localhost:8080/test")
            # response_message = response.json()["response"]
            # assistant_response = response_message

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.prompt_state = []
    

randing()






# # 가영님
# import streamlit as st
# import random
# import time
# import pandas as pd
# import sqlite3
# import requests

# def randing():
  
#     with st.sidebar:
#         openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
#         "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
#         "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
#         "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

#     st.title("✨ 깨끗하게 맑게 자신있게!")
#     st.caption("피부요정 뽀야미에게 맡겨만 주세요!")

#     # SQLite 데이터베이스 연결
#     conn = sqlite3.connect('user_data.db')
#     cursor = conn.cursor()

#     # 테이블 생성 (첫 실행 시 한 번만 실행)
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS user_data (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             age TEXT,
#             gender TEXT,
#             skin_type TEXT,
#             skin_concern TEXT
#         )
#     ''')
#     conn.commit()

#     #폼 생성
#     with st.form(key='columns_in_form'):
#         age, gender, skin_type, skin_concern = st.columns(4)

#         age_selected = age.selectbox('나이', ['10대', '20대', '30대', '40대', '50대', '60대'], key='나이')
#         gender_selected = gender.selectbox('성별', ['남', '여'], key='성별')
#         skin_type_selected = skin_type.selectbox('피부타입', ['악건성', '건성', '중성·복합성', '지성', '민감성'], key='피부타입')
#         skin_concern_selected = skin_concern.selectbox('피부고민', ['여드름', '홍조', '모공', '각질', '블랙헤드', '요철'], key='피부고민')

#         submitted = st.form_submit_button('제출')

#     # 제출 버튼이 눌렸을 때
#     if submitted:
#         # 데이터베이스에 데이터 추가
#         cursor.execute('''
#             INSERT INTO user_data (age, gender, skin_type, skin_concern)
#             VALUES (?, ?, ?, ?)
#         ''', (age_selected, gender_selected, skin_type_selected, skin_concern_selected))
#         conn.commit()
#         st.success('데이터가 성공적으로 저장되었습니다.')

#     # SQLite 연결 닫기
#     conn.close()

#     #채팅 시작
#     main()
    
# def chat_message(role, content, avatar):
#     st.write(f"**{role}**:")
#     st.markdown(f"{avatar} {content}")

# def main():
#     # 이전 대화 기록과 아바타 정보를 저장할 변수
#     chat_history = []
#     last_avatar = '👩🏻'
#     full_response = ""

#     # Display chat messages from history on app rerun
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"], content=message["content"], avatar=message.get("avatar", '👩🏻')):
#             pass

#     # Accept user input
#     if prompt := st.chat_input("말만 해요! 이 뽀야미가 해결해줄게요:)"):
#         # 이전 대화에서 사용한 아바타를 가져오기
#         last_avatar = chat_history[-1]["avatar"] if chat_history else '👩🏻'
#         # 새로운 대화를 기록에 추가
#         chat_history.append({"role": "user", "content": prompt, "avatar": last_avatar})
#         # Display user message in chat message container
#         with st.chat_message("user", prompt, last_avatar):
#             pass


#         # Display assistant response in chat message container
#         with st.chat_message("assistant", full_response, '🧙‍♂️'):
#             pass

#             if "스킨케어 추천" in prompt:
#                 #이미지 3개
#                 bot_response_images = [
#                     {"image_url": "https://image.oliveyoung.co.kr/uploads/images/goods/550/10/0000/0019/A00000019835702ko.jpg?l=ko",
#                         "link_url": "https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000198357&dispCatNo=90000010009&trackingCd=Best_Sellingbest&t_page=%EB%9E%AD%ED%82%B9&t_click=%ED%8C%90%EB%A7%A4%EB%9E%AD%ED%82%B9_%EC%8A%A4%ED%82%A8%EC%BC%80%EC%96%B4_%EC%83%81%ED%92%88%EC%83%81%EC%84%B8&t_number=10", 
#                         "caption": "라로슈포제 시카플라스트 밤"},
#                     {"image_url": "https://image.oliveyoung.co.kr/uploads/images/goods/550/10/0000/0017/A00000017131219ko.jpg?l=ko",
#                         "link_url": "https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000171312&dispCatNo=90000010009&trackingCd=Best_Sellingbest&t_page=%EB%9E%AD%ED%82%B9&t_click=%ED%8C%90%EB%A7%A4%EB%9E%AD%ED%82%B9_%EC%8A%A4%ED%82%A8%EC%BC%80%EC%96%B4_%EC%83%81%ED%92%88%EC%83%81%EC%84%B8&t_number=22", 
#                         "caption": "달바 화이트 트러플 퍼스트 스프레이 세럼 100ml"},
#                     {"image_url": "https://image.oliveyoung.co.kr/uploads/images/goods/550/10/0000/0019/A00000019067724ko.jpg?l=ko",
#                         "link_url": "https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000190677&dispCatNo=90000010009&trackingCd=Best_Sellingbest&t_page=%EB%9E%AD%ED%82%B9&t_click=%ED%8C%90%EB%A7%A4%EB%9E%AD%ED%82%B9_%EC%8A%A4%ED%82%A8%EC%BC%80%EC%96%B4_%EC%83%81%ED%92%88%EC%83%81%EC%84%B8&t_number=27", 
#                         "caption": "토리든 다이브인 저분자 히알루론산 수딩 크림 100ml"} 
#                     ]
                
#                 #Expand 창 생성
#                 for image_info in bot_response_images:
#                     image_with_link = f'<a href="{image_info["link_url"]}" target="_blank"><img src="{image_info["image_url"]}" width="200"></a>'
#                     with st.expander(f"{image_info['caption']}"):
#                         chat_message("assistant", content=f"<a href='{image_info['link_url']}' target='_blank'><img src='{image_info['image_url']}' width='200'></a>", avatar='🧙‍♂️')
#                         #st.markdown(image_with_link, unsafe_allow_html=True)
            
#             else:
#                 assistant_response = random.choice([
#                     "Hello there! How can I assist you today?",
#                     "Hi, human! Is there anything I can help you with?",
#                     "Do you need help?",
#                 ])

#                 # Display assistant response in chat message container
#                 message_placeholder = st.empty()

#                 # Simulate stream of response with milliseconds delay
#                 for chunk in assistant_response.split():
#                     full_response += chunk + " "
#                     time.sleep(0.05)
#                     # Add a blinking cursor to simulate typing
#                     message_placeholder.markdown(full_response + "▌")
                    
#                 message_placeholder.markdown(full_response)

#             # Add assistant response to chat history
#             st.session_state.messages.append({"role": "assistant", "content": full_response, "avatar": '🧙‍♂️'})

# # 초기 실행 시에만 messages를 초기화
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# randing()










    # # Initialize chat history
    # if "messages" not in st.session_state:
    #     st.session_state.messages = []

    # # Display chat messages from history on app rerun
    # for message in st.session_state.messages:
    #     with st.chat_message(message["role"]):
    #         st.markdown(message["content"])

    # # Accept user input
    # if prompt := st.chat_input("말만 해요! 이 뽀야미가 해결해줄게요:)"):
    #     # Add user message to chat history
    #     st.session_state.messages.append({"role": "user", "content": prompt})
    #     # Display user message in chat message container
    #     with st.chat_message("user", avatar='👩🏻'):
    #         st.markdown(prompt)

    #     # Display assistant response in chat message container
    #     with st.chat_message("assistant", avatar='🧙‍♂️'):
    #         full_response = ""

    #         if "스킨케어 추천" in prompt:
    #             #이미지 3개
    #             bot_response_images = [
    #                 {"image_url": "https://image.oliveyoung.co.kr/uploads/images/goods/550/10/0000/0019/A00000019835702ko.jpg?l=ko",
    #                     "link_url": "https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000198357&dispCatNo=90000010009&trackingCd=Best_Sellingbest&t_page=%EB%9E%AD%ED%82%B9&t_click=%ED%8C%90%EB%A7%A4%EB%9E%AD%ED%82%B9_%EC%8A%A4%ED%82%A8%EC%BC%80%EC%96%B4_%EC%83%81%ED%92%88%EC%83%81%EC%84%B8&t_number=10", 
    #                     "caption": "라로슈포제 시카플라스트 밤"},
    #                 {"image_url": "https://image.oliveyoung.co.kr/uploads/images/goods/550/10/0000/0017/A00000017131219ko.jpg?l=ko",
    #                     "link_url": "https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000171312&dispCatNo=90000010009&trackingCd=Best_Sellingbest&t_page=%EB%9E%AD%ED%82%B9&t_click=%ED%8C%90%EB%A7%A4%EB%9E%AD%ED%82%B9_%EC%8A%A4%ED%82%A8%EC%BC%80%EC%96%B4_%EC%83%81%ED%92%88%EC%83%81%EC%84%B8&t_number=22", 
    #                     "caption": "달바 화이트 트러플 퍼스트 스프레이 세럼 100ml"},
    #                 {"image_url": "https://image.oliveyoung.co.kr/uploads/images/goods/550/10/0000/0019/A00000019067724ko.jpg?l=ko",
    #                     "link_url": "https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000190677&dispCatNo=90000010009&trackingCd=Best_Sellingbest&t_page=%EB%9E%AD%ED%82%B9&t_click=%ED%8C%90%EB%A7%A4%EB%9E%AD%ED%82%B9_%EC%8A%A4%ED%82%A8%EC%BC%80%EC%96%B4_%EC%83%81%ED%92%88%EC%83%81%EC%84%B8&t_number=27", 
    #                     "caption": "토리든 다이브인 저분자 히알루론산 수딩 크림 100ml"} 
    #                 ]
                
    #             #Expand 창 생성
    #             for image_info in bot_response_images:
    #                 image_with_link = f'<a href="{image_info["link_url"]}" target="_blank"><img src="{image_info["image_url"]}" width="200"></a>'
    #                 with st.expander(f"{image_info['caption']}"):
    #                     st.markdown(image_with_link, unsafe_allow_html=True)
            
    #         else:
    #             assistant_response = random.choice([
    #                 "Hello there! How can I assist you today?",
    #                 "Hi, human! Is there anything I can help you with?",
    #                 "Do you need help?",
    #             ])

    #             # Display assistant response in chat message container
    #             message_placeholder = st.empty()

    #             # Simulate stream of response with milliseconds delay
    #             for chunk in assistant_response.split():
    #                 full_response += chunk + " "
    #                 time.sleep(0.05)
    #                 # Add a blinking cursor to simulate typing
    #                 message_placeholder.markdown(full_response + "▌")
                    
    #             message_placeholder.markdown(full_response)

    #         # Add assistant response to chat history
    #         st.session_state.messages.append({"role": "assistant", "content": full_response})
            
            # 예1) response = requests.get(url="http://localhost:8080/test")
            # response_message = response.json()["response"]
            # assistant_response = response_message


# randing()