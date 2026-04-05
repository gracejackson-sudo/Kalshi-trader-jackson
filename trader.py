
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

#part 4:ask claude to input new sources and determine mispricings as well as a confidence interval for the importance of the singal on a scale of 1-10
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
    4. A confidence score from 1-10 where:
       - 1-3 = weak signal, probably ignore
       - 4-6 = moderate signal, worth watching
       - 7-10 = strong signal, worth acting on

    Format each signal exactly like this:
    SIGNAL
    Headline: [headline]
    Market: [market name]
    Direction: [YES or NO]
    Reasoning: [one sentence why]
    Confidence: [number]/10
    END

    Only include signals with a confidence of 5 or higher.
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
    raw_signals = analyze(headlines, markets)
    
    # Split into individual signals
    signals = raw_signals.split("SIGNAL")
    
    strong = []
    moderate = []
    
    for signal in signals:
        if "Confidence:" not in signal:
            continue
        # Pull out the confidence number
        try:
            score_line = [l for l in signal.split("\n") if "Confidence:" in l][0]
            score = int(score_line.replace("Confidence:", "").replace("/10", "").strip())
        except:
            continue
        
        if score >= 7:
            strong.append((score, signal.strip()))
        elif score >= 5:
            moderate.append((score, signal.strip()))
    
    # Print strong signals first
    if strong:
        print("\n🔥 STRONG SIGNALS (7+):")
        for score, s in sorted(strong, reverse=True):
            print(f"\n{s}")
    
    if moderate:
        print("\n👀 MODERATE SIGNALS (5-6):")
        for score, s in sorted(moderate, reverse=True):
            print(f"\n{s}")
    
    if not strong and not moderate:
        print("\n✅ No strong signals right now. Checking again in 5 minutes...")
    print("\nWaiting 3 minutes before next check...")
    time.sleep(180)  # wait 3 minutes, then repeat
