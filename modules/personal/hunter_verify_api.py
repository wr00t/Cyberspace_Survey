import json
import requests
from config import settings
from common.search import Search
from config.log import logger
import modules.personal.hunter_search_api as hunter_search


class HunterVerify(Search):
    def __init__(self):
        Search.__init__(self)
        self.source = 'HunterAPIVerify'
        self.url = "https://api.hunter.io/v2/"
        self.key = settings.hunter_api_key
        self.module = 'Personal'
        self.proxy = self.get_proxy(self.source)
        self.filename = None
        self.content = None
        self.search_data = []
        self.usage = settings.hunter_usage

    def verify_email(self, targets):
        try:
            hunter_email_verify = requests.get(self.url + "email-verifier?email=%s&type=personal&api_key=%s"
                                               % (targets, self.key), timeout=(5, 10)).json()
            self.search_data.append(hunter_email_verify['data'])
        except Exception as e:
            logger.log('ERROR', e.args)

    def run(self, targets):
        print(self.usage)
        if not self.have_api(self.key):
            return
        # 调用 HunterSearch 的 hunter_verify
        if not hunter_search.HunterSearch.hunter_verify(self):
            return
        for i in targets:
            HunterVerify.verify_email(self, i)
        print(json.dumps(self.search_data, sort_keys=False, indent=4))
        self.finish()
        return json.dumps(self.search_data, ensure_ascii=False)

def run(targets):
    search = HunterVerify()
    search_data = search.run(targets)
    return search_data

if __name__ == '__main__':
    run(['123@qq.com', '123@bytedance.com'])
