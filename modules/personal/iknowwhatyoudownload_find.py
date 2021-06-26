import json
import requests
from config import settings
from common.search import Search
from config.log import logger


class IknowwhatyoudownloadFind(Search):
    def __init__(self):
        Search.__init__(self)
        self.source = 'IknowwhatyoudownloadAPI'
        self.url = "https://api.antitor.com"
        self.key = settings.iknowwhatyoudownload_api_key
        self.module = 'Personal'
        self.proxy = self.get_proxy(self.source)
        self.filename = None
        self.content = None
        self.search_data = []
        self.usage = settings.iknowwhatyoudownload_find_usage

    def download_find(self, targets):
        try:
            iknowwhatyoudownload_result = requests.get(self.url + '/history/peer/?ip=%s&contents=30&key=%s' % (targets, self.key), timeout=(5, 10)).json()
            if iknowwhatyoudownload_result['contents']:
                self.search_data.append(iknowwhatyoudownload_result)
        except Exception as e:
            logger.log('ERROR', e.args)
        return self.search_data

    def run(self, targets):
        self.begin()
        print(self.usage)
        if not self.have_api(self.key):
            return
        for i in targets:
            IknowwhatyoudownloadFind.download_find(self, i)
        print(json.dumps(self.search_data, sort_keys=False, indent=4, ensure_ascii=False))
        self.finish()
        return json.dumps(self.search_data, ensure_ascii=False)

def run(targets):
    search = IknowwhatyoudownloadFind()
    search_data = search.run(targets)
    return search_data

if __name__ == '__main__':
    run(['8.8.8.8'])


