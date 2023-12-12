from enum import Enum
import streamlit as st

st.set_page_config(
    page_title="ChatGLM3 Music Recommender",
    page_icon=":robot:",
    layout='centered',
    initial_sidebar_state='expanded',
)

import demo_tool

with st.sidebar:
    top_p = st.slider(
        'top_p', 0.0, 1.0, 0.8, step=0.01
    )
    temperature = st.slider(
        'temperature', 0.0, 1.5, 0.95, step=0.01
    )

st.title("ChatGLM3 Music Recommander")

prompt_text = st.chat_input(
    'Get music recommendation with ChatGLM3!',
    key='chat_input',
)

demo_tool.main(top_p, temperature, prompt_text)