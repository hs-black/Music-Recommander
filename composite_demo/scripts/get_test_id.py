import requests, csv
ids = []
for id in requests.get(r"http://localhost:3000/playlist/detail?id=3778678").json()['playlist']['trackIds']:
    ids.append(id['id'])
with open('../data/ids/id_test.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(ids)