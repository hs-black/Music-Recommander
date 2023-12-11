from enum import Enum
import streamlit as st

st.set_page_config(
    page_title="ChatGLM3 Music Recommender",
    page_icon=":robot:",
    layout='centered',
    initial_sidebar_state='expanded',
)

import demo_chat, demo_ci, demo_tool

DEFAULT_SYSTEM_PROMPT = '''
You are ChatGLM3, a large language model trained by Zhipu.AI. Follow the user's instructions carefully.
'''.strip()

class Mode(str, Enum):
    Music_Recommender = '💬 Music Recommender'


with st.sidebar:
    top_p = st.slider(
        'top_p', 0.0, 1.0, 0.8, step=0.01
    )
    temperature = st.slider(
        'temperature', 0.0, 1.5, 0.95, step=0.01
    )
    system_prompt = st.text_area(
        label="System Prompt (Only for chat mode)",
        height=300,
        value=DEFAULT_SYSTEM_PROMPT,
    )

st.title("ChatGLM3 Music Recommander")

prompt_text = st.chat_input(
    'Get music recommendation with ChatGLM3!',
    key='chat_input',
)

demo_tool.main(top_p, temperature, prompt_text)
