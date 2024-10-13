import json
import requests
import pandas as pd
from bs4 import BeautifulSoup


def load_secrets():
    with open("./secrets.json") as f:
        secrets = json.load(f)
    
    return secrets


def get_news_content(link):
    response = requests.get(link)

    if response.status_code == 200:
        data = response.content
        soup = BeautifulSoup(data, "html.parser")
        content = "\n".join([p.get_text() for p in soup.find_all(["p", "h1", "h2", "h3"])])
        return content
    else:
        return "None"

def main():
    secrets = load_secrets()
    api_key = secrets["api-key"]
    file = secrets["news-file"]

    params = {
        "country": "us",
        "category": "technology",
        "apiKey": api_key
    }

    df = pd.read_csv(file)
    df["content"] = df["link"].apply(get_news_content)
    df.to_csv("./news_content.csv")

if __name__ == "__main__":
    main()
