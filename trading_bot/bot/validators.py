import logging
logger = logging.getLogger("TradingBot")

def validate_inputs(symbol: str, side: str, order_type: str, quantity: float, price: float = None):
    validation_failures = []
    
    if not symbol or not symbol.isalnum():
        validation_failures.append("Invalid Crypto Symbol format.")
        
    if side.upper() not in ["BUY", "SELL"]:
        validation_failures.append(f"Side '{side}' must be BUY or SELL.")
        
    if order_type.upper() not in ["MARKET", "LIMIT"]:
        validation_failures.append(f"Type '{order_type}' must be MARKET or LIMIT.")
        
    if quantity <= 0:
        validation_failures.append("Quantity must be greater than 0.")
        
    if order_type.upper() == "LIMIT":
        if price is None or price <= 0:
            validation_failures.append("LIMIT orders require a price greater than 0.")
            
    if validation_failures:
        for failure in validation_failures:
            logger.error(f"VALIDATION FAILURE: {failure}")
        return False, validation_failures
        
    return True, []