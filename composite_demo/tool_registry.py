import os, json
from openai import OpenAI
from langchain.utilities import BingSearchAPIWrapper
import requests

os.environ["OPENAI_API_KEY"] = "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"
os.environ["BING_SUBSCRIPTION_KEY"] = "a24d675d518c4e0a9707ab9d34d75ea2"
os.environ["BING_SEARCH_URL"] = "https://api.bing.microsoft.com/v7.0/search"
client = OpenAI()

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
                        "query": {
                            "type": "string",
                            "description": "需要搜索的信息，直接从网络搜索这个文本，比如'鸡你太美是什么歌?','歌词包含就这样被你征服，是什么歌'",
                        },
                        "other": {
                            "type": "string",
                            "description": "其他关键词（某榜单，某综艺，某游戏，某电影等）",
                        },
                    },
                    "required": ["music_number", "query"],
                },
            },
        }

        # {
        #     "type": "function",
        #     "function": {
        #         "name": "Online_Music_Searcher",
        #         "description": "从网络上获取信息，直接搜索给定的信息",
        #         "parameters": {
        #             "type": "object",
        #             "properties": {
        #                 "Search_text": {
        #                     "type": "string",
        #                     "description": "需要搜索的信息，直接从网络搜索这个文本，比如“鸡你太美是什么歌？”，“歌词包含“就这样被你征服”，那英的，是什么歌”",
        #                 },
        #             },
        #             "required": [],
        #         },
        #     },
        # }
    ]


def Music_Recommender(
    music_number,
    music_name,
    artist_name,
    language,
    genre,
    scene,
    motion,
    music_instrument,
    query,
    other,
) -> str:
    """
    Useful for recommending a list of musics that meets the user's needs。
    """
    result = ""
    art = 'ar'
    songs = []
    if music_name or artist_name:
        para = ""
        if music_name:
            para += music_name + " "
        if artist_name:
            para += artist_name
        r = requests.get(r"http://localhost:3000/search?keywords=" + para)
        songs = r.json()['result']['songs']
        art = 'artists'   
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
        if para:
            r = requests.get(r"http://localhost:3000/search?keywords=" + para + r"&type=1000")
            playlists = r.json()['result']['playlists']
            r = requests.get(r"http://localhost:3000/playlist/track/all?id=" + str(playlists[0]['id']) + "&limit=50&offset=1")
            songs = r.json()['songs']
    if query:
        search = BingSearchAPIWrapper(k=50)
        sresult = search.run(query).replace("<b>", "").replace("</b>", "")
        if len(sresult) > 1950:
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
    if songs:
        result += "下面是网易云的搜索结果：\n"
        for i, song in enumerate(songs[:min(len(songs), 2 * music_number)]):
            search = BingSearchAPIWrapper(k=50)
            sresult = search.run(query).replace("<b>", "").replace("</b>", "")
            if len(result) > 1950:
                sresult = sresult[:1950]
            query = song['name'] + " " + song[art][0]['name'] + "歌曲"
            result += "歌曲" + str(i) + ": "+ song["name"] + "  歌手：" + ",".join([artist['name'] for artist in song[art]]) + " "
            
            r = requests.get(r"http://localhost:3000/search?keywords=" + para + r"&type=1000")
            playlists = r.json()['result']['playlists']
            r = requests.get(r"http://localhost:3000/playlist/track/all?id=" + str(playlists[0]['id']) + "&limit=50&offset=1")
            songs = r.json()['songs']
            result += "歌曲" + str(i) + ": "+ song["name"] + "  歌手：" + ",".join([artist['name'] for artist in song[art]]) + " "
    return result



def Online_Music_Searcher(
   Search_text
) -> str:
    """
    Useful for recommending a list of musics that meets the user's needs。
    """
    search = BingSearchAPIWrapper(k=50)
    sresult = search.run(Search_text).replace("<b>", "").replace("</b>", "")
    if len(sresult) > 1950:
        sresult = sresult[:1950]

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "我从网络上搜索了一些资料，请你从下面的搜索结果中总结我的问题：" + 
                Search_text + "，如果能找到相关信息，告诉我这首歌的正确歌名（如果有，下同），正确作者，风格，乐器，语种，情感，和其他相关的信息，如果有不符合描述的地方请你解释：\n" + sresult,
            }
        ],
        model="gpt-3.5-turbo-1106",
    )
    return chat_completion.choices[0].message.content
