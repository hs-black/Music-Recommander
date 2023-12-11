import os
import platform
import csv
from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm3-6b", trust_remote_code=True)
model = AutoModel.from_pretrained("THUDM/chatglm3-6b", trust_remote_code=True).cuda()
model = model.eval()

system_item = {"role": "system",
               "content": "输入信息为网易云音乐的歌单，以名称：歌单名称，简介：歌单简介的形式给出。你需要给出歌单里音乐的最多五个关键词，比如风格，心情，场景或者来源等等，你的回复格式为“关键词为：一些关键词”。举例：歌单名称：港乐点唱机 | 声生不息的粤语抒情 歌单简介：其实心里最大理想，跟她归家为她唱，关键词为：粤语，流行，经典，抒情，怀旧。歌单名称：2023 中国好声音 ｜ 12期全收录。 歌单简介：中国好声音 关键词为：中国好声音，综艺"}
role = "user"

with open('output.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        flag = 0
        for i in range(1):
            response, _ = model.chat(tokenizer, ("歌单名称：" + row[1] + " 歌单简介：" + row[2]).replace("\n", " "), history=[system_item], role=role, temperature=0.01, top_p=0.95)
            if response.startswith("关键词为："):
                flag = 1
                print(response, end="", flush=True)
                print("")
                break
        if not flag:
            print ("error", response)
            


