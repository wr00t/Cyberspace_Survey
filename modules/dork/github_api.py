import json
import pathlib
import time
import requests
from multiprocessing.dummy import Pool
from config import settings
from common.search import Search
import random
from config.log import logger


class Github(Search):
    def __init__(self):
        Search.__init__(self)
        self.source = 'GithubAPISearch'
        self.token = random.choice(settings.github_token_list)
        self.url = "https://api.github.com/"
        self.module = 'Search'
        self.proxy = self.get_proxy(self.source)
        self.filename = None
        self.content = None
        self.search_data = {}
        self.urls_dict = {}
        self.usage = settings.github_dork_usage
        self.session = requests.Session()


    def __urlencode(self, str):
        str = str.replace(':', '%3A');
        str = str.replace('"', '%22');
        str = str.replace(' ', '+');
        return str

    def github_dork(self, url):
        self.token = random.choice(settings.github_token_list)
        self.session.headers = self.get_header()
        self.session.proxies = self.get_proxy(self.source)
        self.session.verify = self.verify
        self.session.headers.update(
            {'Accept': 'application/vnd.github.v3.text-match+json'})
        headers = {'Authorization': 'token ' + self.token}
        try:
            response = requests.get(url, headers=headers, timeout=(5, 10)).json()
            if 'documentation_url' in response:
                logger.log('ERROR', response['errors'][0]['message'])
            else:
                self.search_data[url] = response['total_count']
            time.sleep(random.random())
        except:
            logger.log('ERROR', response['message'])


    def search(self,):
        github_dork = input('请输入 github dork: ')
        relative_directory = pathlib.Path(__file__).parent.parent
        dic = input('请输入字典路径(不输入默认为 dictionary/github_dorks_minimum.txt): ')
        if dic == '':
            dic = 'dictionary/github_dorks_minimum.txt'
        with open(dic, 'r') as f:
            for i in f.readlines():
                if i.strip():
                    query_dork = self.__urlencode(i.strip() + ' ' + github_dork)
                    url = self.url + 'search/code?per_page=100&s=indexed&type=Code&o=desc&q=%s' % query_dork
                    self.urls_dict[url] = 0

        # POOL FUNCTION TO RUN API SEARCH(原先是采取多线程的方法,但是线程过高,导致 API rate limit)
        # pool = Pool(3)
        # pool.map(self.github_dork, self.urls_dict)
        # pool.close()
        # pool.join()

        # 目前改为单线程发送请求
        for i in self.urls_dict.keys():
            self.github_dork(i)

        # key 为搜索 url, value 为搜索出的数量, 如果value 为 0,则删除掉 key
        if self.search_data.keys():
            for key in list(self.search_data.keys()):
                if self.search_data[key] == 0:
                    del self.search_data[key]
        return self.search_data

    def run(self):
        print(self.usage)
        if not self.have_api(self.token):
            return
        if not self.auth_github(self.url):
            return
        self.begin()
        """
        类统一调用入口
        :param str domain: 域名
        """
        Github.search(self)
        print(json.dumps(self.search_data, sort_keys=False, indent=4))
        self.finish()
        return json.dumps(self.search_data, ensure_ascii=False)

def run():
    search = Github()
    search_data = search.run()
    return json.dumps(search_data)

if __name__ == '__main__':
    run()

