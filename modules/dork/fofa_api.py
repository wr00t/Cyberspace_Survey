import json
import requests
import base64
from config import settings
from common.search import Search
from config.log import logger


class Fofa(Search):
    def __init__(self):
        Search.__init__(self)
        self.source = 'FoFaAPISearch'
        self.url = "https://fofa.so/api/v1/search/all"
        self.email = settings.fofa_api_email
        self.key = settings.fofa_api_key
        self.module = 'Search'
        self.proxy = self.get_proxy(self.source)
        self.filename = None
        self.content = None
        self.search_data = None
        self.usage = settings.fofa_usage

    def search(self):
        try:
            fofa_dork = input('请输入 fofa dork: ')
            fofa_dork_base64 = base64.b64encode(fofa_dork.encode())
            fofa_dork_base64 = bytes.decode(fofa_dork_base64)
            # fofa_search_data = requests.get(self.url, verify=False, proxies=self.proxies).json()
            tmp_url = self.url + '?email=%s&key=%s' % (self.email, self.key) + "&qbase64={}".format(fofa_dork_base64)
            fofa_search_data = requests.get(tmp_url, verify=self.verify, proxies=self.proxy).json()
            self.search_data = fofa_search_data['results']

        except Exception as e:
            logger.log('ERROR', e)



    def run(self):
        print(self.usage)
        if not self.have_api(self.email, self.key):
            return
        self.begin()
        Fofa.search(self)
        print(json.dumps(self.search_data, sort_keys=False, indent=4))
        self.finish()
        return json.dumps(self.search_data, ensure_ascii=False)

def run():
    search = Fofa()
    search_data = search.run()
    return search_data

if __name__ == '__main__':
    run()
