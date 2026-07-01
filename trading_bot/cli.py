import sys
import os
import argparse
import logging
from bot.validators import validate_inputs
from bot.client import BinanceTestnetClient
from bot.orders import OrderManager

logging.basicConfig(level=logging.INFO)

def run_pure_cli(args):
    """Executes when user passes terminal flags directly."""
    print("==============================================")
    print("      🚀 BINANCE FUTURES TESTNET CLI         ")
    print("==============================================")
    
    symbol = args.symbol.upper()
    side = args.side.upper()
    order_type = args.type.upper()
    quantity = args.quantity
    price = args.price

    # Validate inputs using your system validator
    is_valid, errors = validate_inputs(symbol, side, order_type, quantity, price)
    if not is_valid:
        print("\n❌ Input Validation Failed:")
        for err in errors:
            print(f" - {err}")
        return

    # Check for keys
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    if not api_key or not api_secret:
        print("\n❌ System Error: Missing BINANCE_API_KEY or BINANCE_API_SECRET environment variables!")
        return

    try:
        client = BinanceTestnetClient(api_key, api_secret)
        manager = OrderManager(client)
        
        print(f"\n➔ Dispatching Request: {order_type} {side} {quantity} {symbol}" + (f" @ ${price}" if price else ""))
        res = manager.place_order(symbol, side, order_type, quantity, price)
        
        if res.get("success"):
            data = res["data"]
            print("\n=================== RESULT ===================")
            print("✅ Order Placed Successfully!")
            print(f"• Order ID      : {data.get('orderId')}")
            print(f"• Status        : {data.get('status')}")
            print("==============================================\n")
        else:
            print(f"\n❌ Exchange Rejected: {res.get('error')}")
    except Exception as e:
        print(f"\n💥 Connection Failure: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Engine")
    parser.add_argument("--symbol", type=str, help="Trading Pair (e.g., BTCUSDT)")
    parser.add_argument("--side", type=str, choices=["BUY", "SELL"], help="Order Side (BUY/SELL)")
    parser.add_argument("--type", type=str, choices=["MARKET", "LIMIT"], help="Order Type (MARKET/LIMIT)")
    parser.add_argument("--quantity", type=float, help="Order Quantity")
    parser.add_argument("--price", type=float, help="Limit Price (Only for LIMIT orders)")

    # If any arguments are provided via command line, parse them and run CLI mode
    if len(sys.argv) > 1:
        args = parser.parse_args()
        if args.symbol and args.side and args.type and args.quantity is not None:
            run_pure_cli(args)
        else:
            print("⚠️ Missing parameters. Usage example:")
            print("python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01")
    else:
        # No flags passed? Launch your awesome custom GUI app automatically!
        print("==============================================")
        print("      🚀 BINANCE FUTURES TESTNET TERMINAL     ")
        print("==============================================")
        print("Launching control panel graphical interface...")
        from bot.ui import TradingBotUI
        app = TradingBotUI()
        app.mainloop()