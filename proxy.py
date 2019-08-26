import asyncio
from proxybroker import Broker
import requests

def getProxy(log=True):

    async def show(proxies):
        while True:
            proxy = await proxies.get()
            if proxy is None: break
            print('Found proxy: %s' % proxy)

            return {
                'proxy': f'https://{proxy.host}:{proxy.port}',
                'type':'https',
                'ip':f'https://{proxy.host}',
                'port':proxy.port
            }


    proxies = asyncio.Queue()
    broker = Broker(proxies)
    tasks = asyncio.gather(
        broker.find(types=['HTTPS'], limit=1),
        show(proxies))

    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(tasks)

    return result[1]

def get():

    proxy = getProxy()

    print(proxy)

    _type = proxy['type']
    _proxy = proxy['proxy']

    try:
        requests.get(
            "https://www.youtube.com",
            proxies = {
                _type:_proxy
            }
        )
    except IOError:

        print("Connection error!")
        return get()

    else:

        print("All was fine")
        return proxy



if __name__ == '__main__':

    get()
