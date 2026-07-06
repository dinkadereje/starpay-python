import json
import hmac
import hashlib
from urllib import request, error
from typing import Optional, Dict, Any, List

from .exceptions import StarPayAPIError, StarPaySignatureError

class StarPayClient:
    """
    Client for interacting with the StarPay API.
    """
    
    def __init__(self, api_url: str, api_secret: str, merchant_id: str):
        self.api_url = api_url.rstrip('/')
        self.api_secret = api_secret
        self.merchant_id = merchant_id

    def create_order(
        self,
        amount: float,
        description: str,
        customer_name: str,
        customer_phone: str,
        callback_url: str,
        items: List[Dict[str, Any]],
        metadata: Optional[Dict[str, Any]] = None,
        order_id: Optional[str] = None
    ) -> Optional[str]:
        """
        Creates an order in StarPay and returns the payment URL.
        
        :param amount: Total amount for the order
        :param description: Description of the order
        :param customer_name: Full name of the customer
        :param customer_phone: Phone number of the customer
        :param callback_url: Webhook callback URL
        :param items: List of dictionaries with productId, quantity, item_name, unit_price
        :param metadata: Optional dictionary with metadata
        :param order_id: Optional string for the order id, used in mock mode
        :return: Payment URL as a string
        """
        payload = {
            "amount": amount,
            "description": description,
            "currency": "ETB",
            "customerName": customer_name,
            "customerPhoneNumber": customer_phone,
            "callbackURL": callback_url,
            "redirectUrl": callback_url,
            "items": items,
        }
        
        if metadata:
            payload["metadata"] = metadata

        headers = {
            "Content-Type": "application/json",
            "x-api-secret": self.api_secret
        }

        # Mock implementation for testing if we don't have a real secret
        if self.api_secret == 'mock_secret_for_testing':
            oid = order_id or "mock"
            return f"https://sandbox.starpayethiopia.com/checkout/{oid}"

        try:
            req = request.Request(
                f"{self.api_url}/trdp/order",
                data=json.dumps(payload).encode('utf-8'),
                headers=headers,
                method='POST'
            )
            with request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                if data.get('status') == 'success':
                    return data['data']['payment_url']
                else:
                    raise StarPayAPIError(f"StarPay order creation failed: {data}")
        except error.HTTPError as e:
            raise StarPayAPIError(f"HTTPError communicating with StarPay: {e.code} - {e.read()}")
        except Exception as e:
            if isinstance(e, StarPayAPIError):
                raise
            raise StarPayAPIError(f"Error communicating with StarPay: {e}")

    def verify_signature(self, payload: Dict[str, Any], timestamp: str, signature: str) -> bool:
        """
        Verifies the HMAC-SHA256 signature from StarPay callbacks.
        
        :param payload: The JSON payload received in the webhook (as a dictionary)
        :param timestamp: The timestamp string from the webhook header
        :param signature: The signature string from the webhook header
        :return: True if the signature is valid, False otherwise
        """
        try:
            body = json.dumps(payload, separators=(",", ":"))
            message = f"{timestamp}.{body}"
            
            expected_signature = hmac.new(
                self.api_secret.encode("utf-8"),
                message.encode("utf-8"),
                hashlib.sha256
            ).hexdigest()
            
            return hmac.compare_digest(expected_signature, signature)
        except Exception as e:
            raise StarPaySignatureError(f"Signature verification error: {e}")
