import logging
logger = logging.getLogger("TradingBot")

class OrderManager:
    def __init__(self, client):
        self.client = client

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None):
        endpoint = "/fapi/v1/order"
        
        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": order_type.upper(),
            "quantity": str(quantity),
        }
        
        if order_type.upper() == "LIMIT":
            params["price"] = str(price)
            params["timeInForce"] = "GTC"
            
        logger.info(f"Preparing to deploy {order_type} {side} order for {symbol}")
        return self.client.send_signed_request("POST", endpoint, params)