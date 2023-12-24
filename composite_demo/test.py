import requests


proxies = {
  "http": None,
  "https": None,
}

para = "周杰伦"
r = requests.get(r"http://localhost:3000/search?keywords=" + para, proxies = proxies)
print(r)