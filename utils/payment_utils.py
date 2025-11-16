from datetime import datetime
from .text_utils import escape_markdown

def duration(code: str):
    mapping = {
        '2HOUR': '2Hours',
        '1DAYZ': '1Day',
        '3DAYZ': '3Days',
        '1WEEK': '1Week',
        '1MNTH': '1Month'
    }
    return mapping.get(code)

def check_subscription(expiry_date):
    if expiry_date == 'N/A':
        return 'Null'
    now = datetime.now()
    expire_date = datetime.strptime(str(expiry_date), "%Y-%m-%d %H:%M:%S.%f")
    return expire_date > now

def get_wallet_message(symbol: str):
    symbol = symbol.upper()
    wallets = {
        'USDT': 'TEApEsk2WxhfN8xmpJbBPgWBbe5sApFR8d',
        'BTC': '1LQeaah6k8ZS6khEKye9pb1gB2BNVjv8oa',
        'LTC': 'MHyFSrUt9wVjjWYiWYJhxD7xgAQ9yej54g'
    }

    wallet = wallets.get(symbol, "N/A")

    return fr"""ℹ *Wallet Adresse*
`{wallet}`

Send the amount via the *{symbol}* wallet and send a screenshot to Support\."""
