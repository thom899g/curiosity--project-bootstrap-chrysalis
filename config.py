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