from copy import deepcopy
import inspect
from pprint import pformat
import traceback
from types import GenericAlias
from typing import get_origin, Annotated
import requests
import json

from typing import List
from ChatGLM3 import ChatGLM3

from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType

_TOOL_HOOKS = {}
_TOOL_DESCRIPTIONS = {}

def register_tool(func: callable):
    tool_name = func.__name__
    tool_description = inspect.getdoc(func).strip()
    python_params = inspect.signature(func).parameters
    tool_params = []
    for name, param in python_params.items():
        annotation = param.annotation
        if annotation is inspect.Parameter.empty:
            raise TypeError(f"Parameter `{name}` missing type annotation")
        if get_origin(annotation) != Annotated:
            raise TypeError(f"Annotation type for `{name}` must be typing.Annotated")
        
        typ, (description, required) = annotation.__origin__, annotation.__metadata__
        typ: str = str(typ) if isinstance(typ, GenericAlias) else typ.__name__
        if not isinstance(description, str):
            raise TypeError(f"Description for `{name}` must be a string")
        if not isinstance(required, bool):
            raise TypeError(f"Required for `{name}` must be a bool")

        tool_params.append({
            "name": name,
            "description": description,
            "type": typ,
            "required": required
        })
    tool_def = {
        "name": tool_name,
        "description": tool_description,
        "params": tool_params
    }

    print("[registered tool] " + pformat(tool_def))
    _TOOL_HOOKS[tool_name] = func
    _TOOL_DESCRIPTIONS[tool_name] = tool_def

    return func

def dispatch_tool(tool_name: str, tool_params: dict) -> str:
    if tool_name not in _TOOL_HOOKS:
        return f"Tool `{tool_name}` not found. Please use a provided tool."
    tool_call = _TOOL_HOOKS[tool_name]
    try:
        ret = tool_call(**tool_params)  
    except:
        ret = traceback.format_exc()
    return str(ret)

def get_tools() -> dict:
    return deepcopy(_TOOL_DESCRIPTIONS)

# Tool Definitions

@register_tool
def random_number_generator(
    seed: Annotated[int, 'The random seed used by the generator', True], 
    range: Annotated[tuple[int, int], 'The range of the generated numbers', True],
) -> int:
    """
    Generates a random number x, s.t. range[0] <= x < range[1]
    """
    if not isinstance(seed, int):
        raise TypeError("Seed must be an integer")
    if not isinstance(range, tuple):
        raise TypeError("Range must be a tuple")
    if not isinstance(range[0], int) or not isinstance(range[1], int):
        raise TypeError("Range must be a tuple of integers")

    import random
    return random.Random(seed).randint(*range)

@register_tool
def get_weather(
    city_name: Annotated[str, 'The name of the city to be queried', True],
) -> str:
    """
    Get the current weather for `city_name`
    """

    if not isinstance(city_name, str):
        raise TypeError("City name must be a string")

    key_selection = {
        "current_condition": ["temp_C", "FeelsLikeC", "humidity", "weatherDesc",  "observation_time"],
    }
    import requests
    try:
        resp = requests.get(f"https://wttr.in/{city_name}?format=j1")
        resp.raise_for_status()
        resp = resp.json()
        ret = {k: {_v: resp[k][0][_v] for _v in v} for k, v in key_selection.items()}
    except:
        import traceback
        ret = "Error encountered while fetching weather data!\n" + traceback.format_exc() 

    return str(ret)



@register_tool
def Music_Recommender(
    music_number: Annotated[int, '推荐数量（阿拉伯数字）', True] = 8,
    music_name: Annotated[str, '歌曲名（海阔天空，同桌的你等）', False] = None,
    artist_name: Annotated[str, '歌手名（周杰伦，刘若英等）', False]= None,
    language: Annotated[str, '歌曲语种（粤语，英语，德语，华语等）', False]= None,
    genre: Annotated[str, '歌曲风格（流行，摇滚，R&B，布鲁斯，电子等）', False]= None,
    scene: Annotated[str, '歌曲适用场景（清晨，夜晚，运动，学习，工作等）', False]= None,
    motion: Annotated[str, '歌曲情感（怀旧，浪漫，放松，伤感，快乐等）', False]= None,
    music_instrument: Annotated[str, '歌曲主要乐器（钢琴，大提琴，小提琴，吉他等）', False]= None,
    other: Annotated[str, '其他关键词（某榜单，某综艺，某游戏，某电影等）', False]= None,
) -> str:
    """
    Useful for recommending a list of musics that meets the user's needs。
    """
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
    else:
        para = ""
        if language:
            para += language + " "
        if genre:
            para += genre + " "
        if scene:
            para += scene + " "
        if motion:
            para += motion + " "
        if music_instrument:
            para += music_instrument + " "
        if other:
            para += other + " "
        r = requests.get(r"http://localhost:3000/search?keywords=" + para + r"&type=1000")
        playlists = r.json()['result']['playlists']
        r = requests.get(r"http://localhost:3000/playlist/track/all?id=" + str(playlists[0]['id']) + "&limit=50&offset=1")
        songs = r.json()['songs']
    result = ""
    for song in songs[:min(len(songs),2*music_number)]:
        result += song["name"] + "  歌手：" + ",".join([artist['name'] for artist in song[art]]) + r"  歌曲链接：https://music.163.com/#/song?id=" + str(song['id']) + '\n'
    print (result)
    

    # calculator: 单个工具调用示例 3
    # llm = OpenAI(temperature=0)  
    # tools = load_tools(["ddg-search"], llm=llm) 
    # agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True) 
    # agent.run("南昌明天多少度? 这个数的0.23次方是多少？我需要中文的输出结果")
    return result

if __name__ == "__main__":
    print(dispatch_tool("get_weather", {"city_name": "beijing"}))
    print(get_tools())
