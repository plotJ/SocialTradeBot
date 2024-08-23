import asyncio
import json
import requests
from bs4 import BeautifulSoup
import tweepy
import pandas as pd
from textblob import TextBlob
from telegram import Bot
from telegram.error import TelegramError
from web3 import Web3
from solana.rpc.async_api import AsyncClient
from solana.transaction import Transaction
from solana.system_program import TransactionInstruction

# 1. Twitter List Sentiment Analyzer
class TwitterAnalyzer:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        """
        Initialize the TwitterAnalyzer with Twitter API credentials.
        """
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit=True)

    def get_list_tweets(self, list_id, max_tweets=100):
        """
        Fetch tweets from a specified Twitter list.
        :param list_id: ID of the Twitter list
        :param max_tweets: Maximum number of tweets to fetch
        :return: List of tweet objects
        """
        tweets = []
        for tweet in tweepy.Cursor(self.api.list_timeline, list_id=list_id).items(max_tweets):
            tweets.append(tweet)
        return tweets

    def analyze_sentiment(self, tweet):
        """
        Analyze the sentiment of a single tweet.
        :param tweet: Tweet object
        :return: Sentiment classification ('positive', 'neutral', or 'negative')
        """
        analysis = TextBlob(tweet.text)
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def analyze_tweets(self, list_id):
        """
        Analyze tweets from a specified list and return a DataFrame with results.
        :param list_id: ID of the Twitter list
        :return: DataFrame containing analyzed tweet data
        """
        tweets = self.get_list_tweets(list_id)
        analyzed_tweets = []
        for tweet in tweets:
            analyzed_tweets.append({
                'text': tweet.text,
                'user': tweet.user.screen_name,
                'created_at': tweet.created_at,
                'retweet_count': tweet.retweet_count,
                'favorite_count': tweet.favorite_count,
                'sentiment': self.analyze_sentiment(tweet)
            })
        return pd.DataFrame(analyzed_tweets)

# 2. Telegram Project Analyzer Bot
class TelegramAnalyzer:
    def __init__(self, token):
        """
        Initialize the TelegramAnalyzer with a Telegram bot token.
        """
        self.bot = Bot(token)

    async def extract_info(self, message):
        """
        Extract smart contract address and social network links from a message.
        :param message: Message text
        :return: Tuple containing smart contract address and list of social links
        """
        smart_contract = None
        social_links = []
        
        # Extract smart contract address
        if 'smart contract:' in message.lower():
            smart_contract = message.split('smart contract:')[1].strip().split()[0]
        
        # Extract social network links
        social_networks = ['twitter', 'telegram', 'facebook', 'instagram', 'discord']
        for network in social_networks:
            if network in message.lower():
                link = message.lower().split(f'{network}:')[1].strip().split()[0]
                social_links.append((network, link))
        
        return smart_contract, social_links

    async def run(self):
        """
        Run the Telegram bot and process incoming messages.
        """
        try:
            bot_info = await self.bot.get_me()
            print(f"Bot Name: {bot_info.first_name}")
            print(f"Bot Username: @{bot_info.username}")
            
            offset = 0
            while True:
                updates = await self.bot.get_updates(offset=offset, timeout=30)
                for update in updates:
                    if update.message:
                        smart_contract, social_links = await self.extract_info(update.message.text)
                        
                        if smart_contract:
                            print(f"Smart Contract: {smart_contract}")
                        
                        if social_links:
                            print("Social Network Links:")
                            for network, link in social_links:
                                print(f"{network.capitalize()}: {link}")
                        
                        print("---")
                    
                    offset = update.update_id + 1
                
                await asyncio.sleep(1)
        
        except TelegramError as e:
            print(f"Error: {e}")

# 3. Token Security Analyzer
def analyze_token_security(token_address):
    """
    Analyze the security of a token using rugcheck.xyz.
    :param token_address: Address of the token to analyze
    :return: Dictionary containing security analysis results
    """
    base_url = "https://rugcheck.xyz"
    check_url = f"{base_url}/tokens/{token_address}"
    
    try:
        # Send GET request to rugcheck.xyz
        response = requests.get(check_url)
        response.raise_for_status()
        
        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract relevant information
        security_score = soup.select_one('.security-score').text
        liquidity_info = soup.select_one('.liquidity-info').text
        contract_verification = soup.select_one('.contract-verification').text
        warnings = [warning.text for warning in soup.select('.warning')]
        
        # Compile analysis results
        analysis_result = {
            "token_address": token_address,
            "security_score": security_score,
            "liquidity_info": liquidity_info,
            "contract_verification": contract_verification,
            "warnings": warnings
        }
        
        return analysis_result
    
    except requests.RequestException as e:
        print(f"An error occurred while fetching data: {e}")
        return None

