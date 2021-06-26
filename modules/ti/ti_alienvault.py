import json
import tldextract
from config import settings
from common.search import Search
import colorama
from config.log import logger
from OTXv2 import OTXv2
from OTXv2 import IndicatorTypes


class ALIENVAULTOTX(Search):
    def __init__(self):
        Search.__init__(self)
        self.source = 'AlienVaultOTX'
        self.module = 'TI'
        self.proxy = self.get_proxy(self.source)
        self.search_data = []
        self.url = 'https://otx.alienvault.com/'
        self.key = settings.otx_api_key
        self.otx = OTXv2(self.url, self.key)
        self.alerts = []
        self.outfile_dic = {}
        self.usage = settings.ti_otx_usage

    def search(self, targets):
        ip_list, domain_list, file_list, url_list, email_list = self.deal_ti_targets(targets)
        if ip_list:
            for i in ip_list:
                self.detect_ip(i)
                self.check_alerts(i)
        if domain_list:
            for i in domain_list:
                self.detect_domain(i)
                self.check_alerts(i)
        if file_list:
            for i in file_list:
                self.detect_file(i)
                self.check_alerts(i)

    @staticmethod
    def getValue(results, keys):
        if type(keys) is list and len(keys) > 0:

            if type(results) is dict:
                key = keys.pop(0)
                if key in results:
                    return ALIENVAULTOTX.getValue(results[key], keys)
                else:
                    return None
            else:
                if type(results) is list and len(results) > 0:
                    return ALIENVAULTOTX.getValue(results[0], keys)
                else:
                    return results
        else:
            return results

    def detect_ip(self, ip):
        try:
            result = self.otx.get_indicator_details_by_section(IndicatorTypes.IPv4, ip, 'general')
            validation = self.getValue(result, ['validation'])

            if not validation:
                pulses = self.getValue(result, ['pulse_info', 'pulses'])
                if pulses:
                    for pulse in pulses:
                        if 'name' in pulse:
                            self.alerts.append('In pulse: ' + pulse['name'])
        except Exception as e:
            logger.log('ERROR', e)

    def detect_domain(self, hostname):
        domain = tldextract.extract(hostname).domain + '.' + tldextract.extract(hostname).suffix
        if hostname != domain:
            result = self.otx.get_indicator_details_by_section(IndicatorTypes.HOSTNAME, hostname, 'general')

            validation = self.getValue(result, ['validation'])
            if not validation:
                pulses = self.getValue(result, ['pulse_info', 'pulses'])
                if pulses:
                    for pulse in pulses:
                        if 'name' in pulse:
                            self.alerts.append('In pulse: ' + pulse['name'])
        else:
            result = self.otx.get_indicator_details_by_section(
                IndicatorTypes.DOMAIN, domain, 'general')

            validation = self.getValue(result, ['validation'])
            if not validation:
                pulses = self.getValue(result, ['pulse_info', 'pulses'])
                if pulses:
                    for pulse in pulses:
                        if 'name' in pulse:
                            self.alerts.append('In pulse: ' + pulse['name'])

    def detect_file(self, file_hash):
        if len(file_hash) == 32:
            file_hash_type = IndicatorTypes.FILE_HASH_MD5
        elif len(file_hash) == 40:
            file_hash_type = IndicatorTypes.FILE_HASH_SHA1
        elif len(file_hash) == 64:
            file_hash_type = IndicatorTypes.FILE_HASH_SHA256
        else:
            return

        try:
            result = self.otx.get_indicator_details_by_section(file_hash_type, file_hash, 'general')
            validation = self.getValue(result, ['validation'])

            if not validation:
                pulses = self.getValue(result, ['pulse_info', 'pulses'])
                if pulses:
                    for pulse in pulses:
                        if 'name' in pulse:
                            self.alerts.append('In pulse: ' + pulse['name'])
        except Exception as e:
            logger.log('ERROR', e)


    def check_alerts(self, target):
        if len(self.alerts) > 0:
            print(colorama.Fore.RED + '{} 被识别为潜在恶意'.format(target) + colorama.Style.RESET_ALL)
        else:
            print('{} 未知或非恶意'.format(target))

        # 将IP威胁事件格式化为字典形式
        entity_dic = {}
        # alerts_dic = {}
        alerts_lst = []

        idx = 1
        for item in self.alerts:
            key = 'pulse' + str(idx)
            value = item.split(':')[1].strip()
            # alerts_dic[key] = value
            alerts_lst.append(value)
            idx += 1
        #
        entity_dic['target'] = target
        entity_dic['pulses'] = alerts_lst
        entity_dic['pulses_total'] = len(alerts_lst)
        self.alerts = []
        if entity_dic['pulses']:
            self.search_data.append(entity_dic)

    def run(self, targets):
        print(self.usage)
        if not self.have_api(self.key):
            return
        self.begin()
        ALIENVAULTOTX.search(self, targets)
        print(json.dumps(self.search_data, sort_keys=False, indent=4))
        self.finish()
        return json.dumps(self.search_data, ensure_ascii=False)

def run(targets):
    search = ALIENVAULTOTX()
    search_data = search.run(targets)
    return json.dumps(search_data)

if __name__ == '__main__':
    run(['f590e1b6a80cf3e8360388382eabb04b3e247b78'])
