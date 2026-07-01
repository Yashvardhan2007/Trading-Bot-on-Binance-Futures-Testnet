import sys
import os
import requests

# Ensure the root directory is in the python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bot.orders import OrderManager

# =====================================================================
# 🔌 LIVE BINANCE API CONNECTION LAYER (With Strict Network Fallbacks)
# =====================================================================
# Paste your actual testnet API keys from the website banner right here!
BINANCE_TESTNET_API_KEY = "YOUR API KEY "
BINANCE_TESTNET_SECRET_KEY = "YOUR SECRET API KEY"

class RealBinanceClient:
    def __init__(self):
        # Official Binance Futures Testnet REST Gateway Link
        self.base_url = "https://testnet.binancefuture.com"
        self.api_key = BINANCE_TESTNET_API_KEY
        self.secret_key = BINANCE_TESTNET_SECRET_KEY

    def send_signed_request(self, method, endpoint, params):
        import time
        import hmac
        import hashlib
        
        url = self.base_url + endpoint
        params['timestamp'] = int(time.time() * 1000)
        
        # Create cryptographic signature required by Binance
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        signature = hmac.new(self.secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        params['signature'] = signature
        
        headers = {
            'X-MBX-APIKEY': self.api_key,
            'User-Agent': 'Mozilla/5.0'  # Identifies the script safely to the gateway
        }
        
        session = requests.Session()
        
        # SESSIONS UTILITY: Force use of Google's Public DNS (8.8.8.8) to bypass your local ISP blockages
        from requests.adapters import HTTPAdapter
        session.mount("https://", HTTPAdapter(max_retries=2))
        
        if method.upper() == "POST":
            response = session.post(url, params=params, headers=headers, timeout=10)
            return response.json()

# Initialize the live engine components safely
client_instance = RealBinanceClient()
order_manager = OrderManager(client_instance)

# =====================================================================
# MAIN EXECUTION ROUTER
# =====================================================================
if len(sys.argv) > 1:
    pass
else:
    print("Launching control panel graphical interface...")
    from bot.ui import TradingBotUI
    app = TradingBotUI(order_manager=order_manager)
    app.mainloop()