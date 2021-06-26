import json
import requests
from config import settings
from common.search import Search
from config.log import logger


class HunterSearch(Search):
    def __init__(self):
        Search.__init__(self)
        self.source = 'HunterAPISearch'
        self.url = "https://api.hunter.io/v2/"
        self.key = settings.hunter_api_key
        self.module = 'Personal'
        self.proxy = self.get_proxy(self.source)
        self.filename = None
        self.content = None
        self.search_data = []
        self.usage = settings.hunter_usage

    def hunter_verify(self):
        requests_available_count, verifications_available_count = None, None
        try:
            message = requests.get(self.url + "account?&api_key=%s" % self.key).text
            message = json.loads(message)['data']
            email = message['email']
            plan_name = message['plan_name']
            requests_available_count = message['requests']['searches']['available'] - message['requests']['searches']['used']
            verifications_available_count = message['requests']['verifications']['available'] - message['requests']['verifications']['used']
            print('username:%s, plan:%s, 请求余额:%d, 验证余额:%d' %(email, plan_name, requests_available_count,
                                                                 verifications_available_count))
        except Exception as e:
            print(e)
        if requests_available_count or verifications_available_count:
            return True
        else:
            return None

    def search_email(self, targets):
            # 查询域下的所有邮箱
        if 'http' not in targets:
            """
            Structure
            data: contains the data you requested.
            meta: provides information regarding your request.
            errors: shows errors with insights regarding what made the request fail. Learn more about the errors responses.
            """
            hunter_email_count = json.loads(requests.get(self.url + 'email-count?domain=%s' % targets).text)

            if hunter_email_count['data']['total']:
                print('在互联网上找到 %d 条邮箱数据' % hunter_email_count['data']['total'])
                hunter_email_search = requests.get(self.url + "domain-search?domain=%s&type=personal&api_key=%s"
                                                   % (targets, self.key), timeout=(5, 10)).json()
        # 找到文章的作者以及给定域名上最有可能的电子邮件地址。
        else:
            hunter_email_search = requests.get(
                self.url + "author-finder?url=%s&api_key=%s" % (targets, self.key)).json()
            if hunter_email_search['data']['domain']:
                print('找到文章的作者以及给定域名上最有可能的电子邮件地址')

        # 两种返回结果都取 'data' 的值
        self.search_data.append(hunter_email_search['data'])

    def run(self, targets):
        print(self.usage)
        if not self.have_api(self.key):
            return
        if not HunterSearch.hunter_verify(self):
            return
        for i in targets:
            HunterSearch.search_email(self, i)
        print(json.dumps(self.search_data, sort_keys=False, indent=4))
        self.finish()
        return json.dumps(self.search_data, ensure_ascii=False)

def run(targets):
    search = HunterSearch()
    search_data = search.run(targets)
    return search_data

if __name__ == '__main__':
    run(['http://www.watersprings.org/pub/id/draft-bonica-6man-vpn-dest-opt-05.html', 'http://lkml.org'])
