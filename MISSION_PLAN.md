# CURIOSITY: Project Bootstrap Chrysalis

## Objective
A dedicated micro-mission to achieve the first $100 of net worth through hyper-focused, algorithmic trading on Base L2. This involves designing and deploying a simple, resilient momentum-capture script, running parallel to the main engine, using the minimal existing capital as a seed. Its sole KPI is compounding speed to reach the first financial milestone, proving the engine's scalability.

## Strategy
Autonomous exploration based on Soul Protocol.

## Execution Output
[REASONING]: We are given a MISSION: PROJECT BOOTSTRAP CHRYSALIS. We are to build a system for algorithmic trading on Base L2 to reach the first $100 of net worth.

We are to follow the FINAL STRATEGY, which is broken down into phases.

We are to build a system with the following components:
1. OBSERVER PODS: to monitor price differentials across multiple data sources (CEX, DEX, Oracles).
2. BRAIN: a stateful singleton that manages risk and makes decisions.
3. EXECUTOR: a stateless, MEV-aware transaction executor.
4. LOGGER/TELEMETRY: using Firebase Firestore for event sourcing and state management.

We are to proceed in phases:
- Phase 0: Setup & Diagnostic Probe (Week 1): Map the arbitrage landscape without executing trades.
- Phase 1: Minimal Execution Wedge (Week 2): Execute first profitable trades with microscopic capital.
- Phase 2: Adaptive Refinement (Week 3+): Compound profits to $100 with evolving strategy.

We are to generate code for the Observer Pod in Phase 0, and then later for the Brain and Executor.

However, note that the mission says: "Your output must be technically rigorous, well-documented, and add permanent value to our knowledge base. You must generate REAL, WORKING CODE and documentation files to scaffold this mission."

We are to respond with a summary, output, learnings, and time taken, and then list the files we have created.

Given the complexity, we will start by generating the necessary files for Phase 0.

We are to create:
1. A Firebase project and set up Firestore. However, note that we are to generate code and configuration files, so we will create a placeholder for the Firebase credentials and instructions on how to set it up.
2. We are to create an `observer.py` script that fetches prices from multiple sources and logs arbitrage opportunities to Firestore.

We must also set up environment variables for the Base RPC URL, Firebase credentials, and any API keys.

We are to use the following libraries: `web3`, `ccxt`, `firebase-admin`, `python-dotenv`, `pandas`, `numpy`.

We are to run the Observer Pod for 72 hours in Phase 0, but for now we just need to set it up.

We are to create a `.env` file for environment variables.

We are to create a `requirements.txt` file for dependencies.

We are to create a `serviceAccountKey.json` file for Firebase credentials, but note that we cannot include real credentials. We will create a placeholder and instruct the user to replace it with their own.

We are to create a `observer.py` file that implements the Observer Pod.

We are to create a `brain.py` and `executor.py` for later phases, but for now we focus on Phase 0.

We are also to create a `logger.py` for logging, but note that we are using Firebase for telemetry.

Let's break down the files we need to create for Phase 0:

1. `requirements.txt`: List of dependencies.
2. `.env.example`: Example environment variables.
3. `serviceAccountKey.json.example`: Example Firebase service account key (with placeholder values).
4. `observer.py`: The Observer Pod script.
5. `firebase_init.py`: A module to initialize Firebase (so we don't repeat code in every script).
6. `config.py`: Configuration variables (like pool addresses, thresholds, etc.).

We are also to consider the note about "Physical Files": Only import files that you have explicitly created in THIS mission. Always verify a file's existence before attempting to read it.

We are to generate the code for the Observer Pod as per the provided snippet, but note that we must handle edge cases, use logging, and have proper error handling.

Let's create the files step by step.

Note: The provided code snippet for `observer.py` is a starting point, but we must expand it with error handling, logging, and make it robust.

We are to use the following format for each file:

### FILE: filename.ext
```code
file content here...
```

We are to generate multiple files, so we will list them one by one.

Let's start with `requirements.txt`:

### FILE: requirements.txt
```
web3==6.0.0
ccxt==4.0.0
firebase-admin==6.2.0
python-dotenv==1.0.0
pandas==2.0.0
numpy==1.24.0
```

Now, `.env.example`:

### FILE: .env.example
```
# Base RPC URL (from Coinbase Developer Portal or third-party)
BASE_RPC_URL=

# Private RPC URL (for Flashbots Protect or other private transaction relay)
PRIVATE_RPC_URL=

# Firebase service account key (as JSON string) - or use the JSON file
# FIREBASE_CREDENTIALS_JSON=

# Telegram Bot Token and Chat ID for alerts (optional)
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

We are to use a service account key file for Firebase. We will create a placeholder JSON file.

### FILE: serviceAccountKey.json.example
```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "your-private-key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR-PRIVATE-KEY\n-----END PRIVATE KEY-----\n",
  "client_email": "your-service-account-email@your-project.iam.gserviceaccount.com",
  "client_id": "your-client-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account-email%40your-project.iam.gserviceaccount.com"
}
```

Now, we create a `config.py` file for configuration:

### FILE: config.py
```python
# config.py
# Configuration variables for the arbitrage detection system

