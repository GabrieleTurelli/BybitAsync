import json
import aiohttp
import time
import hmac
import hashlib


def _dict_to_query_string(params: dict) -> str:
    """
    Convert a dictionary to a query string.

    :param params: Dictionary to be converted.
    :return: Query string.
    """
    return '&'.join([f'{key}={value}' for key, value in params.items()])


class Bybit_requester:
    """
    Initialize the Bybit_requester.

    :param api_key: Your API key as a string.
    :param api_secret: Your API secret as a string.
    """
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.recv_window = str(5000)
        self.base_url = "https://api.bybit.com"

    async def send_public_request(self, endpoint: str, params: dict = None) -> dict:
        """
        Send a public request to the Bybit API.

        :param endpoint: The API endpoint to which the request is sent.
        :param params: Optional dictionary of parameters to be sent with the request.
        :return: The response from the API as a dictionary.
        """
        url = f"{self.base_url}{endpoint}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                return await response.json()

    async def send_signed_request(self, method: str, endpoint: str, params: dict):
        """
        Send a signed (private) request to the Bybit API.

        :param method: HTTP method ('GET' or 'POST') for the request.
        :param endpoint: The API endpoint to which the request is sent.
        :param params: Dictionary of parameters to be sent with the request.
        :return: The response from the API as a dictionary.
        """
        time_stamp = str(int(time.time() * 10 ** 3))
        signature = self._gen_signature(params, time_stamp, method)
        headers = {
            'X-BAPI-API-KEY': self.api_key,
            'X-BAPI-SIGN': signature,
            'X-BAPI-SIGN-TYPE': '2',
            'X-BAPI-TIMESTAMP': str(time_stamp),
            'X-BAPI-RECV-WINDOW': self.recv_window,
            'Content-Type': 'application/json',
            "Accept": "application/json"
        }
        url = f"{self.base_url}{endpoint}"
        async with aiohttp.ClientSession() as session:

            if method == "POST":
                async with session.request("POST", url, headers=headers, data=json.dumps(params)) as response:
                    response.raise_for_status()
                    return await response.json()

            elif method == "GET":
                params = _dict_to_query_string(params)
                url = url + "?" + params

                async with session.request("GET", url, headers=headers) as response:
                    response.raise_for_status()
                    return await response.json()

    def _gen_signature(self, params: dict, time_stamp: str, method: str):
        """
        Generate a signature for a private API request.

        :param params: Dictionary of parameters for the request.
        :param time_stamp: Timestamp string for the signature.
        :param method: HTTP method ('GET' or 'POST') for the request.
        :return: The generated signature as a string.
        """
        if method.upper() == "POST":
            params = json.dumps(params)
            param_str = time_stamp + self.api_key + self.recv_window + str(params)
        else:
            param_str = time_stamp + self.api_key + self.recv_window + str(_dict_to_query_string(params))

        hash = hmac.new(bytes(self.api_secret, "utf-8"), param_str.encode("utf-8"), hashlib.sha256)
        return hash.hexdigest()




