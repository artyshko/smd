from proxyscrape import create_collector, get_collector
import urllib
import requests

def getProxy(log=True):

    try:

        collector = create_collector(
            'smd-collector',
            ('socks4', 'http')
        )

    except:

        collector = get_collector('smd-collector')


    proxy = collector.get_proxy()

    result = {
        'proxy': f'{proxy[5]}://{proxy[0]}:{proxy[1]}',
        'type':proxy[5],
        'ip':f'{proxy[5]}://{proxy[0]}',
        'port':proxy[1]
    }

    if log:
        print(f'| PROXY | {str(proxy[3]).upper()} | {str(proxy[5]).upper()} {"| ANONYMOUS |" if proxy[4] else "| PUBLIC |"} {result["proxy"]} |')

    return result

def get():

    proxy = getProxy()

    _type = proxy['type']
    _proxy = proxy['proxy']

    try:
        requests.get(
            "http://example.com",
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
