import streamlit as st
from webui_pages.utils import *
from webui_pages.music_dialogue.music_dialogue import music_dialogue_page, chat_box
import os
import sys
from configs import VERSION
from server.utils import api_address


api = ApiRequest(base_url=api_address())

if __name__ == "__main__":
    is_lite = "lite" in sys.argv

    st.set_page_config(
        "Music-Chatchat WebUI",
        os.path.join("img", "chatchat_icon_blue_square_v2.png"),
        initial_sidebar_state="expanded",
        menu_items={
            'About': f"""欢迎使用 Music-Chatchat WebUI {VERSION}！"""
        }
    )

    with st.sidebar:
        st.image(
            os.path.join(
                "img",
                "logo-long-chatchat-trans-v2.png"
            ),
            use_column_width=True
        )
        st.caption(
            f"""<p align="right">当前版本：{VERSION}</p>""",
            unsafe_allow_html=True,
        )


    music_dialogue_page(api=api, is_lite=is_lite)
