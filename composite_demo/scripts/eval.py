import os
import random
import csv
import numpy as np
import sys 
import json
sys.path.append("..") 
from tool_registry import tools, Music_Recommender, client

def Our_Recommender(input):
    messages=[{"role": "system", "content": "You are smart music AI Assistant. You can find musics that users want. 并给出推荐和介绍"},
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
                    choose = 5
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
        
def ChatGPT(input):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": input,
            }
        ],
        model="gpt-3.5-turbo-1106",
    )
    output = chat_completion.choices[0].message.content
    return output

funcs = [Our_Recommender, ChatGPT] # LLM's functions
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
        for row in reader:
            song_name = row[0]
            singer_names = row[1][:-1].split('、')
            input = '歌曲' + song_name + '的歌手是谁？返回2个可能的歌手'
            for j in range(len(funcs)):
                attempts = 0
                while attempts < 5:
                    try:
                        output = funcs[j](input)
                        break
                    except:
                        attempts += 1
                if any (singer_name in output for singer_name in singer_names):
                    correct_count[j] += 1
                print("Eval singer, song_name:", song_name, "model", funcs[j].__name__, "correct_count", correct_count[j])
    correct_rate = correct_count / num_eval
    with open("output.txt", 'w', encoding='utf-8') as f:
        f.write("======eval_singer======\n")
        for i in range(len(funcs)):
            f.write(funcs[i].__name__ + " " + str(correct_rate[i]) + "\n")
    print("======eval_singer======")
    for i in range(len(funcs)):
        print(funcs[i].__name__, correct_rate[i])

def eval_tag():
    correct_count = np.zeros(len(funcs))
    with open(testFile, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            song_name = row[0]
            tags = row[3][:-1].split('、')
            refer_tags = original_tags.copy()
            for tag in tags:
                if tag not in refer_tags:
                    refer_tags.append(tag)
            input = '歌曲' + song_name + '的曲风是什么？从' + str(refer_tags) + '中选择2个可能的曲风'
            for j in range(len(funcs)):
                attempts = 0
                while attempts < 5:
                    try:
                        output = funcs[j](input)
                        break
                    except:
                        attempts += 1
                if any (tag in output for tag in tags):
                    correct_count[j] += 1
                print("Eval tag, song_name:", song_name, "model", funcs[j].__name__, "correct_count", correct_count[j])
    correct_rate = correct_count / num_eval
    with open("output.txt", 'w', encoding='utf-8') as f:
        f.write("======eval_tag======\n")
        for i in range(len(funcs)):
            f.write(funcs[i].__name__ + " " + str(correct_rate[i]) + "\n")
    print("======eval_tag======")
    for i in range(len(funcs)):
        print(funcs[i].__name__, correct_rate[i])

def eval_language():
    correct_count = np.zeros(len(funcs))
    with open(testFile, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
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
            input = '歌曲' + song_name + '的语种是什么？\'国语\'、\'粤语\'均被认为是\'华语\'，从' + str(language_list) + '中选择1个最可能的语种'
            for j in range(len(funcs)):
                attempts = 0
                while attempts < 5:
                    try:
                        output = funcs[j](input)
                        break
                    except:
                        attempts += 1
                if any (lang in output for lang in processed_language):
                    correct_count[j] += 1
                print("Eval language, song_name:", song_name, "model", funcs[j].__name__, "correct_count", correct_count[j])
    correct_rate = correct_count / num_eval
    with open("output.txt", 'w', encoding='utf-8') as f:
        f.write("======eval_language======\n")
        for i in range(len(funcs)):
            f.write(funcs[i].__name__ + " " + str(correct_rate[i]) + "\n")
    print("======eval_language======")
    for i in range(len(funcs)):
        print(funcs[i].__name__, correct_rate[i])


if __name__ == "__main__":
    eval_singer()
    eval_tag()
    eval_language()