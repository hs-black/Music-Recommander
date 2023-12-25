import requests
import csv
import sys
def main(target):
    output_path = "../data/csv_data/data_" + target + ".csv"
    input_id_path = "../data/ids/id_" + target + ".csv"
    f_output = open(output_path,'w',encoding='utf-8',newline='')
    csv_writer = csv.writer(f_output)
    csv_writer.writerow(["歌名", "歌手", "曲风", "推荐标签", "语种", "BPM", "乐评"])

    with open(input_id_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            ids = list(map(int, row))
    count = 1
    for id in ids:
        try:
            dataa = requests.get(f"http://localhost:3000/song/detail?ids={id}").json()
            data = requests.get(f"http://localhost:3000/song/wiki/summary?id={id}").json()['data']['blocks']
            row = ["", "", "", "", "", "", ""]
            row[0] = dataa['songs'][0]['name']
            for i in range(len(dataa['songs'][0]['ar'])):
                row[1] += dataa['songs'][0]['ar'][i]['name']
                row[1] += '、'

            for i in range(len(data[1]['creatives'])):
                title = str(data[1]['creatives'][i]['uiElement']['mainTitle']['title'])
                if title == '曲风':
                    for j in range(len(data[1]['creatives'][i]['resources'])):
                        row[2] += str(data[1]['creatives'][i]['resources'][j]['uiElement']['mainTitle']['title'])
                        row[2] += '、'
                elif title == '推荐标签':
                    for j in range(len(data[1]['creatives'][i]['resources'])):
                        row[3] += str(data[1]['creatives'][i]['resources'][j]['uiElement']['mainTitle']['title'])
                        row[3] += '、'
                elif title == '语种':
                    row[4] = str(data[1]['creatives'][i]['uiElement']['textLinks'][0]['text'])
                elif title == 'BPM':
                    row[5] = str(data[1]['creatives'][i]['uiElement']['textLinks'][0]['text'])
                elif title == '乐评':
                    row[6] = str(data[1]['creatives'][i]['resources'][0]['uiElement']['descriptions'][0]['description'])
                else:
                    continue
            csv_writer.writerow(row)
        except:
            continue
        print(count)
        count += 1
    f_output.close()

if __name__ == "__main__":
    main(sys.argv[1])