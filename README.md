# SocialTradeBot

SocialTradeBot is a comprehensive Python tool designed to analyze cryptocurrency projects through various social and technical metrics. It combines sentiment analysis, security checks, influencer analysis, and decentralized exchange interactions to provide a holistic view of a cryptocurrency project.

## Features

1. **Twitter List Sentiment Analysis**: Analyzes the sentiment of tweets from specified Twitter lists.
2. **Telegram Project Analyzer**: Extracts key information from Telegram messages about crypto projects.
3. **Token Security Analysis**: Checks the security of token contracts using rugcheck.xyz.
4. **Twitter Influencer Analysis**: Analyzes Twitter accounts for influencer metrics using twitterscore.io.
5. **Raydium Token Swap**: Facilitates token swaps on the Raydium decentralized exchange.

## Installation

1. Clone this repository:
git clone [[https://github.com/yourusername/CryptoSocialAnalyzer.git](https://github.com/plotJ/SocialTradeBot)](https://github.com/plotJ/SocialTradeBot/)

2. Navigate to the project directory:
cd SocialTradeBot

3. Install the required dependencies:
pip install -r requirements.txt


## Usage

1. Set up your API keys and tokens in a `config.py` file (not included in the repository for security reasons).
2. Run the main script:
python main.py


## Configuration

Before running the script, you need to set up the following:

- Twitter API credentials
- Telegram Bot Token
- Raydium Swap contract ABI and address

Create a `config.py` file with the following structure:

```python
TWITTER_CONSUMER_KEY = "your_consumer_key"
TWITTER_CONSUMER_SECRET = "your_consumer_secret"
TWITTER_ACCESS_TOKEN = "your_access_token"
TWITTER_ACCESS_TOKEN_SECRET = "your_access_token_secret"

TELEGRAM_BOT_TOKEN = "your_telegram_bot_token"

RAYDIUM_SWAP_ABI = [...]  # Your Raydium Swap ABI here
RAYDIUM_SWAP_ADDRESS = "your_raydium_swap_address"
Contributing
Contributions, issues, and feature requests are welcome. Feel free to check issues page if you want to contribute.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Disclaimer
This tool is for educational and research purposes only. Always do your own research before making any investment decisions. The authors are not responsible for any financial losses incurred from using this tool.
