import json
import requests

import streamlit as st
from streamlit.delta_generator import DeltaGenerator

proxies = {
  "http": None,
  "https": None,
}

from conversation import Conversation, Role
from tool_registry import tools, Music_Recommender, client

MAX_LENGTH = 8192
TRUNCATE_LENGTH = 1024

def MusicPlay(MusicName, ArtistName):
    print(MusicName, ArtistName)
    
    r = requests.get(f"http://localhost:3000/search?keywords={MusicName} {ArtistName}", proxies = proxies)
    tid = r.json()['result']['songs'][0]['id']
    print (tid)
    r = requests.get(f"http://localhost:3000/song/url/v1?id={tid}&level=exhigh", proxies = proxies)
    url = r.json()['data'][0]['url']
    print (url)
    return url

# Append a conversation into history, while show it in a new markdown block
def append_conversation(
    conversation: Conversation,
    history: list[Conversation],
    placeholder: DeltaGenerator | None=None,
) -> None:
    history.append(conversation)
    conversation.show(placeholder)

def main(top_p: float, temperature: float, choose, prompt_text: str):
    
    if 'tool_history' not in st.session_state:
        st.session_state.tool_history = []
    if 'messages' not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": "You are smart music AI Assistant. You can find musics that users want. 并给出推荐和介绍"}]

    history: list[Conversation] = st.session_state.tool_history
    messages: list[dict] = st.session_state.messages

    for conversation in history:
        conversation.show()

    if prompt_text:
        prompt_text = prompt_text.strip()
        append_conversation(Conversation(Role.USER, prompt_text), history)
        
        placeholder = st.container()
        message_placeholder = placeholder.chat_message(name="assistant", avatar="assistant")
        markdown_placeholder = message_placeholder.empty()

        messages.append({"role": "user", "content": prompt_text})

        print(messages)
        with markdown_placeholder:
            with st.spinner(f'Generating Text ...'):
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo-1106",
                    messages=messages,
                    tools=[tools[0]],
                    tool_choice="auto",  # auto is default, but we'll be explicit
                    temperature=temperature,
                    top_p=top_p
                )


        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        # Step 2: check if the model wanted to call a function
        PlayAudio = None
        if tool_calls:
            
            with markdown_placeholder:
                with st.spinner(f'Calling tools ...'):
                    available_functions = {
                        "Music_Recommender": Music_Recommender,
                        "MusicPlay": MusicPlay,
                    }  # only one function in this example, but you can have multiple
                    messages.append(response_message)  # extend conversation with assistant's reply
                    # Step 4: send the info for each function call and function response to the model
                    print (f"toolcall is {tool_calls}")
                    for tool_call in tool_calls:
                        function_name = tool_call.function.name
                        function_to_call = available_functions[function_name]
                        function_args = json.loads(tool_call.function.arguments)
                        if function_name == "Music_Recommender":
                            function_response = function_to_call(
                                music_number = function_args.get("music_number", 8),
                                music_name = function_args.get("music_name", None),
                                artist_name = function_args.get("artist_name", None),
                                language = function_args.get("language", None),
                                genre = function_args.get("genre", None),
                                scene = function_args.get("scene", None),
                                motion = function_args.get("motion", None),
                                music_instrument = function_args.get("music_instrument", None),
                                query = function_args.get("query", ""),
                                other = function_args.get("other", None),
                                choose = choose
                            )

                        messages.append(
                            {
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": function_name,
                                "content": function_response,
                            }
                        )  # extend conversation with function response

                    print("M", messages)
                    response_message = client.chat.completions.create(
                            model="gpt-3.5-turbo-1106",
                            messages=messages,
                            temperature=temperature,
                            top_p=top_p
                        ).choices[0].message
                    print("R", response_message)
                    PlayAudio = client.chat.completions.create(
                            model="gpt-3.5-turbo-1106",
                            messages=[
                                {"role": "system", "content": "You are AI Audio Player, 从用户的输入中找到音乐的名字和歌手的名字，并调用工具 MusicPlay 来生成播放按钮"},
                                {"role": "user", "content": response_message.content}
                                ],
                            tools=[tools[1]],
                            tool_choice='auto',
                            temperature=temperature,
                            top_p=top_p
                        ).choices[0].message
                     
                    print(response_message)

        messages.append(
                            {
                                "role": "assistant",
                                "content": response_message.content,
                            }
                        )
        append_conversation(Conversation(
                                Role.ASSISTANT,
                                response_message.content,
                            ), history, markdown_placeholder)
        
        if PlayAudio:
            tool_calls = PlayAudio.tool_calls
        
        if tool_calls:
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                if function_name == "MusicPlay":
                    placeholder = st.container()
                    message_placeholder = placeholder.chat_message(name="assistant", avatar="assistant")
                    markdown_placeholder = message_placeholder.empty()
                    function_response = function_to_call(
                        MusicName = function_args.get("MusicName", "杀死那个石家庄人"),
                        ArtistName = function_args.get("ArtistName", "万能青年旅店"),
                    )
                    append_conversation(Conversation(
                                            Role.ASSISTANT,
                                            response_message.content,
                                            function_response
                                        ), history, markdown_placeholder)
