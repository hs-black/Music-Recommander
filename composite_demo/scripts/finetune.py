from openai import OpenAI
import os

os.environ["OPENAI_API_KEY"] = ""
os.environ["BING_SUBSCRIPTION_KEY"] = ""
os.environ["BING_SEARCH_URL"] = "https://api.bing.microsoft.com/v7.0/search"
client = OpenAI()

client.files.create(
  file=open("dataset.jsonl", "rb"),
  purpose="fine-tune"
)