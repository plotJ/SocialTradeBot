# config.py

# Twitter API Credentials
TWITTER_CONSUMER_KEY = "your_twitter_consumer_key_here"
TWITTER_CONSUMER_SECRET = "your_twitter_consumer_secret_here"
TWITTER_ACCESS_TOKEN = "your_twitter_access_token_here"
TWITTER_ACCESS_TOKEN_SECRET = "your_twitter_access_token_secret_here"

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = "your_telegram_bot_token_here"

# Raydium Swap Contract Details
RAYDIUM_SWAP_ADDRESS = "your_raydium_swap_contract_address_here"

# This is a dummy ABI. Replace it with the actual Raydium Swap ABI
RAYDIUM_SWAP_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "tokenIn", "type": "address"},
            {"internalType": "address", "name": "tokenOut", "type": "address"},
            {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
            {"internalType": "uint256", "name": "minAmountOut", "type": "uint256"}
        ],
        "name": "swap",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "nonpayable",
        "type": "function"
    }
    # Add more ABI entries as needed
]

# Solana RPC URL
SOLANA_RPC_URL = "https://api.mainnet-beta.solana.com"

# Web3 Provider URL (for Ethereum-based operations, if needed)
WEB3_PROVIDER_URL = "https://mainnet.infura.io/v3/your_infura_project_id_here"

# Additional configuration variables can be added here as needed
RUGCHECK_BASE_URL = "https://rugcheck.xyz"
TWITTERSCORE_BASE_URL = "https://twitterscore.io"

# List IDs for Twitter analysis
TWITTER_LIST_IDS = ["list_id_1", "list_id_2"]

# Maximum number of tweets to analyze
MAX_TWEETS_TO_ANALYZE = 100

# Slippage and price impact settings for token swaps
DEFAULT_SLIPPAGE = 0.01  # 1%
MAX_PRICE_IMPACT = 0.05  # 5%

# Add any other configuration variables your project might need
