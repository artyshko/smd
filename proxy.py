from proxyscrape import create_collector, get_collector

def getProxy(log=True):

    try:

        collector = create_collector(
            'smd-collector',
            ('http', 'https', 'socks4', 'socks5')
        )

    except:

        collector = get_collector('smd-collector')


    proxy = collector.get_proxy(
        {
            'code': ('us', 'uk'),
            'anonymous': True
        }
    )

    result = {
        'proxy': f'{proxy[5]}://{proxy[0]}:{proxy[1]}'
    }

    if log:
        print(f'| PROXY | {str(proxy[3]).upper()} | {str(proxy[5]).upper()} {"| ANONYMOUS |" if proxy[4] else "| PUBLIC |"} {result["proxy"]} |')

    return result
