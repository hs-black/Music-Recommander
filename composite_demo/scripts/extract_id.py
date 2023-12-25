import csv, os

input_path = '/home/zsu/Langchain-Chatchat/knowledge_base/music/content'
target = '90后'
output_path = 'id_'+ target + '.csv'

ids = []
filenames = os.listdir(input_path)
for filename in filenames:
    if target in filename:
        input_file = os.path.join(input_path, filename)
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                ids_before = row[4][1:-1].split(', ')
                for id in ids_before:
                    if id != "" and int(id) not in ids:
                        ids.append(int(id))
f_output = open(output_path,'w',encoding='utf-8',newline='')
csv_writer = csv.writer(f_output)
print(len(ids))
csv_writer.writerow(ids)