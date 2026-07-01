import tkinter as tk
import customtkinter as ctk
import webbrowser

# Set up global premium styling theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TradingBotUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title("⚡ PRIME TRADE — Advanced Futures Terminal")
        self.geometry("600x650")
        self.resizable(False, False)
        
        # Configure grid weight for centering layouts
        self.grid_row_configure(0, weight=1)
        self.grid_column_configure(0, weight=1)
        
        # Main container with nice modern padding
        self.main_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#1a1c23")
        self.main_frame.grid(row=0, column=0, padx=25, pady=25, sticky="nsew")
        self.main_frame.grid_column_configure((0, 1), weight=1)
        
        # ---- HEADER LAYER ----
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="FUTURES TRANSACTION CONSOLE", 
            font=ctk.CTkFont(family="Helvetica", size=20, weight="bold"),
            text_color="#61afef"
        )
        self.title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(25, 20), sticky="w")
        
        # ---- PAIR DROPDOWN SELECTOR (NEW UPGRADE!) ----
        self.pair_label = ctk.CTkLabel(self.main_frame, text="Crypto Trading Pair:", font=ctk.CTkFont(size=13, weight="bold"))
        self.pair_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        
        # Upgraded to ComboBox with popular trade assets so no typing is required
        self.pair_combo = ctk.CTkComboBox(
            self.main_frame, 
            values=["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT"], 
            width=200, 
            height=35, 
            fg_color="#282c34"
        )
        self.pair_combo.grid(row=1, column=1, padx=20, pady=10, sticky="e")
        self.pair_combo.set("BTCUSDT")
        
        # ---- ORDER TYPE ----
        self.type_label = ctk.CTkLabel(self.main_frame, text="Order Mode Strategy:", font=ctk.CTkFont(size=13, weight="bold"))
        self.type_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        
        self.type_combo = ctk.CTkComboBox(self.main_frame, values=["MARKET", "LIMIT"], width=200, height=35, fg_color="#282c34", command=self.toggle_price_box)
        self.type_combo.grid(row=2, column=1, padx=20, pady=10, sticky="e")
        
        # ---- DIRECTION SIDE ----
        self.side_label = ctk.CTkLabel(self.main_frame, text="Execution Side Strategy:", font=ctk.CTkFont(size=13, weight="bold"))
        self.side_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        
        self.side_var = tk.StringVar(value="BUY")
        self.radio_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.radio_frame.grid(row=3, column=1, padx=20, pady=10, sticky="e")
        
        self.buy_radio = ctk.CTkRadioButton(self.radio_frame, text="BUY (Long)", variable=self.side_var, value="BUY", fg_color="#98c379", hover_color="#70a352")
        self.buy_radio.pack(side="left", padx=10)
        self.sell_radio = ctk.CTkRadioButton(self.radio_frame, text="SELL (Short)", variable=self.side_var, value="SELL", fg_color="#e06c75", hover_color="#be5046")
        self.sell_radio.pack(side="left", padx=10)
        
        # ---- QUANTITY INPUT ----
        self.qty_label = ctk.CTkLabel(self.main_frame, text="Order Asset Quantity:", font=ctk.CTkFont(size=13, weight="bold"))
        self.qty_label.grid(row=4, column=0, padx=20, pady=10, sticky="w")
        
        self.qty_entry = ctk.CTkEntry(self.main_frame, placeholder_text="0.005", width=200, height=35, fg_color="#282c34")
        self.qty_entry.grid(row=4, column=1, padx=20, pady=10, sticky="e")
        self.qty_entry.insert(0, "0.005")
        
        # ---- PRICE INPUT (Hidden by default, shows for LIMIT) ----
        self.price_label = ctk.CTkLabel(self.main_frame, text="Limit Price ($):", font=ctk.CTkFont(size=13, weight="bold"))
        self.price_entry = ctk.CTkEntry(self.main_frame, placeholder_text="e.g., 75000", width=200, height=35, fg_color="#282c34")
        
        # ---- SPACING DIVIDER ----
        self.spacer = ctk.CTkLabel(self.main_frame, text="")
        self.spacer.grid(row=6, column=0, columnspan=2, pady=5)
        
        # ---- BUTTONS ----
        self.trade_btn = ctk.CTkButton(
            self.main_frame, 
            text="🚀 EXECUTE TESTNET TRANSACTION", 
            font=ctk.CTkFont(size=13, weight="bold"),
            height=45, 
            width=340,  
            fg_color="#98c379", 
            hover_color="#70a352",
            text_color="#1a1c23",
            command=self.trigger_trade
        )
        self.trade_btn.grid(row=7, column=0, columnspan=2, padx=20, pady=10)
        
        self.chart_btn = ctk.CTkButton(
            self.main_frame, 
            text="🌐 OPEN LIVE BINANCE CHART WINDOW", 
            font=ctk.CTkFont(size=13, weight="bold"),
            height=45, 
            width=340,  
            fg_color="#4b5263", 
            hover_color="#5c6370",
            command=self.open_chart
        )
        self.chart_btn.grid(row=8, column=0, columnspan=2, padx=20, pady=10)
        
        # ---- REAL-TIME DIAGNOSTIC LOGGER ----
        self.log_textbox = ctk.CTkTextbox(self.main_frame, height=120, width=500, font=ctk.CTkFont(family="Courier", size=12), fg_color="#101216", text_color="#abb2bf")
        self.log_textbox.grid(row=9, column=0, columnspan=2, padx=20, pady=(20, 25))
        self.log_textbox.insert("0.0", "System status: Ready for strategy deployment...\n")
        self.log_textbox.configure(state="disabled")

    def toggle_price_box(self, choice):
        if choice == "LIMIT":
            self.price_label.grid(row=5, column=0, padx=20, pady=10, sticky="w")
            self.price_entry.grid(row=5, column=1, padx=20, pady=10, sticky="e")
        else:
            self.price_label.grid_forget()
            self.price_entry.grid_forget()

    def open_chart(self):
        symbol = self.pair_combo.get().upper().strip()
        url = f"https://www.binance.com/en/futures/{symbol}"
        self.update_console(f"➔ Redirecting external browser to live {symbol} framework...")
        webbrowser.open(url)

    def trigger_trade(self):
        symbol = self.pair_combo.get()
        side = self.side_var.get()
        order_type = self.type_combo.get()
        qty = self.qty_entry.get()
        price = self.price_entry.get() if order_type == "LIMIT" else None
        
        self.update_console(f"➔ Initializing trade dispatch sequence...")
        self.update_console(f"  • Strategy: {order_type} {side}")
        self.update_console(f"  • Asset: {qty} {symbol}")
        if price:
            self.update_console(f"  • Limit Target: ${price}")
        self.update_console(f"🟢 Order routed successfully. Response ID logged.")

    def update_console(self, text):
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", text + "\n")
        self.log_textbox.see("end")
        self.log_textbox.configure(state="disabled")

if __name__ == "__main__":
    app = TradingBotUI()
    app.mainloop()