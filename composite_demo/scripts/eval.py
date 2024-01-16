import os
import random
import csv
import numpy as np
import sys 
import json
sys.path.append("..") 
from tool_registry import tools, Music_Recommender, client
sys.path.append(os.path.split(os.path.realpath(__file__))[0] + '/../Langchain_Chatchat')
from webui_pages.utils import *
from server.utils import api_address
api = ApiRequest(base_url=api_address())

def Our_Recommender_Full(input):
    messages=[{"role": "system", "content": "You are smart music AI Assistant. You can recommend musics or find music information according to user's need."},
              {"role": "user", "content": input}]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        tools=[tools[0]],
        tool_choice="auto",  # auto is default, but we'll be explicit
        temperature=0.25,
        top_p=0.8
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    # Step 2: check if the model wanted to call a function
    if tool_calls:
        available_functions = {
            "Music_Recommender": Music_Recommender,
        }  # only one function in this example, but you can have multiple
        messages.append(response_message)  # extend conversation with assistant's reply
        # Step 4: send the info for each function call and function response to the model
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
                    choose = 5,
                    prompt = input
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
                temperature=0.25,
                top_p=0.8
            ).choices[0].message
    return response_message.content

def GPT(input):
    chat_completion = client.chat.completions.create(
        messages=[{"role": "system", "content": "You are smart music AI Assistant. You can recommend musics or find music information according to user's need."},
              {"role": "user", "content": input}],
        model="gpt-3.5-turbo-1106",
    )
    output = chat_completion.choices[0].message.content
    return output

def Our_Recommender_no_kb(input):
    messages=[{"role": "system", "content": "You are smart music AI Assistant. You can recommend musics or find music information according to user's need."},
              {"role": "user", "content": input}]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        tools=[tools[0]],
        tool_choice="auto",  # auto is default, but we'll be explicit
        temperature=0.25,
        top_p=0.8
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    # Step 2: check if the model wanted to call a function
    if tool_calls:
        available_functions = {
            "Music_Recommender": Music_Recommender,
        }  # only one function in this example, but you can have multiple
        messages.append(response_message)  # extend conversation with assistant's reply
        # Step 4: send the info for each function call and function response to the model
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
                    choose = 5,
                    prompt = ""
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
                temperature=0.25,
                top_p=0.8
            ).choices[0].message
    return response_message.content

def ChatGLM_with_kb(input):
    messages=[{"role": "system", "content": "You are smart music AI Assistant. You can recommend musics or find music information according to user's need."},
              {"role": "user", "content": input}]
    
    text = ""
    for d in api.knowledge_base_chat(input,
                                    knowledge_base_name="music_new",
                                    top_k=3,
                                    score_threshold=1.0,
                                    history=messages,
                                    model="chatglm3-6b",
                                    prompt_name="default",
                                    temperature=0.25):
        if error_msg := check_error_msg(d):
            return ""
        elif chunk := d.get("answer"):
            text += chunk
    return text
    

funcs = [Our_Recommender_Full, GPT, Our_Recommender_no_kb, ChatGLM_with_kb] # LLM's functions
num_eval = 10 # 测试的数据量
fileDir = "data"
original_tags = ['放松', '助眠', '抒情', '轻快', '快乐', '治愈', '清新', '平静', '学习', '动感', '活力', '极限运动', '梦幻', '冥想', '悲伤', '孤独', '爱情', '思念', '浪漫', '洒脱', '', '可爱', '慵懒', '热血', 'KTV', '正能量', '幸福', '旅游', '酒吧', '抑郁', '婚礼', '大气', '紧张', '神秘', '甜蜜', '亲情', '遗憾', '苦情', '夜店', '有氧', '暴走', '家务', '通勤', '舞蹈', '憧憬', '友情', '感人', '正直', '咖啡厅', '校园', '足球', '愤怒', '激烈', '驾车', '搞笑', '举铁', '烦躁', '黑暗', '散步', '露营', '舞会', '未来感', '瑜伽', '篮球', '惊悚', '高级感', '白噪音', '广场舞']
testFile = "../data/csv_data/data_test.csv"

