import os
import platform
import csv
import ast
from transformers import AutoTokenizer, AutoModel
import os
import glob

# 指定目录


tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm3-6b", trust_remote_code=True)
model = AutoModel.from_pretrained("THUDM/chatglm3-6b", trust_remote_code=True).cuda()
model = model.eval()

system_item = {"role": "system",
               "content": 
               '''
               输入信息为网易云音乐的歌单，以歌单名称；歌单简介的形式给出。
               你需要给出歌单里音乐的最多五个关键词来描述这个歌单内部音乐的共同特征，比如风格，心情，适用场景或者来源等等。
               下面是一些例子：
               歌单名称：港乐点唱机 | 声生不息的粤语抒情；歌单简介：其实心里最大理想，跟她归家为她唱
               关键词为：粤语，流行，经典，抒情，怀旧
               歌单名称：2023 中国好声音 ｜ 12期全收录；歌单简介：中国好声音 
               关键词为：中国好声音，综艺
               歌单名称：国摇/迷幻/独立/自赏/钉鞋/朋克；歌单简介：我肚子里住了个吐肥皂泡的小人,一开心就咕嘟咕嘟吐泡儿。凉椅上享受六点半的晚风吹两个泡泡,下雨天黎明一个清甜的梦吐三个泡泡,空调房西瓜正中心的第一口要吐一小溜儿泡泡。要是想到了你,那准像晃过的冰镇汽水,咕嘟咕嘟嘟嘟涨了满肚,最后嘭--的一声,炸出朵漂亮的小花来。
               关键词为：摇滚，迷幻
               '''}
role = "user"

# string = "歌单名称：天赐的声音 | 大口呼吸，世界热烈 歌单简介：《天赐的声音》是一档中国电视音乐选秀节目，在浙江卫视播出，至今已播出四季。"

# response, _ = model.chat(tokenizer, string, history=[system_item], role=role, temperature=0.01, top_p=0.95)
# print(response)

tagdict = {}
songsdict = {}

directory = './file'

            
import json
# 遍历目录下所有以 .csv 结尾的文件
prename = "6666666666666666"
for filename in glob.glob(os.path.join(directory, '*.csv')):
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        cnt = 0
        for row in reader:
            tags = ast.literal_eval(row[3])
            songs = ast.literal_eval(row[4])
            response, _ = model.chat(tokenizer, ("歌单名称：" + row[1] + "；歌单简介：" + row[2]).replace("\n", ","), history=[system_item], role=role, temperature=0.01, top_p=0.95, top_k=20)
            last_colon = response.rfind('：')
            if last_colon != -1:
                result = response[last_colon+1:]
                tags = tags + result.split('，')
                for tag in tags:
                    if tag not in tagdict:
                        tagdict[tag] = 1
                for song in songs:
                    if song not in songsdict:
                        songsdict[song] = {}
                    dic = songsdict[song]
                    for tag in tags:
                        dic[tag] = 1
                cnt += 1
            else:
                continue
            if cnt % 10 == 0:
                print (f"process {cnt}")

        print (f'finish file {filename}')
        if filename[7] != prename[7]:
            print ("Saving")
            with open('tagdict.json', 'w') as f:
                json.dump(tagdict, f)
            with open('songsdict.json', 'w') as f:
                json.dump(songsdict, f)
        prename = filename



with open('tagdict.json', 'w') as f:
    json.dump(tagdict, f)
with open('songsdict.json', 'w') as f:
    json.dump(songsdict, f)

