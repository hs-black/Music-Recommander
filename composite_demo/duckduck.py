#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os,json
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from openai import OpenAI
from langchain.utilities import BingSearchAPIWrapper
import requests

os.environ["OPENAI_API_KEY"] = "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"
os.environ["BING_SUBSCRIPTION_KEY"] = "a24d675d518c4e0a9707ab9d34d75ea2"
os.environ["BING_SEARCH_URL"] = "https://api.bing.microsoft.com/v7.0/search"
client = OpenAI()


# In[3]:


tools = [
        {
            "type": "function",
            "function": {
                "name": "Music_Recommender",
                "description": "Useful for recommending a list of musics that meets the user's needs",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "music_number": {
                            "type": "number",
                            "description": "推荐数量（阿拉伯数字）",
                        },
                        "music_name": {
                            "type": "string",
                            "description": "歌曲名（海阔天空，同桌的你等）",
                        },
                        "artist_name": {
                            "type": "string",
                            "description": "歌手名（周杰伦，刘若英等）",
                        },
                        "language": {
                            "type": "string",
                            "description": "歌曲语种（粤语，英语，德语，华语等）",
                        },
                        "genre": {
                            "type": "string",
                            "description": "歌曲风格（流行，摇滚，R&B，布鲁斯，电子等）",
                        },
                        "scene": {
                            "type": "string",
                            "description": "歌曲适用场景（清晨，夜晚，运动，学习，工作等）",
                        },
                        "motion": {
                            "type": "string",
                            "description": "歌曲情感（怀旧，浪漫，放松，伤感，快乐等）",
                        },
                        "music_instrument": {
                            "type": "string",
                            "description": "歌曲主要乐器（钢琴，大提琴，小提琴，吉他等）",
                        },
                        "other": {
                            "type": "string",
                            "description": "其他关键词（某榜单，某综艺，某游戏，某电影等）",
                        },
                    },
                    "required": ["music_number"],
                },
            },
        }
    ]


# In[7]:


def Music_Recommender(
    music_number,
    music_name,
    artist_name,
    language,
    genre,
    scene,
    motion,
    music_instrument,
    other,
) -> str:
    """
    Useful for recommending a list of musics that meets the user's needs。
    """
    result = ""
    art = 'ar'
    if music_name or artist_name:
        para = ""
        if music_name:
            para += music_name + " "
        if artist_name:
            para += artist_name
        r = requests.get(r"http://localhost:3000/search?keywords=" + para)
        songs = r.json()['result']['songs']
        art = 'artists'    
        query = para + "歌曲"
        search = BingSearchAPIWrapper(k=50)
        sresult = search.run(query).replace("<b>", "").replace("</b>", "")
        if len(result) > 1950:
            sresult = sresult[:1950]

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "我从网络上搜索了一些资料，请你从下面的搜索结果中总结" + 
                    query + "，如果能找到相关信息，告诉我这首歌的正确歌名（如果有，下同），正确作者，风格，乐器，语种，情感，和其他相关的信息，如果有不符合描述的地方请你解释：\n" + sresult,
                }
            ],
            model="gpt-3.5-turbo-1106",
        )
        result += "下面是网络的搜索结果：\n" + chat_completion.choices[0].message.content + "\n"
    else:
        para = ""
        if music_instrument:
            para += music_instrument + " "
        if language:
            para += language + " "
        if genre:
            para += genre + " "
        if scene:
            para += scene + " "
        if motion:
            para += motion + " "
        if other:
            para += other + " "
        r = requests.get(r"http://localhost:3000/search?keywords=" + para + r"&type=1000")
        playlists = r.json()['result']['playlists']
        r = requests.get(r"http://localhost:3000/playlist/track/all?id=" + str(playlists[0]['id']) + "&limit=50&offset=1")
        songs = r.json()['songs']
    result += "下面是网易云的搜索结果：\n"
    for song in songs[:min(len(songs), 2 * music_number)]:
#         search = BingSearchAPIWrapper(k=50)
#         sresult = search.run(query).replace("<b>", "").replace("</b>", "")
#         if len(result) > 1950:
#             sresult = sresult[:1950]

#         chat_completion = client.chat.completions.create(
#             messages=[
#                 {
#                     "role": "user",
#                     "content": "我从网络上搜索了一些资料，请你从下面的搜索结果中总结" + 
#                     query + "，如果能找到相关信息，告诉我这首歌的正确歌名（如果有，下同），正确作者，风格，乐器，语种，情感，和其他相关的信息：\n" + sresult,
#                 }
#             ],
#             model="gpt-3.5-turbo-1106",
#         )
#         result += "下面是网络的搜索结果：\n" + chat_completion.choices[0].message.content + "\n"
        
        result += song["name"] + "  歌手：" + ",".join([artist['name'] for artist in song[art]]) + r"  歌曲链接：https://music.163.com/#/song?id=" + str(song['id']) + '\n'
    # print (result)
    return result


# In[8]:


def search(messages):
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
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "Music_Recommender": Music_Recommender,
        }  # only one function in this example, but you can have multiple
        messages.append(response_message)  # extend conversation with assistant's reply
        # Step 4: send the info for each function call and function response to the model
        # print (f"toolcall is {tool_calls}")
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                music_number = function_args.get("music_number", 8),
                music_name = function_args.get("music_name", None),
                artist_name = function_args.get("artist_name", None),
                language = function_args.get("language", None),
                genre = function_args.get("genre", None),
                scene = function_args.get("scene", None),
                motion = function_args.get("motion", None),
                music_instrument = function_args.get("music_instrument", None),
                other = function_args.get("other", None),
            )
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function response
        second_response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
        )  # get a new response from the model where it can see the function response
        # print(messages)
        return second_response


# In[9]:


# result = search(messages = [{"role": "user", "content": "推荐2首日语歌"}])


# # In[10]:


# print(result.choices[0].message.content)


# In[ ]:




