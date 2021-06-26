import json
import pathlib
import time
import requests
from multiprocessing.dummy import Pool
from config import settings
from common.search import Search
import colorama
from config.log import logger


class Inquest(Search):
    def __init__(self):
        Search.__init__(self)
        self.source = 'InquestAPI'
        self.inquest_url = "https://labs.inquest.net/api/"
        self.module = 'TI'
        self.proxy = self.get_proxy(self.source)
        self.search_data = []
        self.alerts = []
        self.usage = settings.ti_inquest_usage
        self.session = requests.Session()
        self.inquest_dfi_url = self.inquest_url + 'dfi/search/'
        self.inquest_compromise_url = self.inquest_url + 'iocdb/'
        self.time = time.time()

    def inquests_keyword_search(self, internat_url):
        response = self.session.get(self.inquest_compromise_url + 'search?keyword=%s' % internat_url, timeout=(5, 10)).json()
        if response['data']:
            self.alerts.append(colorama.Fore.RED + '{} 被识别为潜在恶意'.format(internat_url) + colorama.Style.RESET_ALL)
            self.search_data.append(response)
        else:
            self.alerts.append('{} 未知或非恶意'.format(internat_url))

    def inquests_file_search(self, file):
        if len(file) == 32:
            response = self.session.get(self.inquest_dfi_url + 'hash/md5?hash=%s' % file).json()
        elif len(file) == 40:
            response = self.session.get(self.inquest_dfi_url + 'hash/sha1?hash=%s' % file).json()
        elif len(file) == 64:
            response = self.session.get(self.inquest_dfi_url + 'hash/sha256?hsah=%s' % file).json()
        elif len(file) == 128:
            response = self.session.get(self.inquest_dfi_url + 'hash/sha512?hsah=%s' % file).json()
        if response['data']:
            self.search_data.append(response)
            self.alerts.append(colorama.Fore.RED + '{} 被识别为潜在恶意'.format(file) + colorama.Style.RESET_ALL)
        else:
            self.alerts.append('{} 未知或非恶意'.format(file))

    def inquests_email_search(self, email):
        response = self.session.get(self.inquest_dfi_url + 'ioc/email?keyword=%s' % email).json()
        if response['data']:
            self.alerts.append(colorama.Fore.RED + '{} 被识别为潜在恶意'.format(email) + colorama.Style.RESET_ALL)
            self.search_data.append(response)
        else:
            self.alerts.append('{} 未知或非恶意'.format(email))

    def search(self, targets):
        self.session.headers = self.get_header()
        self.session.proxies = self.get_proxy(self.source)
        self.session.verify = self.verify
        self.session.headers.update({'content-type': 'application/json'})
        ip_list, domain_list, file_list, url_list, email_list = self.deal_ti_targets(targets)
        internat_list = ip_list + domain_list + url_list
        try:
            pool = Pool(30)
            if file_list:
                pool.map(self.inquests_file_search, file_list)
            if internat_list:
                pool.map(self.inquests_keyword_search, internat_list)
            if email_list:
                pool.map(self.inquests_email_search, email_list)
            pool.close()
            pool.join()

        except Exception as e:
            logger.log('ERROR', e)

    def run(self, targets):
        print(self.usage)
        self.begin()
        Inquest.search(self, targets)
        print(json.dumps(self.search_data, sort_keys=False, indent=4, ensure_ascii=False))
        for i in self.alerts:
            print(i)
        self.finish()
        return json.dumps(self.search_data, ensure_ascii=False)

def run(targets):
    search = Inquest()
    search_data = search.run(targets)
    return search_data

if __name__ == '__main__':
    run(['http://www.sbmc-card.in/confirm/landing.html'])



