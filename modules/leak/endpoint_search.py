import json
import time
import random
from urllib.parse import urlparse
import tldextract
from common.search import Search
from functools import partial
from multiprocessing.dummy import Pool
from config import settings
from config.log import logger
import requests
import re

MIN_LENGTH = 5
_url_chars = '[a-zA-Z0-9\-\.\?\#\$&@%=_:/\]\[]'
_not_url_chars = '[^a-zA-Z0-9\-\.\?\#\$&@%=_:/\]\[]'
t_endpoints = []
t_exclude = [
    r'^http://$',
    r'^https://$',
    r'^javascript:$',
    r'^tel:$',
    r'^mailto:$',
    r'^text/javascript$',
    r'^application/json$',
    r'^application/javascript$',
    r'^text/plain$',
    r'^text/html$',
    r'^text/x-python$',
    r'^text/css$',
    r'^image/png$',
    r'^image/jpeg$',
    r'^image/x-icon$',
    r'^img/favicon.ico$',
    r'^application/x-www-form-urlencoded$',
    r'/Users/[0-9a-zA-Z\-\_]/Desktop',
    r'www.w3.org',
    r'schemas.android.com',
    r'www.apple.com',
    # r'^#',
    # r'^\?',
    # r'^javascript:',
    # r'^mailto:',
]
t_regexp = [
    r'[\'"\(].*(http[s]?://' + _url_chars + '*?)[\'"\)]',
    r'[\'"\(](http[s]?://' + _url_chars + '+)',

    r'[\'"\(](' + _url_chars + '+\.sdirect' + _url_chars + '*)',
    r'[\'"\(](' + _url_chars + '+\.htm' + _url_chars + '*)',
    r'[\'"\(](' + _url_chars + '+\.php' + _url_chars + '*)',
    r'[\'"\(](' + _url_chars + '+\.asp' + _url_chars + '*)',
    r'[\'"\(](' + _url_chars + '+\.js' + _url_chars + '*)',
    r'[\'"\(](' + _url_chars + '+\.xml' + _url_chars + '*)',
    r'[\'"\(](' + _url_chars + '+\.ini' + _url_chars + '*)',
    r'[\'"\(](' + _url_chars + '+\.conf' + _url_chars + '*)',
    r'[\'"\(](' + _url_chars + '+\.cfm' + _url_chars + '*)',

    r'href\s*[.=]\s*[\'"](' + _url_chars + '+)',
    r'src\s*[.=]\s*[\'"](' + _url_chars + '+)',
    r'url\s*[:=]\s*[\'"](' + _url_chars + '+)',

    r'urlRoot\s*[:=]\s*[\'"](' + _url_chars + '+)',
    r'endpoint[s]\s*[:=]\s*[\'"](' + _url_chars + '+)',
    r'script[s]\s*[:=]\s*[\'"](' + _url_chars + '+)',

    r'\.ajax\s*\(\s*[\'"](' + _url_chars + '+)',
    r'\.get\s*\(\s*[\'"](' + _url_chars + '+)',
    r'\.post\s*\(\s*[\'"](' + _url_chars + '+)',
    r'\.load\s*\(\s*[\'"](' + _url_chars + '+)',

    ### a bit noisy
    # r'[\'"](' + _url_chars + '+/' + _url_chars + '+)?[\'"]',
    # r'content\s*[.=]\s*[\'"]('+_url_chars+'+)',
]
class EndpointSearch(Search):
    def __init__(self):
        Search.__init__(self)
        self.module = 'Leak'
        self.source = 'EndpointSearch'
        self.usage = settings.endpoint_search_usage
        self.session = requests.Session()
        self.proxy = self.get_proxy(self.source)
        self.token = random.choice(settings.github_token_list)
        self.search_data = []
        self.commoncrawl_url = 'https://index.commoncrawl.org/' + settings.commoncrawl_search_page
        self.wayback_detail_url = 'https://web.archive.org/cdx/search/cdx/search/cds'
        self.wayback_check_url = 'https://archive.org/wayback/available'
        self.github_url_api = 'https://api.github.com/'
        self.github_endpoint_list = set()
        self.commoncrawl_result_list = []
        self.wayback_result_list = set()
        self.raw_html_urls = []

    def get_endpoint(self, targets, items):
        raw_html_url = self.getRawUrl(items)
        time.sleep(random.random())
        if raw_html_url in self.raw_html_urls:
            return
        self.raw_html_urls.append(raw_html_url)
        code = self.doGetCode(raw_html_url)
        regexp = r'((([0-9a-z_\-\.]+)\.)?' + targets.replace('.', '\.') + ')'
        if code:
            matches = re.findall(regexp, code, re.IGNORECASE)
            if matches:
                # 添加来源
                self.github_endpoint_list.add((matches[0][0], items['html_url']))
                for r in t_regexp:
                    edpt = re.findall(r, code, re.IGNORECASE)
                    if edpt:
                        for endpoint in edpt:
                            endpoint = endpoint.strip()
                            if len(endpoint) >= MIN_LENGTH:
                                goodbye = False
                                for exclude in t_exclude:
                                    if re.match(exclude, endpoint):
                                        goodbye = True
                                        break
                                if goodbye:
                                    continue
                                if endpoint.startswith('http'):
                                    domain = tldextract.extract(endpoint).fqdn
                                    sss = re.match(regexp, domain)
                                    if not sss:
                                        continue
                                    self.github_endpoint_list.add(endpoint)

    def github_endpoint(self, targets):
        headers = {'Authorization': 'token ' + self.token}
        time.sleep(random.random())
        # https://docs.github.com/en/rest/reference/search
        """
        q           该查询包含一个或多个搜索关键字和限定词.限定词允许您将搜索限制在GitHub的特定区域.
        sort        对查询结果进行排序,只能是indexed，它表示GitHub搜索基础结构最近对文件建立索引的程度.
        order       确定返回的第一个搜索结果是最高匹配数（desc）还是最低匹配数（asc）。除非您提供，否则将忽略此参数sort。
        per_page    每页结果（最多100个）。
        page        要获取的结果的页码
        """
        # 首先查看域名在 github 是否存在,total_count 不为 0 则为存在，不填写 page 默认为第一页
        github_result = requests.get(self.github_url_api + 'search/code?per_page=100&s=indexed&type=Code&o=desc&q=%s' % targets, headers=headers).json()
        total_count = github_result['total_count']
        if not total_count:
            return
        pool = Pool(30)
        pool.map(partial(self.get_endpoint, targets), github_result['items'])
        pool.close()
        pool.join()
        # 对每一个 html_url 的原网页进行 get_endpoint(正则) self.github_endpoint_list 查看结果
        # self.get_endpoint(github_result, targets)
        page = self.calculate_page(total_count)
        # 数量超过 100 的情况
        if page > 1:
            for i in range(2, page + 1):
                github_result = requests.get(self.github_url_api + 'search/code?per_page=100&s=indexed&type=Code&o=desc&q=%s&page=%s' % (targets, str(i)), headers=headers, timeout=(5, 10)).json()
                # 对每一个 html_url 的原网页进行get_endpoint(正则)
                if 'items' in github_result:
                    pool = Pool(30)
                    pool.map(partial(self.get_endpoint, targets), github_result['items'])
                    pool.close()
                    pool.join()

        return True

    def search(self, targets):
        # github endpoint
        self.session.headers = self.get_header()
        self.session.proxies = self.get_proxy(self.source)
        self.session.verify = self.verify
        self.session.headers.update(
            {'Accept': 'application/vnd.github.v3.text-match+json'})
        try:
            if not self.github_endpoint(targets):
                logger.log('TRACE', f'{targets} Module:EndpointSearch github-endpoint failed')
        # 在 commoncrawl 查找域名为 *.t00ls.net 的所有爬取地址
            commoncrawl_result = requests.get(self.commoncrawl_url + '?url=*.%s&output=json' % targets, timeout=(5, 10)).text
            # if 'error' not in commoncrawl_result and 'No Captures found' not in commoncrawl_result:
            if 'No Captures found' not in commoncrawl_result:
                logger.log('INFOR', f'Common Crawl check success: %s' % (self.commoncrawl_url + '?url=*.%s&output=json' % targets))
                self.commoncrawl_result_list = re.findall(r'"url": "(.*?)"', commoncrawl_result, re.S)
                self.commoncrawl_result_list = list(set(self.commoncrawl_result_list))
            else:
                logger.log('TRACE', f'{targets} Module:EndpointSearch commoncrawl NOT FOUND')

            # https://github.com/internetarchive/wayback/tree/master/wayback-cdx-server wayback machine 接口
            wayback_check = json.loads(requests.get(self.wayback_check_url + '?url=%s' % targets).text)
            if wayback_check['archived_snapshots']:
                logger.log('INFOR', f'Wayback Machine check success: %s' % (self.wayback_check_url + '?url=%s' % targets), timeout=(5, 10))
                # 在 wayback 查找域名为 t00ls.net(包括子域名) 的所有网站快照
                wayback_result = requests.get(self.wayback_detail_url + '?url=%s/*&output=json&limit=1000' % targets).json()
                del wayback_result[0]
                for i in wayback_result:
                    if i[2] not in self.wayback_result_list:
                        self.wayback_result_list.add(i[2])
            else:
                logger.log('TRACE', f'{targets} Module:EndpointSearch wayback machine NOT FOUND')

        except Exception as e:
            logger.log('ERROR', e)


        tmp = {'commoncrawl': list(self.commoncrawl_result_list), 'wayback': list(self.wayback_result_list),
               'github-endpoint': list(self.github_endpoint_list)}
        if tmp.values():
            self.search_data.append(tmp)

    def run(self, targets):
        print(self.usage)
        self.begin()
        if not self.auth_github(self.github_url_api):
            return
        for i in targets:
            EndpointSearch.search(self, i)
        print(json.dumps(self.search_data, sort_keys=False, indent=4))
        self.finish()
        return json.dumps(self.search_data, ensure_ascii=False)

def run(targets):
    search = EndpointSearch()
    search_data = search.run(targets)
    return search_data

if __name__ == '__main__':
    run(['dnslog.cn'])






