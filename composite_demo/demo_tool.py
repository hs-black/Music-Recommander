import json
import re
import time
import yaml
from yaml import YAMLError

import streamlit as st
from streamlit.delta_generator import DeltaGenerator

from client import get_client
from conversation import postprocess_text, preprocess_text, Conversation, Role
from tool_registry import tools, Music_Recommender, client, Online_Music_Searcher

MAX_LENGTH = 8192
TRUNCATE_LENGTH = 1024

# Append a conversation into history, while show it in a new markdown block
def append_conversation(
    conversation: Conversation,
    history: list[Conversation],
    placeholder: DeltaGenerator | None=None,
) -> None:
    history.append(conversation)
    conversation.show(placeholder)

def main(top_p: float, temperature: float, prompt_text: str):
    
    if 'tool_history' not in st.session_state:
        st.session_state.tool_history = []
    if 'messages' not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": "You are smart music AI Assistant. You can find musics that users want."}]

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
        with markdown_placeholder:
            with st.spinner(f'Generating Text ...'):
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo-1106",
                    messages=messages,
                    tools=tools,
                    tool_choice="auto",  # auto is default, but we'll be explicit
                )


        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        # Step 2: check if the model wanted to call a function

        if tool_calls:
            
            with markdown_placeholder:
                with st.spinner(f'Calling tools ...'):
                    available_functions = {
                        "Music_Recommender": Music_Recommender,
                        # "Online_Music_Searcher": Online_Music_Searcher,
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
                            )
                        elif function_name == "Online_Music_Searcher":
                            function_response = function_to_call(
                                Search_text = function_args.get("Search_text", "")
                            )

                        messages.append(
                            {
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": function_name,
                                "content": function_response,
                            }
                        )  # extend conversation with function response
                        response_message = client.chat.completions.create(
                                model="gpt-3.5-turbo-1106",
                                messages=messages,
                            ).choices[0].message
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