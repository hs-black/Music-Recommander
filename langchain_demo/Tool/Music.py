import abc
import math
from typing import Any
import requests
import json
import re
import csv
from langchain.tools import BaseTool
import ast
from transformers import AutoTokenizer, AutoModel
import os
import glob

class Music(BaseTool, abc.ABC):
    name = "Music"
    description = "Useful for recommended a list of musics that meets the user's needs"

    def __init__(self):
        super().__init__()

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        # 用例中没有用到 arun 不予具体实现
        pass


    def _run(self, para: str) -> str:
        # response, _ = self.model.chat(self.tokenizer, para, history=[self.system_item1], role=self.role, temperature=0.01, top_p=0.95, top_k=20)
        # print (response)
        r = requests.get(r"http://localhost:3000/search?keywords=" + para + r"&type=1000")
        playlists = r.json()['result']['playlists']
        print (playlists[0]['id'])
        r = requests.get(r"http://localhost:3000/playlist/track/all?id=" + str(playlists[0]['id']) + "&limit=5&offset=1")
        songs = r.json()['songs']
        result = ""
        for song in songs:
            # result += "歌曲名称：" + song["name"] + " 作者：" + ",".join([artist['name'] for artist in song['ar']]) + '\n'
            result += song["name"] + " 歌手： " + ",".join([artist['name'] for artist in song['ar']]) + '\n'
        print (result)
        return result

