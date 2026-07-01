# ⚡ PRIME TRADE — Binance Futures Trading Bot

## 🛠️ Installation & Setup

### 1. Install Dependencies
Run the package manager sequence to install all required libraries:
```bash
pip install -r trading_bot/requirements.txt

2. Configure API Credentials
Navigate to the project directory:

Bash
cd trading_bot
Copy the configuration template to create your secure environment profile:

Bash
cp .env.example .env
Open the newly created .env file and replace the placeholder text with your real Binance Testnet keys (do not use quotation marks):

Ini, TOML
BINANCE_TESTNET_API_KEY=your_actual_api_key_here
BINANCE_TESTNET_SECRET_KEY=your_actual_secret_key_here

{ IF YOU WANT A GRAPHICAL INTERFACE THEN DOWNLODE IT AND RUN IN YOU POWER SHELL}
💻 Running the GUI (Visual Pop-up Window)
If you want to view a graphical interface instead of using terminal arguments, simply run cli.py with no flags. A clean desktop application window will pop up automatically:

Bash
python cli.py
📦 Key GUI Features:
One-Click Execution: Dedicated visual buttons to submit Market Orders instantly.

Limit Order Modals: Clean input boxes to specify target entries and exit prices.

Real-time Logs: A live visual printout window inside the UI showing exchange response receipts directly.

{IF WANT TO TRY IT IN GITHUB THE USE THIS METHOD}


🚀 Execution Commands
Ensure you are inside the trading_bot directory before executing commands:
Bash
cd trading_bot
1. Market BUY Order
Execute an immediate buy order at current market rates:

Bash
python cli.py --side BUY --type MARKET --symbol BTCUSDT --qty 0.005
2. Market SELL Order (Short)
Execute an immediate short position at current market rates:

Bash
python cli.py --side SELL --type MARKET --symbol BTCUSDT --qty 0.005
3. Limit BUY Order
Set a pending buy order triggered when the asset drops to your specific target entry floor:

Bash
python cli.py --side BUY --type LIMIT --symbol BTCUSDT --qty 0.005 --price 91200

4. Limit SELL Order
Set a pending limit sell order or take profit threshold:

Bash
python cli.py --side SELL --type LIMIT --symbol BTCUSDT --qty 0.005 --price 102500
