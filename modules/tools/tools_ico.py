import base64
import json
from config import settings
from common.search import Search
import mmh3
import requests
from config.log import logger


class ICOHASH(Search):
    def __init__(self):
        Search.__init__(self)
        self.source = 'ICOHASH'
        self.module = 'TOOLS'
        self.proxy = self.get_proxy(self.source)
        self.search_data = []
        self.usage = settings.tools_ico_usage

    def search(self, targets):
        headers = self.get_header()
        try:
            response = requests.get('%s' % targets, verify=False, headers=headers, proxies=self.proxy, timeout=(5, 10))
            favicon = base64.b64encode(response.content)
            hash = mmh3.hash(favicon)
            fofa_dork = 'icon_hash=' + str(hash)
            shodan_dork = 'http.favicon.hash:' + str(hash)
            tmp = {'target': targets, 'dork': (fofa_dork, shodan_dork)}
            self.search_data.append(tmp)
        except Exception as e:
            logger.log('ERROR', e)

    def run(self, targets):
        print(self.usage)
        self.begin()
        for i in targets:
            ICOHASH.search(self, i)
        print(json.dumps(self.search_data, sort_keys=False, indent=4))
        self.finish()
        return json.dumps(self.search_data, ensure_ascii=False)

def run(targets):
    search = ICOHASH()
    search_data = search.run(targets)
    return json.dumps(search_data)

if __name__ == '__main__':
    run(['https://www.baidu.com/favicon.ico'])


