from bybit_async import Bybit_requester
import asyncio


async def fetch_market_data():
    market_data = {'category': 'linear',
                   'symbol': 'BTCUSDT',
                   'interval': 'D'}
    data = await bybit_requester.send_public_request(endpoint='/v5/market/kline',
                                                     params=market_data)
    print(data)


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
    asyncio.run(fetch_market_data())

