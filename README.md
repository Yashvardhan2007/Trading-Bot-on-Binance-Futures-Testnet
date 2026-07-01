# Trading-Bot-on-Binance-Futures-Testnet
# 🚀 Binance Futures Testnet Trading Bot with Dashboard UI

A robust, modern Python trading application designed for the PrimeTrade.ai internship assignment. This system features a dual-mode execution entry framework, operating both as a high-efficiency Command Line Interface (CLI) and a sleek, dark-mode desktop terminal panel.

---

## 🛠️ System Architecture & File Layout
The codebase is structured cleanly into decoupled functional layers following industry-standard production practices:

```text
trading_bot/
  ├── bot/
  │    ├── __init__.py
  │    ├── client.py        # Binance client wrapper (HMAC SHA256 signing)
  │    ├── orders.py        # Order placement layer logic
  │    ├── validators.py    # Local parameter input validation engine
  │    └── ui.py            # CustomTkinter Dark-Mode visual dashboard layer
  ├── cli.py                # Dual-mode execution entry-point
  ├── bot.log               # Persistent diagnostic transaction logging file
  └── requirements.txt      # System dependencies matrix


  ✨ Core Features Implemented
Dual-Mode Execution Entry-Point: Automatically shifts execution based on user context. Passing terminal flags triggers pure script execution; launching with no arguments automatically boots the modern desktop visual interface panel.

Cryptographic Authentication Layer: Fully signed API requests containing custom query encoding strings and HMAC SHA256 encryption signatures generated locally via timestamps.

Robust Input Validation Framework: Catches structural formatting anomalies, illegal parameters, or missing boundary quantities locally before making network API calls.

TradingView Chart Pairing UI (Bonus Feature): Features a custom dashboard component button that opens a browser window mapped directly to the live trading charts on the exchange.

Production-Grade Logging Protocol: Writes detailed operational logs to bot.log tracking exact JSON payloads transmitted and the subsequent raw structural execution responses returned by the Binance engine.

🔑 How to Configure Your Binance API Keys
This application strictly relies on system environment variables to isolate sensitive credentials securely. Do not hardcode your private keys into the source files.

To test this application with your own Binance Testnet account, you must export your API credentials to your terminal environment session before running the scripts.

💻 On Linux / macOS / GitHub Codespaces:
Run these commands in your terminal (replace the placeholder text with your actual testnet keys):
export BINANCE_API_KEY="your_actual_testnet_api_key_here"
export BINANCE_API_SECRET="your_actual_testnet_secret_key_here"

🪟 On Windows (PowerShell):
Run these commands in your PowerShell window (replace the placeholder text with your actual testnet keys):

PowerShell
$env:BINANCE_API_KEY="your_actual_testnet_api_key_here"
$env:BINANCE_API_SECRET="your_actual_testnet_secret_key_here"
🚀 Step-by-Step Setup & Important Execution Commands
1. Installation
Install the project dependencies inside your terminal:

Bash
pip install -r requirements.txt
2. Pure CLI Flag Mode (Instant Execution)
Run standard transactions instantly directly inside your command terminal workspace using these commands:

Bash
# Execute an instantaneous MARKET BUY order
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.005

# Deploy a specific target LIMIT SELL order
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.005 --price 75000
3. Advanced Desktop GUI Control Panel Mode
To experience the interactive visual trading station dashboard, execute the entry-point script without passing any structural terminal flags:

Bash
python cli.py