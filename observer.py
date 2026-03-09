# observer.py
# Observer Pod: Monitors price differentials across multiple data sources (CEX, DEX, Oracles)
# and logs arbitrage opportunities to Firestore.

import time
import logging
from datetime import datetime
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import ccxt
from web3 import Web3
from firebase_init import init_firebase
import config

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Web3 connection to Base L2
w3 = Web3(Web3.HTTPProvider(os.getenv('BASE_RPC_URL')))
if not w3.is_connected():
    logger.error("Failed to connect to Base RPC")
    sys.exit(1)

# Initialize CEX exchange (Coinbase)
coinbase = ccxt.coinbase()

# Initialize Firebase Firestore
db = init_firebase()

# Helper function to get Uniswap V3 price from pool contract
def get_uniswap_price(pool_address):
    """
    Fetch the current price from a Uniswap V3 pool.
    This requires the pool contract to have the `slot0` function.
    """
    # TODO: Replace with actual ABI for Uniswap V3 pool (we only need slot0)
    # For now, we use a minimal ABI for slot0
    pool_abi = [
        {
            "inputs": [],
            "name": "slot0",
            "outputs": [
                {"internalType": "uint160", "name": "sqrtPriceX96", "type": "uint160"},
                {"internalType": "int24", "name": "tick", "type": "int24"},
                {"internalType": "uint16", "name": "observationIndex", "type": "uint16"},
                {"internalType": "uint16", "name": "observationCardinality", "type": "uint16"},
                {"internalType": "uint16", "name": "observationCardinalityNext", "type": "uint16"},
                {"internalType": "uint8", "name": "feeProtocol", "type": "uint8"},
                {"internalType": "bool", "name": "unlocked", "type": "bool"}
            ],
            "stateMutability": "view",
            "type": "function"
        }
    ]
    pool_contract = w3.eth.contract(address=pool_address, abi=pool_abi)
    try:
        slot0 = pool_contract.functions.slot0().call()
        sqrtPriceX96 = slot0[0]
        # Convert sqrtPriceX96 to actual price (assuming token0 is USDC and token1 is WBTC/ETH)
        # This conversion is simplified and may need adjustment based on the pool's token order and decimals
        price = (sqrtPriceX96 ** 2) / (2 ** 192)
        # Adjust for decimals (assuming USDC has 6 decimals and WBTC has 8, or ETH has 18)
        # TODO: Adjust for the specific pool's token decimals
        return price
    except Exception as e:
        logger.error(f"Error fetching Uniswap price from {pool_address}: {e}")
        return None

# Helper function to get Chainlink price
def get_chainlink_price(oracle_address):
    """
    Fetch the current price from a Chainlink oracle.
    """
    # Chainlink price feed ABI for latestRoundData
    chainlink_abi = [
        {
            "inputs": [],
            "name": "latestRoundData",
            "outputs": [
                {"internalType": "uint80", "name": "roundId", "type": "uint80"},
                {"internalType": "int256", "name": "answer", "type": "int256"},
                {"internalType": "uint256", "name": "startedAt", "type": "uint256"},
                {"internalType": "uint256", "name": "updatedAt", "type": "uint256"},
                {"internalType": "uint80", "name": "answeredInRound", "type": "uint80"}
            ],
            "stateMutability": "view",
            "type": "function"
        }
    ]
    oracle_contract = w3.eth.contract(address=oracle_address, abi=chainlink_abi)
    try:
        latest_round_data = oracle_contract.functions.latestRoundData().call()
        price = latest_round_data[1]  # answer is the second element
        # Adjust for decimals (Chainlink oracles typically have 8 decimals)
        price = price / 1e8
        return price
    except Exception as e:
        logger.error(f"Error fetching Chainlink price from {oracle_address}: {e}")
        return None

# Helper function to get Pyth price (simplified)
def get_pyth_price(oracle_address):
    """
    Fetch the current price from a Pyth oracle.
    Note: This is a simplified version. Pyth may require a different on-chain interaction.
    """
    # TODO: Implement Pyth price fetching based on their on-chain contract
    # For now, return None as a placeholder
    logger.warning("Pyth price fetching not yet implemented.")
    return None

def fetch_prices(asset='WBTC'):
    """
    Fetch prices for a given asset from multiple sources.
    Returns a dictionary with prices from CEX, DEX, and oracles.
    """
    prices = {
        'timestamp': datetime.utcnow().isoformat(),
        'asset': asset,
        'cex': None,
        'dex': None,
        'oracle_chainlink': None,
        'oracle_pyth': None
    }

    # Fetch CEX price (Coinbase)
    try:
        ticker = coinbase.fetch_ticker(config.CEX_PAIRS[asset])
        prices['cex'] = ticker['last']
    except Exception as e:
        logger.error(f"Error fetching CEX price for {asset}: {e}")

    # Fetch DEX price (Uniswap V3)
    dex_pool_address = config.DEX_PAIRS.get(asset)
    if dex_pool_address:
        prices['dex'] = get_uniswap_price(dex_pool_address)

    # Fetch Oracle prices
    oracle_addresses = config.ORACLE_PAIRS.get(asset)
    if oracle_addresses:
        if oracle_addresses.get('chainlink'):
            prices['oracle_chainlink'] = get_chainlink_price(oracle_addresses['chainlink'])
        if oracle_addresses.get('pyth'):
            prices['oracle_pyth'] = get_pyth_price(oracle_addresses['pyth'])

    return prices

def detect_arbitrage(prices):
    """
    Detect arbitrage opportunity between CEX and DEX.
    If the spread is above the threshold (config.ARB_THRESHOLD), log the opportunity to Firestore.
    """
    if prices['cex'] is None or prices['dex'] is None:
        logger.warning(f"Missing price data for {prices['asset']}: CEX={prices['cex']}, DEX={prices['dex']}")
        return

    spread = abs(prices['cex'] - prices['dex']) / prices['cex'] * 100
    if spread > config.ARB_THRESHOLD:
        opportunity = {
            **prices,
            'spread': spread,
            'detected_at': datetime.utcnow().isoformat()
        }
        try:
            # Write to Firestore collection 'arb_opportunities'
            db.collection('arb_opportunities').add(opportunity)
            logger.info(f"Arbitrage opportunity detected for {prices['asset']}: {spread:.2f}%")
        except Exception as e:
            logger.error(f"Failed to write arbitrage opportunity to Firestore: {e}")
    else:
        logger.debug(f"No arbitrage opportunity for {prices['asset']}: spread={spread:.2f}%