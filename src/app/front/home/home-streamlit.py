# 가영님
import streamlit as st
import random
import time
import requests

def randing():
   
    with st.sidebar:
        openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
        "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
        "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
        "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

    st.title("깨끗하게 맑게 자신있게!")
    st.caption("피부요정 뽀야미에게 맡겨만 주세요!")

    with st.form(key='columns_in_form'):
        age, gender, skin_type, skin_concern = st.columns(4)

        age_selected = age.selectbox('나이', ['10대', '20대', '30대', '40대', '50대', '60대'], key='나이')
        gender_selected = gender.selectbox('성별', ['남', '여'], key='성별')
        skin_type_selected = skin_type.selectbox('피부타입', ['악건성', '건성', '중성·복합성', '지성', '민감성'], key='피부타입')
        skin_concern_selected = skin_concern.selectbox('피부고민', ['여드름', '홍조', '모공', '각질', '블랙헤드', '요철'], key='피부고민')

        submitted = st.form_submit_button('제출')

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content":"당신의 피부고민은 무엇인가요?"])

    # Accept user input
    if prompt := st.chat_input("말만 해요! 이 뽀야미가 해결해줄게요:)"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            response = requests.get(url="http://localhost:8080/test")
            response_message = response.json()["response"]
            # assistant_response = random.choice(
            #     [
            #         "Hello there! How can I assist you today?",
            #         "Hi, human! Is there anything I can help you with?",
            #         "Do you need help?",
            #     ]
            # )
            assistant_response = response_message
            # Simulate stream of response with milliseconds delay
            for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role":    "assistant", "content": full_response})

randing()