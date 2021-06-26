import re
import time
import urllib
import requests
import tldextract
from bs4 import BeautifulSoup
from config import settings
from config.log import logger
from common import utils
import urllib3
urllib3.disable_warnings()
from urllib.parse import urlparse


class Module(object):
    def __init__(self):
        self.cookie = None
        self.header = dict()
        self.proxy = None
        self.delay = 1  # 请求睡眠时延
        self.timeout = settings.request_timeout_second  # 请求超时时间
        self.verify = settings.request_ssl_verify  # 请求SSL验证
        self.results = list()  # 存放模块结果
        self.start = time.time()  # 模块开始执行时间
        self.end = None  # 模块结束执行时间
        self.elapse = None  # 模块执行耗时
        self.session = requests.Session()

    def save_json(self, search_data):
        logger.log('TRACE', f'Save the dork results found by '
                            f'{self.output} module as a json file')
        path = settings.result_save_dir
        # path = settings.result_save_dir.joinpath(filename)
        # path.mkdir(parents=True, exist_ok=True)
        filename = path.joinpath(self.output)
        if search_data:
            with open(filename, 'a+') as file:
                file.write(search_data)

    def deleteDuplicate(self, results_list_dict):
        seen = set()
        new_l = []
        for i in results_list_dict:
            t = tuple(i.items())
            if t not in seen:
                seen.add(t)
                new_l.append(i)
        return new_l

    def deal_target(self, targets):
        deal_target_results = []
        if type(targets) == str:
            deal_target_results.append(targets)
        elif type(targets) == list:
            deal_target_results = targets
        return deal_target_results

    def have_api(self, *apis):
        """
        Simply check whether the api information configure or not

        :param  apis: apis set
        :return bool: check result
        """
        if not all(apis):
            logger.log('DEBUG', f'{self.source} module is not configured')
            return False
        return True

    def get_header(self):
        """
        Get request header

        :return: header
        """
        headers = utils.gen_fake_header()
        if isinstance(headers, dict):
            self.header = headers
            return headers
        return self.header

    def get_proxy(self, module):
        """
        Get proxy

        :param str module: module name
        :return: proxy
        """
        if not settings.enable_request_proxy:
            logger.log('TRACE', f'All modules do not use proxy')
            return self.proxy
        if settings.proxy_all_module:
            logger.log('TRACE', f'{module} module uses proxy')
            return utils.get_random_proxy()
        else:
            logger.log('TRACE', f'{module} module does not use proxy')
            return self.proxy

    def get(self, url, params=None, check=True, ignore=False, raise_error=False, **kwargs):
        """
        Custom get request

        :param str  url: request url
        :param dict params: request parameters
        :param bool check: check response
        :param bool ignore: ignore error
        :param bool raise_error: raise error or not
        :param kwargs: other params
        :return: response object
        """
        session = requests.Session()
        session.trust_env = False
        level = 'ERROR'
        if ignore:
            level = 'DEBUG'
        try:
            resp = session.get(url,
                               params=params,
                               cookies=self.cookie,
                               headers=self.header,
                               proxies=self.proxy,
                               timeout=self.timeout,
                               verify=self.verify,
                               **kwargs)
        except Exception as e:
            if raise_error:
                if isinstance(e, requests.exceptions.ConnectTimeout):
                    logger.log(level, e.args[0])
                    raise e
            logger.log(level, e.args[0])
            return None
        if not check:
            return resp
        if utils.check_response('GET', resp):
            return resp
        return None

    def calculate_page(self, total_count):
        if total_count % 100 != 0:
            max_page = int(total_count / 100) + 1
        else:
            max_page = int(total_count / 100)
        return max_page

    def getRawUrl(self, result):
        raw_url = result['html_url'];
        raw_url = raw_url.replace('https://github.com/', 'https://raw.githubusercontent.com/')
        raw_url = raw_url.replace('/blob/', '/')
        return raw_url;

    def doGetCode(self, url):
        try:
            r = requests.get(url, timeout=5)
        except Exception as e:
            logger.log(e)
            return False

        return r.text

    def begin(self):
        """
        begin log
        """
        logger.log('DEBUG', f'Start Cyberspace_Survey {self.source} module')
        time.sleep(0.01)

    def finish(self):
        """
        finish log
        """
        self.end = time.time()
        self.elapse = round(self.end - self.start, 1)
        logger.log('DEBUG', f'Finished {self.source} module')
        logger.log('INFOR', f'{self.source} module took {self.elapse} seconds')
        logger.log('DEBUG', f'{self.source} module found {self.search_data}')

    def auth_github(self, github_url_api):
        """
        github api 认证

        :return: 认证失败返回False 成功返回True
        """
        self.session.headers = self.get_header()
        self.session.proxies = self.get_proxy(self.source)
        self.session.verify = self.verify
        self.session.headers.update(
            {'Accept': 'application/vnd.github.v3.text-match+json'})
        self.session.headers.update({'Authorization': 'token ' + self.token})
        try:
            resp = self.session.get(github_url_api)
        except Exception as e:
            logger.log('ERROR', e.args)
            return False
        if resp.status_code != 200:
            resp_json = resp.json()
            msg = resp_json.get('message')
            logger.log('ERROR', msg)
            return False
        else:
            logger.log('INFOR', f'Github Authorization SUCCESS')
        del self.session.headers['Authorization']
        return True

    def deal_ti_targets(self, targets):
        ip_list = []
        domain_list = []
        file_list = []
        url_list = []
        email_list = []
        pattern = re.compile(r'((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}')
        for i in targets:
            i = i.strip().lower()
            tmp = pattern.search(i)
            domain = tldextract.extract(i).fqdn
            if 'http' in i:
                url_list.append(i)
            elif '@' in i:
                email_list.append(i)
            elif tmp:
                ip_list.append(tmp.group(0))
            elif (len(i) == 32 or len(i) == 40 or len(i) == 64 or len(i) == 128) and '.' not in i:
                file_list.append(i)
            if domain:
                domain_list.append(domain)
        return ip_list, domain_list, file_list, url_list, email_list

    def judge_hex(self, targets):
        bytes_list = []
        hex_list = []
        ip_list = []
        pattern = re.compile(r'((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}')
        for i in targets:
            if isinstance(i, bytes):
                bytes_list.append(i)
            if isinstance(i, str):
                tmp = pattern.search(i)
                if tmp:
                    ip_list.append(tmp.group(0))
                else:
                    hex_list.append(i)
        return bytes_list, hex_list, ip_list


