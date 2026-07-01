import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode
import logging

# Persistent logger configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()]
)
logger = logging.getLogger("TradingBot")

class BinanceTestnetClient:
    def __init__(self, api_key: str, api_secret: str):
        self.base_url = "https://testnet.binancefuture.com"
        self.api_key = api_key
        self.api_secret = api_secret
        
        if not self.api_key or not self.api_secret:
            logger.error("API Key or Secret is missing in environment variables!")
            raise ValueError("API credentials must be provided.")

    def _generate_signature(self, params: dict) -> str:
        query_string = urlencode(params)
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def send_signed_request(self, method: str, endpoint: str, params: dict = None) -> dict:
        if params is None:
            params = {}
            
        url = f"{self.base_url}{endpoint}"
        params['timestamp'] = int(time.time() * 1000)
        params['signature'] = self._generate_signature(params)
        
        headers = {
            "X-MBX-APIKEY": self.api_key
        }
        
        logger.info(f"Sending {method} request to {endpoint} with parameters: {params}")
        
        try:
            if method.upper() == "POST":
                response = requests.post(url, headers=headers, data=params, timeout=10)
            else:
                response = requests.get(url, headers=headers, params=params, timeout=10)
                
            res_json = response.json()
            
            if response.status_code != 200:
                logger.error(f"Binance API Error {response.status_code}: {res_json}")
                return {"success": False, "error": res_json.get("msg", "Unknown API error")}
                
            logger.info(f"Successful Binance Response: {res_json}")
            return {"success": True, "data": res_json}
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Network / Connection error: {str(e)}")
            return {"success": False, "error": f"Network Error: {str(e)}"}