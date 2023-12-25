from openai import OpenAI
import os

os.environ["OPENAI_API_KEY"] = "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"
os.environ["BING_SUBSCRIPTION_KEY"] = "a24d675d518c4e0a9707ab9d34d75ea2"
os.environ["BING_SEARCH_URL"] = "https://api.bing.microsoft.com/v7.0/search"
client = OpenAI()

client.files.create(
  file=open("dataset.jsonl", "rb"),
  purpose="fine-tune"
)