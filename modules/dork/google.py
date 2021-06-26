import json
import random
import time
from common.search import Search
from googlesearch import search
from config import settings


class Google(Search):
    def __init__(self):
        Search.__init__(self)
        self.module = 'Search'
        self.source = 'GoogleSearch'
        self.init = 'https://www.google.com/'
        self.addr = 'https://www.google.com/search'
        self.usage = settings.google_usage
        self.search_data = []

    def search(self,):
        self.header = self.get_header()
        self.header.update({'User-Agent': 'Googlebot',
                            'Referer': 'https://www.google.com'})
        # self.proxy = self.get_proxy(self.source)
        # resp = self.get(self.init)
        # if not resp:
        #     return
        # self.cookie = resp.cookies
        # self.delay = random.randint(1, 5)
        # time.sleep(self.delay)
        self.proxy = self.get_proxy(self.source)
        google_dork = input('请输入google dork: ')
        """
        query：我们要搜索的查询字符串。
        tld： tld代表顶级域名，这意味着我们要在google.com或google.in或其他某个域名上搜索结果。
        lang： lang代表语言。
        num：我们想要的结果数。
        start：要检索的第一个结果。
        stop：要检索的最后结果。使用“无”可永久搜索。
        pause：间隔以等待HTTP请求之间的时间。时间间隔太短可能会导致Google阻止您的IP。保持较大的延迟将使您的程序变慢，但它是安全且更好的选择。
        返回值：生成器（迭代器）产生找到的URL。如果stop参数为None，则迭代器将永远循环
        """
        for i in search(google_dork, tld='com', lang='en', start=0, stop=None, pause=5):
            self.search_data.append(i)


    def run(self):
        """
        类执行入口
        """
        print(self.usage)
        self.begin()
        Google.search(self)
        print(json.dumps(self.search_data, sort_keys=False, indent=4))
        self.finish()
        return json.dumps(self.search_data, ensure_ascii=False)

def run():
    """
    类统一调用入口

    """
    search = Google()
    search_data = search.run()
    return search_data


if __name__ == '__main__':
    run()
