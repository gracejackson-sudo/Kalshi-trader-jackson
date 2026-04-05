
#part 1: loading API keys
import os
from dotenv import load_dotenv

load_dotenv()  # reads .env file containing private API keys 

ANTHROPIC_KEY = os.getenv("claude_API_key")
NEWS_KEY = os.getenv("news_API_key")
KALSHI_KEY_ID = os.getenv("kalshi_API_key")

#part 2: retrieve Kalshi markets
from kalshi_python import Configuration, KalshiClient

def get_markets():
    config = Configuration(host="https://api.elections.kalshi.com/trade-api/v2")
    with open("gracejprojects.txt", "r") as f:
        config.private_key_pem = f.read()
    config.api_key_id = KALSHI_KEY_ID

    client = KalshiClient(config)
    markets = client.get_markets(limit=30)  # grabs 30 open markets
    return markets

#part 3: retrieve news headlines and format
import requests

def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_KEY}"
    response = requests.get(url)
    articles = response.json()["articles"]
    return [a["title"] for a in articles[:10]]

#part 4:ask claude to input new sources and determine mispricings 
import anthropic

def analyze(headlines, markets):
    client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

    # Turn markets into readable text
    market_text = "\n".join([
        f"- {m.title} | Current price: {m.last_price}¢"
        for m in markets.markets
    ])

    headline_text = "\n".join(headlines)

    prompt = f"""
    Here are today's top news headlines:
    {headline_text}

    Here are open prediction markets on Kalshi:
    {market_text}

    For each headline that seems relevant to a market, tell me:
    1. Which market it affects
    2. Whether it makes YES or NO more likely
    3. If the current price seems wrong given the news (mispriced)

    Be concise. Only flag real mispricings.
    """

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text

#part 5: implementation
import time

print(" Starting Kalshi Signal Bot...")

while True:
    print("\n--- Checking for signals ---")
    headlines = get_news()
    markets = get_markets()
    signals = analyze(headlines, markets)
    print(signals)
    print("\nWaiting 3 minutes before next check...")
    time.sleep(180)  # wait 3 minutes, then repeat