# Kalshi-trader-jackson
# Kalshi AI Signal Bot

A Python bot that scans live news headlines, matches them to open Kalshi prediction markets, and uses AI to flag potential mispricings all in the terminal.

## What It Does

1. Fetches the latest top news headlines
2. Pulls open markets from Kalshi
3. Sends both to an AI model to find relevant connections
4. Prints trading signals when the news suggests a market may be mispriced

## Example Output

   
--- Checking for signals ---

Headline: "Fed signals rate pause through summer"
→ Affects: "Will the Fed cut rates in June?" market
→ Makes NO more likely
→ Current price is 65¢ YES — likely OVERPRICED given this news
   

## Setup

### 1. Clone the repo
   bash
git clone https://github.com/yourusername/kalshi-trader.git
cd kalshi-trader
   

### 2. Install dependencies
   bash
pip3 install -r requirements.txt
   

### 3. Add your API keys
Create a `.env` file in the project folder:
   
ANTHROPIC_API_KEY=your_key_here
NEWS_API_KEY=your_key_here
KALSHI_API_KEY_ID=your_key_here
   

You'll also need your Kalshi private key file (`.pem` or `.txt`) saved in the project folder.

### 4. Run it
   bash
python3 trader.py
   

The bot checks for signals every 5 minutes.

## API Keys You'll Need

| Service | What it's for | Link |

| Kalshi | Fetches live prediction markets | [kalshi.com](https://kalshi.com) |
| Anthropic or Groq | AI analysis of headlines | [console.anthropic.com](https://console.anthropic.com) or [console.groq.com](https://console.groq.com) |
| NewsAPI | Live news headlines | [newsapi.org](https://newsapi.org) |

## Project Structure

   
kalshi-trader-jackson
├── trader.py         # Main bot script
├── requirements.txt  # Python dependencies
├── .env              # Your API keys (never uploaded to GitHub)
├── .gitignore        # Keeps .env private
└── README.md         # This file
   

## Roadmap

- [ ] Web dashboard instead of terminal output
- [ ] Confidence scoring (1–10) on each signal
- [ ] SMS/Slack alerts for strong signals
- [ ] Actual trade execution via Kalshi API

## Purpose
- I've become very interested in Kalshi lately as a prediction market since the "odds" shown don't actually correlate to real odds bt rather the amount of money placed. Therefore it is possible and somewhat likely that markets become extremely distorted based on false or misleading information. This is one of the initial parts of a larger kalshi trading system I'm building.