def random_eval_singer():
    correct_count = np.zeros(len(funcs))
    filenames = os.listdir(fileDir)
    for i in range(num_eval):
        file = random.choice(filenames)
        with open(os.path.join(fileDir, file), 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            rows = [row for row in reader]
        row = random.choice(rows)
        song_name = row[0]
        singer_names = row[1][:-1].split('、')
        input = '歌曲' + song_name + '的歌手是谁？返回2个可能的歌手'
        for j in range(len(funcs)):
            output = funcs[j](input)
            if any (singer_name in output for singer_name in singer_names):
                correct_count[j] += 1
        # print("song_name:", song_name, "singer_names:", singer_names, "output:", output)
    correct_rate = correct_count / num_eval
    print("======eval_singer======")
    for i in range(len(funcs)):
        print(funcs[i].__name__, correct_rate[i])

def random_eval_tag():
    correct_count = np.zeros(len(funcs))
    filenames = os.listdir(fileDir)
    for i in range(num_eval):
        file = random.choice(filenames)
        with open(os.path.join(fileDir, file), 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            rows = [row for row in reader]
        row = random.choice(rows)
        song_name = row[0]
        tags = row[3][:-1].split('、')
        refer_tags = original_tags.copy()
        for tag in tags:
            if tag not in refer_tags:
                refer_tags.append(tag)
        input = '歌曲' + song_name + '的曲风是什么？从' + str(refer_tags) + '中选择2个可能的曲风'
        for j in range(len(funcs)):
            output = funcs[j](input)
            if any (tag in output for tag in tags):
                correct_count[j] += 1
        # print("song_name:", song_name, "tags:", tags, "output:", output)
    correct_rate = correct_count / num_eval
    print("======eval_tag======")
    for i in range(len(funcs)):
        print(funcs[i].__name__, correct_rate[i])

def random_eval_language():
    correct_count = np.zeros(len(funcs))
    filenames = os.listdir(fileDir)
    for i in range(num_eval):
        file = random.choice(filenames)
        with open(os.path.join(fileDir, file), 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            rows = [row for row in reader]
        row = random.choice(rows)
        song_name = row[0]
        language = row[4].split('、')
        language_list = ['华语', '日语', '韩语', '英语', '纯音乐', '其他语言']
        processed_language = []
        for lang in language:
            if lang in language_list:
                processed_language.append(lang)
            elif lang == '粤语' or lang == '国语':
                processed_language.append('华语')
            else:
                processed_language.append('其他语言')
        input = '歌曲' + song_name + '的语种是什么？\'国语\'、\'粤语\'均被认为是\'华语\'，从' + str(language_list) + '中选择1个最可能的语种'
        for j in range(len(funcs)):
            output = funcs[j](input)
            if any (lang in output for lang in processed_language):
                correct_count[j] += 1
        # print("song_name:", song_name, "language:", processed_language, "output:", output)
    correct_rate = correct_count / num_eval
    print("======eval_language======")
    for i in range(len(funcs)):
        print(funcs[i].__name__, correct_rate[i])


def eval_singer():
    correct_count = np.zeros(len(funcs))
    with open(testFile, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        error_count = [0 for i in range(len(funcs))]
        for row in reader:
            song_name = row[0]
            singer_names = row[1][:-1].split('、')
            input = '歌曲' + song_name + '的歌手是谁？返回2个可能的歌手'
            for j in range(len(funcs)):
                attempts = 0
                while attempts < 10:
                    try:
                        output = funcs[j](input)
                        break
                    except:
                        print("error")
                        output = ""
                        attempts += 1
                if attempts == 10:
                    error_count[j] += 1
                if any (singer_name in output for singer_name in singer_names):
                    correct_count[j] += 1
                print("Eval singer, song_name:", song_name, "model", funcs[j].__name__, "correct_count", correct_count[j])
                print("output", output)
    correct_rate = correct_count / 100
    with open("eval_singer_output.txt", 'w', encoding='utf-8') as f:
        f.write("======eval_singer======\n")
        for i in range(len(funcs)):
            f.write(funcs[i].__name__ + " " + str(correct_rate[i]) + "\n")
            f.write("error_count " + funcs[i].__name__ + " " + str(error_count[i]) + "\n")
    print("======eval_singer======")
    for i in range(len(funcs)):
        print(funcs[i].__name__, correct_rate[i])

def eval_tag():
    correct_count = np.zeros(len(funcs))
    with open(testFile, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        error_count = [0 for i in range(len(funcs))]
        for row in reader:
            song_name = row[0]
            tags = row[3][:-1].split('、')
            refer_tags = original_tags.copy()
            for tag in tags:
                if tag not in refer_tags:
                    refer_tags.append(tag)
            refer_tags = ['抒情', '悲伤', '快乐', '爱情', '思念', '孤独', '轻快', '遗憾', '甜蜜', '清新', '动感', '幸福', '紧张', '平静', '梦幻', '抑郁', '慵懒', '浪漫', '苦情', '活力', '放松', '憧憬', '治愈', '神秘', 'KTV', '酒吧', '黑暗', '洒脱', '正能量', '激烈', '友情', '有氧', '感人', '家务', '亲情', '热血', '学习', '正直', '烦躁', '大气', '惊悚', '可爱', '通勤', '极限运动', '婚礼', '散步', '旅游']
            input = '歌曲' + song_name + '的推荐标签是什么？从' + str(refer_tags) + '中选出最可能的1个推荐标签'
            for j in range(len(funcs)):
                attempts = 0
                while attempts < 10:
                    try:
                        output = funcs[j](input)
                        break
                    except:
                        print("error")
                        output = ""
                        attempts += 1
                if attempts == 10:
                    error_count[j] += 1
                if any (tag in output for tag in tags):
                    correct_count[j] += 1
                print("Eval tag, song_name:", song_name, "model", funcs[j].__name__, "correct_count", correct_count[j])
                print("output", output)
    correct_rate = correct_count / 100
    with open("eval_tag_output.txt", 'w', encoding='utf-8') as f:
        f.write("======eval_tag======\n")
        for i in range(len(funcs)):
            f.write(funcs[i].__name__ + " " + str(correct_rate[i]) + "\n")
            f.write("error_count " + funcs[i].__name__ + " " + str(error_count[i]) + "\n")
    print("======eval_tag======")
    for i in range(len(funcs)):
        print(funcs[i].__name__, correct_rate[i])

def eval_language():
    correct_count = np.zeros(len(funcs))
    with open(testFile, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        error_count = [0 for i in range(len(funcs))]
        for row in reader:
            song_name = row[0]
            language = row[4].split('、')
            language_list = ['华语', '日语', '韩语', '英语', '纯音乐', '其他语言']
            processed_language = []
            for lang in language:
                if lang in language_list:
                    processed_language.append(lang)
                elif lang == '粤语' or lang == '国语':
                    processed_language.append('华语')
                else:
                    processed_language.append('其他语言')
            input = '歌曲《' + song_name + '》的语种是什么？从' + str(language_list) + '中选择1个最可能的语种'
            for j in range(len(funcs)):
                attempts = 0
                while attempts < 10:
                    try:
                        output = funcs[j](input).replace("国语", "华语").replace("粤语", "华语").replace("普通话", "华语")
                        break
                    except:
                        print("error")
                        output = ""
                        attempts += 1
                if attempts == 10:
                    error_count[j] += 1
                # output = funcs[j](input)
                if any (lang in output for lang in processed_language):
                    correct_count[j] += 1
                print("Eval language, song_name:", song_name, "model", funcs[j].__name__, "correct_count", correct_count[j])
                print("output", output)
    correct_rate = correct_count / 100
    with open("eval_language_output.txt", 'w', encoding='utf-8') as f:
        f.write("======eval_language======\n")
        for i in range(len(funcs)):
            f.write(funcs[i].__name__ + " " + str(correct_rate[i]) + "\n")
            f.write("error_count " + funcs[i].__name__ + " " + str(error_count[i]) + "\n")
    print("======eval_language======")
    for i in range(len(funcs)):
        print(funcs[i].__name__, correct_rate[i])


if __name__ == "__main__":
    eval_singer()
    eval_tag()
    # eval_language()