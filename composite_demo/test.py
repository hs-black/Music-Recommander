import requests
import json
functions = [{
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
    }]

samples = []
samples.append({
    "messages": [
        {'role': 'system', 'content': 'You are smart music AI Assistant. You can find musics that users want. 并给出推荐和介绍'},
        {'role': 'user', 'content': '请推荐一首SHE的歌曲'},
        {"role": "assistant", "function_call": {"name": "Music_Recommender", "arguments": "{\"music_number\":1,\"artist_name\":\"SHE\",\"query\":\"SHE的歌曲\"}"}}
    ],
    "functions": functions
})

samples.append({
    "messages": [
        {'role': 'system', 'content': 'You are smart music AI Assistant. You can find musics that users want. 并给出推荐和介绍'},
        {'role': 'user', 'content': '帮我找两首陈奕迅的粤语歌曲, 要伤感的'},
        {"role": "assistant", "function_call": {"name": "Music_Recommender", "arguments": "{\"music_number\":2,\"artist_name\":\"陈奕迅\", \"motion\":\"伤感\",\"query\":\"陈奕迅的伤感粤语歌曲\"}"}}
    ],
    "functions": functions
})

samples.append({
    "messages": [
        {'role': 'system', 'content': 'You are smart music AI Assistant. You can find musics that users want. 并给出推荐和介绍'},
        {'role': 'user', 'content': '请你推荐三首周杰伦的华语歌曲, 要放松的学习时候听的'},
        {"role": "assistant", "function_call": {"name": "Music_Recommender", "arguments": "{\"music_number\":3,\"artist_name\":\"周杰伦\", \"motion\":\"放松\", \"scene\":\"学习\", \"query\":\"周杰伦的华语歌曲, 适合放松学习\"}"}}
    ],
    "functions": functions
})

samples.append({
    "messages": [
        {'role': 'system', 'content': 'You are smart music AI Assistant. You can find musics that users want. 并给出推荐和介绍'},
        {'role': 'user', 'content': '请推荐五首大提琴曲'},
        {"role": "assistant", "function_call": {"name": "Music_Recommender", "arguments": "{\"music_number\":5,\"music_instrument\":\"大提琴\",\"query\":\"著名的大提琴曲\"}"}}
    ],
    "functions": functions
})

samples.append({
    "messages": [
        {'role': 'system', 'content': 'You are smart music AI Assistant. You can find musics that users want. 并给出推荐和介绍'},
        {'role': 'user', 'content': '请推荐一首在电影《你的名字》中出现的插曲'},
        {"role": "assistant", "function_call": {"name": "Music_Recommender", "arguments": "{\"music_number\":1,\"query\":\"电影《你的名字》中出现的插曲\",\"other\":\"你的名字\"}"}}
    ],
    "functions": functions
})

samples.append({
    "messages": [
        {'role': 'system', 'content': 'You are smart music AI Assistant. You can find musics that users want. 并给出推荐和介绍'},
        {'role': 'user', 'content': '请推荐一首SHE的歌曲'},
        {"role": "assistant", "function_call": {"name": "Music_Recommender", "arguments": "{\"music_number\":1,\"artist_name\":\"SHE\",\"query\":\"SHE的歌曲\"}"}}
    ],
    "functions": functions
})

samples.append({
    "messages": [
        {'role': 'system', 'content': 'You are smart music AI Assistant. You can find musics that users want. 并给出推荐和介绍'},
        {'role': 'user', 'content': '帮我找两首陈奕迅的粤语歌曲, 要伤感的'},
        {"role": "assistant", "function_call": {"name": "Music_Recommender", "arguments": "{\"music_number\":2,\"artist_name\":\"陈奕迅\", \"motion\":\"伤感\",\"query\":\"陈奕迅的伤感粤语歌曲\"}"}}
    ],
    "functions": functions
})

samples.append({
    "messages": [
        {'role': 'system', 'content': 'You are smart music AI Assistant. You can find musics that users want. 并给出推荐和介绍'},
        {'role': 'user', 'content': '请你推荐三首周杰伦的华语歌曲, 要放松的学习时候听的'},
        {"role": "assistant", "function_call": {"name": "Music_Recommender", "arguments": "{\"music_number\":3,\"artist_name\":\"周杰伦\", \"motion\":\"放松\", \"scene\":\"学习\", \"query\":\"周杰伦的华语歌曲, 适合放松学习\"}"}}
    ],
    "functions": functions
})

samples.append({
    "messages": [
        {'role': 'system', 'content': 'You are smart music AI Assistant. You can find musics that users want. 并给出推荐和介绍'},
        {'role': 'user', 'content': '请推荐五首大提琴曲'},
        {"role": "assistant", "function_call": {"name": "Music_Recommender", "arguments": "{\"music_number\":5,\"music_instrument\":\"大提琴\",\"query\":\"著名的大提琴曲\"}"}}
    ],
    "functions": functions
})

samples.append({
    "messages": [
        {'role': 'system', 'content': 'You are smart music AI Assistant. You can find musics that users want. 并给出推荐和介绍'},
        {'role': 'user', 'content': '请推荐一首在电影《你的名字》中出现的插曲'},
        {"role": "assistant", "function_call": {"name": "Music_Recommender", "arguments": "{\"music_number\":1,\"query\":\"电影《你的名字》中出现的插曲\",\"other\":\"你的名字\"}"}}
    ],
    "functions": functions
})

with open("dataset.jsonl", "w") as file:
	t = 1

for sample in samples:
	json_sample = json.dumps(sample, ensure_ascii=False)

	with open("dataset.jsonl", "a", encoding='utf-8') as file:
		file.write(json_sample)
		file.write('\n')