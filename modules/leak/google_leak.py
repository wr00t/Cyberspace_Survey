import json
import urllib.parse
from common.search import Search
from googlesearch import search
from config import settings
from config.log import logger


class GoogleLeak(Search):
    def __init__(self):
        Search.__init__(self)
        self.module = 'Leak'
        self.source = 'GoogleLeak'
        self.init = 'https://www.google.com/'
        self.addr = 'https://www.google.com/search'
        self.usage = settings.google_leak_usage
        self.search_data = []

    def search(self, targets):
        self.header = self.get_header()
        self.header.update({'User-Agent': 'Googlebot',
                            'Referer': 'https://www.google.com'})
        self.proxy = self.get_proxy(self.source)
        leak_file = "site:%s AND ext:xml |ext:conf |ext:cnf |ext:reg |ext:inf |ext:rdp |ext:cfg |ext:txt |ext:ora |ext:ini |ext:sql |ext:dbf |ext:mdb |ext:log |ext:bkf |ext:bkp |ext:bak |ext:old |ext:backup |ext:doc |ext:docx |ext:odt |ext:pdf |ext:rtf |ext:sxw |ext:psw |ext:ppt |ext:pptx |ext:pps |ext:csv |ext:php |inurl:id" % targets
        directory_traversal = "site:%s AND intitle:index.of | inurl:/.svn/entries | inurl:/.git | inurl:/.DS_Store | inurl:/phpMyAdmin | inurl:/applicationintitle:phpinfo |inurl:pass |inurl:key |inurl:rsa" % targets
        tmp = {'leak_file': [], 'directory_traversal': []}
        try:
            for i in search(leak_file, tld='com', lang='en', start=0, stop=None, pause=10.0):
                tmp['leak_file'].append(urllib.parse.unquote(i))
            for i in search(directory_traversal, tld='com', lang='en', start=0, stop=None, pause=10.0):
                tmp['directory_traversal'].append(urllib.parse.unquote(i))
            if tmp.values():
                self.search_data.append(tmp)
            else:
                logger.log('INFOR', 'Google Leak Not FOUND')
        except Exception as e:
            logger.log('ERROR', e)
        return self.search_data

    def run(self, targets):
        print(self.usage)
        self.begin()
        for i in targets:
            GoogleLeak.search(self, i)
        self.finish()
        print(json.dumps(self.search_data, sort_keys=False, indent=4))
        return json.dumps(self.search_data, ensure_ascii=False)

def run(targets):
    search = GoogleLeak()
    search_data = search.run(targets)
    return search_data

if __name__ == '__main__':
    run(['dnslog.cn'])


