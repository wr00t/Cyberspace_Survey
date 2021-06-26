import json
from config import settings
from common.search import Search
import shodan
from config.log import logger


class ShodanAPI(Search):
    def __init__(self):
        Search.__init__(self)
        self.module = 'Search'
        self.source = 'ShodanAPISearch'
        self.key = settings.shodan_api_key
        self.api = shodan.Shodan(self.key, proxies=self.proxy)
        self.usage = settings.shodan_usage
        self.search_data = []

    def search(self):
        self.header = self.get_header()
        self.proxy = self.get_proxy(self.source)
        try:
            shodan_dork = input('请输入dork: ')
            shodan_search_data = self.api.search(shodan_dork)
            shodan_info_results = self.api.info()
            matches_result = shodan_search_data['matches']
            for i in matches_result:
                if 'http' in i.keys():
                    tmp = {'hostnames': i['hostnames'], 'asn': i['asn'], 'ip': i['ip_str'], 'port': i['port'],
                           'title': i['http']['title'], 'html_hash': i['http']['html_hash']}
                else:
                    tmp = {'hostnames': i['hostnames'], 'asn': i['asn'], 'ip': i['ip_str'], 'port': i['port']}
                self.search_data.append(tmp)
            if self.search_data:
                print('一共检测出 %d 条数据,导出限制 100 条' % shodan_search_data['total'])
            else:
                print('shodan dork 没有获取到数据')
            # 查询信用不足5则发出警告
            # shodan_info_results = self.api.info()
            # if shodan_info_results['query_credits'] < 6: print('[ Info ] 查询信用剩余：%s' % str(shodan_info_results['query_credits']))
        except Exception as e:
            logger.log('ERROR', e)

    def run(self):
        """
        类执行入口
        """
        print(self.usage)
        self.begin()
        if not self.have_api(self.key):
            return
        ShodanAPI.search(self)
        print(json.dumps(self.search_data, sort_keys=False, indent=4))
        self.finish()
        return json.dumps(self.search_data, ensure_ascii=False)

def run():
    """
    类统一调用入口

    """
    search = ShodanAPI()
    search_data = search.run()
    return search_data


if __name__ == '__main__':
    run()