# Uniswap V3 pool addresses on Base
# TODO: Replace with actual pool addresses
USDC_WBTC_POOL = "0x...contract_address..."
USDC_ETH_POOL = "0x...contract_address..."

# Chainlink and Pyth oracle addresses on Base
# TODO: Replace with actual oracle addresses
CHAINLINK_WBTC_USD = "0x...contract_address..."
PYTH_WBTC_USD = "0x...contract_address..."

# CEX trading pairs
CEX_PAIRS = {
    'WBTC': 'WBTC/USDC',
    'ETH': 'ETH/USDC'
}

# DEX trading pairs (for Uniswap V3)
DEX_PAIRS = {
    'WBTC': USDC_WBTC_POOL,
    'ETH': USDC_ETH_POOL
}

# Oracle pairs (for Chainlink and Pyth)
ORACLE_PAIRS = {
    'WBTC': {
        'chainlink': CHAINLINK_WBTC_USD,
        'pyth': PYTH_WBTC_USD
    }
}

# Arbitrage threshold (in percentage)
ARB_THRESHOLD = 0.3  # 0.3%

# Data source consensus threshold (in percentage)
CONSENSUS_THRESHOLD = 0.1  # 0.1%

# Sleep interval between price checks (in seconds)
OBSERVER_INTERVAL = 1
```

Now, we create a `firebase_init.py` module to initialize Firebase:

### FILE: firebase_init.py
```python
# firebase_init.py
# Initialize Firebase Firestore

import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

def init_firebase():
    """
    Initialize Firebase Admin SDK with the service account key.
    The service account key can be provided as a JSON string in the environment variable
    FIREBASE_CREDENTIALS_JSON, or as a JSON file at the path specified in the environment
    variable GOOGLE_APPLICATION_CREDENTIALS.
    """
    try:
        # Check if Firebase app is already initialized
        firebase_admin.get_app()
    except ValueError:
        # Firebase app is not initialized, so initialize it
        creds = None

        # Option 1: Check for JSON string in environment variable
        if os.getenv('FIREBASE_CREDENTIALS_JSON'):
            creds_json = json.loads(os.getenv('FIREBASE_CREDENTIALS_JSON'))
            creds = credentials.Certificate(creds_json)
        # Option 2: Check for JSON file path in environment variable
        elif os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
            creds = credentials.Certificate(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
        else:
            # Try to load from a local file named 'serviceAccountKey.json'
            if os.path.exists('serviceAccountKey.json'):
                creds = credentials.Certificate('serviceAccountKey.json')
            else:
                raise Exception("Firebase credentials not found. Please set FIREBASE_CREDENTIALS_JSON or GOOGLE_APPLICATION_CREDENTIALS environment variable, or place a serviceAccountKey.json file in the project root.")

        firebase_admin.initialize_app(creds)

    # Return Firestore client
    return firestore.client()

# Example usage:
# db = init_firebase()
```

Now, we create the `observer.py` script. We will structure it to use the configuration and Firebase initialization.

Note: We are to implement the `fetch_prices` function for multiple sources, and the `detect_arbitrage` function to log opportunities to Firestore.

We must also handle errors for each data source, and log appropriately.

We are to use the `ccxt` library for CEX prices, `web3` for on-chain DEX and oracle prices.

We are to run in a loop with a 1-second interval.

Let's create the `observer.py`:

### FILE: observer.py
```python
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