# Asynchronous Bybit API v5 Connector in Python
## Introduction
This Python script contains the Bybit_requester class, designed for asynchronous interactions with the Bybit API v5. It facilitates non-blocking API calls for both public and private endpoints, making it ideal for high-frequency trading bots and other real-time data processing applications.

## Features
- **Asynchronous API Calls**: Utilizes `asyncio` and `aiohttp` for efficient, non-blocking operations.

- **Public and Private API Requests**: Easily send requests to both public and private API endpoints.

- **signature Generation**: Automatic generation of signatures for authenticated requests.

## Prerequisites
- Python 3.7 or later.
- aiohttp library.
```bash
$ pip install aiohttp
```

## Installation
Clone this repository and install the required dependencies:

```bash
$ git clone https://github.com/GabrieleTurelli/BybitAsync.git
$ cd bybit-async-connector
$ pip install aiohttp
```
## Usage
### Initialization


Import and initialize **Bybit_requester**:

```python
from bybit_async import Bybit_requester

bybit_requester = Bybit_requester(api_key='your_api_key', api_secret='your_api_secret')
```

### Sending Public Requests

Fetch public market data:

```python
import asyncio
from bybit_async import Bybit_requester


async def fetch_market_data():
    data = await bybit_requester.send_public_request(endpoint='/v5/market/kline', 
                                                     params={'category':'linear',
                                                             'symbol': 'BTCUSDT',
                                                             'interval':'D'})
    print(data)

if __name__ == "__main__":
    bybit_requester = Bybit_requester("your_api_key", "your_api_secret")
    asyncio.run(fetch_market_data())
```
### Sending Private Requests
Place an order:

```python
import asyncio
from bybit_async import Bybit_requester


async def place_order():
    order_data = {
        'category': 'linear',
        'symbol': 'BTCUSDT',
        'orderType': 'Market',
        'side': 'Buy',
        'qty': '0.001',
        'positionIdx': 1
    }
    response = await bybit_requester.send_signed_request(method='POST',
                                                         endpoint='/v5/order/create',
                                                         params=order_data)
    print(response)

if __name__ == "__main__":
    bybit_requester = Bybit_requester("your_api_key", "your_api_secret")
    asyncio.run(place_order())
```
## Bybit API Documentation
For information on available endpoints and their parameters, refer to the [Bybit API Documentation](https://bybit-exchange.github.io/docs/v5/intro).

## Contributing
Contributions are welcome! Please fork this repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer
This software is provided "as is", without warranty of any kind. Use it at your own risk.