# 4. Twitter Influencer Analyzer
def analyze_twitter_influencers(twitter_handle):
    """
    Analyze Twitter influencers using twitterscore.io.
    :param twitter_handle: Twitter handle to analyze
    :return: Dictionary containing influencer analysis results
    """
    base_url = "https://twitterscore.io"
    analysis_url = f"{base_url}/twitter/{twitter_handle}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Send GET request to twitterscore.io
        response = requests.get(analysis_url, headers=headers)
        response.raise_for_status()
        
        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract relevant information
        influencer_count = soup.select_one('.influencer-count').text
        total_followers = soup.select_one('.total-followers').text
        engagement_rate = soup.select_one('.engagement-rate').text
        
        top_influencers = [influencer.text for influencer in soup.select('.top-influencer')]
        
        # Compile analysis results
        analysis_result = {
            "twitter_handle": twitter_handle,
            "influencer_count": influencer_count,
            "total_followers": total_followers,
            "engagement_rate": engagement_rate,
            "top_influencers": top_influencers[:5]  # Limit to top 5 influencers
        }
        
        return analysis_result
    
    except requests.RequestException as e:
        print(f"An error occurred while fetching data: {e}")
        return None

# 5. Raydium Token Swap Script
class RaydiumSwapper:
    def __init__(self, raydium_swap_abi, raydium_swap_address):
        """
        Initialize the RaydiumSwapper with ABI and contract address.
        :param raydium_swap_abi: ABI of the Raydium swap contract
        :param raydium_swap_address: Address of the Raydium swap contract
        """
        self.RAYDIUM_SWAP_ABI = raydium_swap_abi
        self.RAYDIUM_SWAP_ADDRESS = raydium_swap_address
        self.solana_client = AsyncClient("https://api.mainnet-beta.solana.com")
        self.w3 = Web3(Web3.HTTPProvider('https://solana-api.projectserum.com'))

    async def get_current_price(self, token_in_address, token_out_address):
        """
        Get the current price for a token pair.
        This is a placeholder function and needs to be implemented.
        :param token_in_address: Address of the input token
        :param token_out_address: Address of the output token
        :return: Current price
        """
        # Implement price fetching logic here
        pass

    async def perform_token_swap(self, token_in_address, token_out_address, amount_in, min_amount_out, slippage, max_price_impact):
        """
        Perform a token swap on Raydium.
        :param token_in_address: Address of the input token
        :param token_out_address: Address of the output token
        :param amount_in: Amount of input token to swap
        :param min_amount_out: Minimum amount of output token to receive
        :param slippage: Allowed slippage percentage
        :param max_price_impact: Maximum allowed price impact percentage
        :return: Transaction receipt
        """
        # Create contract instance
        swap_contract = self.w3.eth.contract(address=self.RAYDIUM_SWAP_ADDRESS, abi=self.RAYDIUM_SWAP_ABI)

        # Get current price and calculate expected output
        current_price = await self.get_current_price(token_in_address, token_out_address)
        expected_out = amount_in * current_price
        min_amount_out_with_slippage = min_amount_out * (1 - slippage)

        # Check price impact
        price_impact = (expected_out - min_amount_out) / expected_out
        if price_impact > max_price_impact:
            raise ValueError(f"Price impact too high: {price_impact:.2%}")

        # Prepare swap transaction
        swap_tx = swap_contract.functions.swap(
            token_in_address,
            token_out_address,
            amount_in,
            min_amount_out_with_slippage
        ).buildTransaction({
            'from': self.w3.eth.accounts[0],
            'gas': 2000000,
            'gasPrice': self.w3.eth.gas_price,
            'nonce': self.w3.eth.get_transaction_count(self.w3.eth.accounts[0]),
        })

        # Sign and send transaction
        signed_txn = self.w3.eth.account.sign_transaction(swap_tx, private_key='YOUR_PRIVATE_KEY')
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        # Wait for transaction receipt
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        return tx_receipt

# Main function to demonstrate usage of all components
async def main():
    # 1. Twitter List Sentiment Analysis
    twitter_analyzer = TwitterAnalyzer("CONSUMER_KEY", "CONSUMER_SECRET", "ACCESS_TOKEN", "ACCESS_TOKEN_SECRET")
    list_id = "YOUR_LIST_ID"
    tweet_analysis = twitter_analyzer.analyze_tweets(list_id)
    print("Twitter Sentiment Analysis:")
    print(tweet_analysis.head())
    print("\n")

    # 2. Telegram Project Analysis
    telegram_analyzer = TelegramAnalyzer("YOUR_BOT_TOKEN")
    # Run this in a separate thread or process as it's a long-running task
    # await telegram_analyzer.run()

    # 3. Token Security Analysis
    token_address = "SAMPLE_TOKEN_ADDRESS"
    security_analysis = analyze_token_security(token_address)
    print("Token Security Analysis:")
    print(json.dumps(security_analysis, indent=2))
    print("\n")

    # 4. Twitter Influencer Analysis
    twitter_handle = "SAMPLE_TWITTER_HANDLE"
    influencer_analysis = analyze_twitter_influencers(twitter_handle)
    print("Twitter Influencer Analysis:")
    print(json.dumps(influencer_analysis, indent=2))
    print("\n")

    # 5. Raydium Token Swap
    raydium_swapper = RaydiumSwapper("RAYDIUM_SWAP_ABI", "RAYDIUM_SWAP_ADDRESS")
    try:
        swap_result = await raydium_swapper.perform_token_swap(
            "TOKEN_IN_ADDRESS",
            "TOKEN_OUT_ADDRESS",
            100,  # amount_in
            95,   # min_amount_out
            0.01, # slippage
            0.05  # max_price_impact
        )
        print("Raydium Swap Result:")
        print(f"Transaction Hash: {swap_result.transactionHash.hex()}")
    except Exception as e:
        print(f"Raydium Swap Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
