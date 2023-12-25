import json
import csv
import os
import random
import copy
base = {"messages": [{"role": "system", "content": "You are smart music AI Assistant. You can find musics that users want. 并给出推荐和介绍"}, {"role": "user", "content": ""}, {"role": "assistant", "content": ""}]}

dataset = []
directory_path = os.getcwd()

all_tags = []
for filename in os.listdir(directory_path):
    if filename.endswith('.csv'):  # 确保文件是以.csv结尾的CSV文件
        file_path = os.path.join(directory_path, filename)  # 构建完整的文件路径

        # 打开CSV文件
        with open(file_path, 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            
            # 遍历CSV文件的每一行
            
            for row in csvreader:
                # 在这里进行CSV数据的处理
                name = row[0]
                artist = row[1]
                type = row[2]
                tag = row[3]
                lang = row[4]
                bpm = row[5]
                comment = row[6]

                if name == "歌名":
                    continue
                
                if artist:
                    
                    data = copy.deepcopy(base)
                    data["messages"][1]["content"] = "歌曲" + name + "的歌手是谁?"
                    data["messages"][2]["content"] = artist
                    dataset.append(data)
                
                if lang:
                    
                    data = copy.deepcopy(base)
                    data["messages"][1]["content"] = "歌曲" + name + "的语种是什么?"
                    data["messages"][2]["content"] = lang
                    dataset.append(data)
                
                if tag:

                    tags = tag.split("、")
                    
                    for tag_name in tags:
                        if tag_name:
                            all_tags.append(tag_name)

all_tags = list(set(all_tags))


for filename in os.listdir(directory_path):
    if filename.endswith('.csv'):  # 确保文件是以.csv结尾的CSV文件
        file_path = os.path.join(directory_path, filename)  # 构建完整的文件路径

        # 打开CSV文件
        with open(file_path, 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            
            # 遍历CSV文件的每一行
            
            for row in csvreader:
                # 在这里进行CSV数据的处理
                name = row[0]
                artist = row[1]
                type = row[2]
                tag = row[3]
                lang = row[4]
                bpm = row[5]
                comment = row[6]

                if tag:

                    tags = tag.split("、")
                    true_tags = [item for item in tags if item]

                    true_tag = random.choice(true_tags)
                    
                    total_tags = []

                    for _ in range(5):
                        total_tags.append(random.choice(all_tags))
                    
                    total_tags.append(true_tag)
                    random.shuffle(total_tags)

                    data = copy.deepcopy(base)

                    result_string = ', '.join(total_tags)
                    data["messages"][1]["content"] = "请给歌曲" + name + "打一个标签, 从" + result_string + "中选择。"
                    data["messages"][2]["content"] = true_tag

                    dataset.append(data)


with open("dataset.jsonl", "w") as file:
	t = 1

for data in dataset:
	json_sample = json.dumps(data, ensure_ascii=False)

	with open("dataset.jsonl", "a", encoding='utf-8') as file:
		file.write(json_sample)
		file.write('\n')