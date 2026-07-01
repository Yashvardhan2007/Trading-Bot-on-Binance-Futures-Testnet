import sys
import os
import requests
from dotenv import load_dotenv

# Path safety configurations - explicitly target the .env file in this directory
base_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(base_dir, ".env"))

from bot.orders import OrderManager

# Load keys and automatically strip away any accidental quotation marks
BINANCE_TESTNET_API_KEY = os.getenv("BINANCE_TESTNET_API_KEY", "").strip('"').strip("'")
BINANCE_TESTNET_SECRET_KEY = os.getenv("BINANCE_TESTNET_SECRET_KEY", "").strip('"').strip("'")

class RealBinanceClient:
    def __init__(self):
        self.base_url = "https://testnet.binancefuture.com"
        self.api_key = BINANCE_TESTNET_API_KEY
        self.secret_key = BINANCE_TESTNET_SECRET_KEY

    def send_signed_request(self, method, endpoint, params):
        import time
        import hmac
        import hashlib
        
        if not self.api_key or not self.secret_key:
            return {"error_local": True, "msg": "Missing credentials. Please check your .env file."}
            
        url = self.base_url + endpoint
        params['timestamp'] = int(time.time() * 1000)
        
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        signature = hmac.new(self.secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        params['signature'] = signature
        
        headers = {
            'X-MBX-APIKEY': self.api_key,
            'User-Agent': 'Mozilla/5.0'
        }
        
        try:
            if method.upper() == "POST":
                response = requests.post(url, params=params, headers=headers, timeout=10)
                return response.json()
        except Exception as e:
            return {"error_local": True, "msg": str(e)}

client_instance = RealBinanceClient()
order_manager = OrderManager(client_instance)

# =====================================================================
# MAIN EXECUTION ROUTER
# =====================================================================
if len(sys.argv) > 1:
    print("\n🚀 --- EXECUTING CLI TERMINAL TRANSACTION ---")
    
    import argparse
    parser = argparse.ArgumentParser(description="⚡ PRIME TRADE Terminal")
    parser.add_argument('--side', type=str, required=True, choices=['BUY', 'SELL'])
    parser.add_argument('--type', type=str, default='MARKET', choices=['MARKET', 'LIMIT'])
    parser.add_argument('--symbol', type=str, default='BTCUSDT')
    parser.add_argument('--qty', type=float, required=True)
    parser.add_argument('--price', type=float, default=None)
    
    args = parser.parse_args()
    
    if args.type == 'LIMIT' and args.price is None:
        print("❌ Configuration Error: --price must be specified when using --type LIMIT")
        sys.exit(1)
        
    print(f"➔ Dispatching Strategy Sequence...")
    
    try:
        response = order_manager.place_order(
            symbol=args.symbol, 
            side=args.side, 
            order_type=args.type, 
            quantity=args.qty,
            price=args.price
        )
        
        if isinstance(response, dict) and ("code" in response or "error_local" in response):
            print(f"❌ Transaction Rejected by Exchange Core!")
            print(f"   • Error Log Message: {response.get('msg', 'Unknown Server Exception')}")
            if "code" in response:
                print(f"   • Server Error Code: {response['code']}")
        else:
            print(f"🟢 Order Success! Server Response: {response}")
            
    except Exception as e:
        print(f"❌ Framework Execution Crash: {str(e)}")
        
else:
    print("Launching control panel graphical interface...")
    from bot.ui import TradingBotUI
    app = TradingBotUI(order_manager=order_manager)
    app.mainloop()
