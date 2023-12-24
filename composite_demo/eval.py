import os
import random
import csv
import numpy as np
from duckduck import search

def Music_Recommender(input):
    result = search(messages = [{"role": "user", "content": input}])
    output = result.choices[0].message.content
    return output

funcs = [Music_Recommender] # LLM's functions
num_eval = 10 # 测试的数据量
fileDir = "data"
original_tags = ['放松', '助眠', '抒情', '轻快', '快乐', '治愈', '清新', '平静', '学习', '动感', '活力', '极限运动', '梦幻', '冥想', '悲伤', '孤独', '爱情', '思念', '浪漫', '洒脱', '', '可爱', '慵懒', '热血', 'KTV', '正能量', '幸福', '旅游', '酒吧', '抑郁', '婚礼', '大气', '紧张', '神秘', '甜蜜', '亲情', '遗憾', '苦情', '夜店', '有氧', '暴走', '家务', '通勤', '舞蹈', '憧憬', '友情', '感人', '正直', '咖啡厅', '校园', '足球', '愤怒', '激烈', '驾车', '搞笑', '举铁', '烦躁', '黑暗', '散步', '露营', '舞会', '未来感', '瑜伽', '篮球', '惊悚', '高级感', '白噪音', '广场舞']

def eval_singer():
    correct_count = np.zeros(len(funcs))
    filenames = os.listdir(fileDir)
    for i in range(num_eval):
        file = random.choice(filenames)
        with open(os.path.join(fileDir, file), 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = [row for row in reader]
        row = random.choice(rows)
        song_name = row[0]
        singer_names = row[1][:-1].split('、')
        input = '歌曲' + song_name + '的歌手是谁？返回2个可能的歌手'
        for j in range(len(funcs)):
            output = funcs[j](input)
            if any (singer_name in output for singer_name in singer_names):
                correct_count[j] += 1
        print("song_name:", song_name, "singer_names:", singer_names, "output:", output)
    correct_rate = correct_count / num_eval
    print("======eval_singer======")
    for i in range(len(funcs)):
        print(funcs[i].__name__, correct_rate[i])

def eval_tag():
    correct_count = np.zeros(len(funcs))
    filenames = os.listdir(fileDir)
    for i in range(num_eval):
        file = random.choice(filenames)
        with open(os.path.join(fileDir, file), 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
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
        print("song_name:", song_name, "tags:", tags, "output:", output)
    correct_rate = correct_count / num_eval
    print("======eval_tag======")
    for i in range(len(funcs)):
        print(funcs[i].__name__, correct_rate[i])

def eval_language():
    correct_count = np.zeros(len(funcs))
    filenames = os.listdir(fileDir)
    for i in range(num_eval):
        file = random.choice(filenames)
        with open(os.path.join(fileDir, file), 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
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
        print("song_name:", song_name, "language:", processed_language, "output:", output)
    correct_rate = correct_count / num_eval
    print("======eval_language======")
    for i in range(len(funcs)):
        print(funcs[i].__name__, correct_rate[i])
        
if __name__ == "__main__":
    eval_singer()
    eval_tag()
    eval_language()