import fire
from common import utils
from common import module
from config.banner import script_banner
import modules.dork.fofa_api as fofa_search
import modules.dork.shodan_api as shodan_search
import modules.dork.google as google_search
import modules.dork.github_api as github_search
import modules.personal.hunter_search_api as hunter_search
import modules.personal.hunter_verify_api as hunter_verify
import modules.personal.iknowwhatyoudownload_find as download_find
import modules.personal.github_email_api as github_email
import modules.leak.google_leak as google_leak
import modules.leak.endpoint_search as internet_endpoint
import modules.ti.ti_inquest as ti_inquest
import modules.ti.ti_alienvault as ti_alienvault
import modules.tools.tools_ico as tools_ico
import modules.tools.tools_cert as tools_cert
import modules.tools.tools_exif as tools_exif
import modules.tools.tools_file as tools_file
import modules.tools.tools_str2hex as str2hex


class Cyberspace_Survey(object):
    """
    Cyberspace_Survey 帮助信息

    Cyberspace_Survey usages

    Cyberspace_Survey is a powerful OSINT tool

    Example:
        dork 模块
        python3 Cyberspace_Survey.py dork --plateform google --output google.txt
        python3 Cyberspace_Survey.py dork --plateform fofa --output fofa.txt
        python3 Cyberspace_Survey.py dork --plateform shodan --output shodan.txt
        python3 Cyberspace_Survey.py dork --plateform github --output github.txt

        personal 模块
        python3 Cyberspace_Survey.py personal --plateform hunter_search --target bytedance.com --output hunter.txt
        python3 Cyberspace_Survey.py personal --plateform hunter_verify --target xx@bytedance.com --output hunter.txt
        python3 Cyberspace_Survey.py personal --plateform download_find  --target 111.111.111.111 --output download.txt
        python3 Cyberspace_Survey.py personal --plateform github_email --target github_id --output github_email.txt

        ti 模块
        python3 Cyberspace_Survey.py ti --plateform inquest --target ['xred.mooo.com','f481819cc864d272b4a2dc7eed506adc'] --output inquest.txt
        python3 Cyberspace_Survey.py ti --plateform otx --target ['xred.mooo.com','f481819cc864d272b4a2dc7eed506adc'] --output otx.txt

        leak 模块
        python3 Cyberspace_Survey.py leak --plateform internet_endpoint --target baidu.com --output endpoint.txt
        python3 Cyberspace_Survey.py leak --plateform google_leak --target baidu.com --output google_leak.txt

        tools 模块
        python3 Cyberspace_Survey.py tools --plateform ico --target https://www.baidu.com/favicon.ico --output ico.txt
        python3 Cyberspace_Survey.py tools --plateform cert --target baidu.com --output cert.txt
        python3 Cyberspace_Survey.py tools --plateform exif --target 1.jpg --output cert.txt
        python3 Cyberspace_Survey.py tools --plateform file --target hex_data.bin --output hex.txt
        python3 Cyberspace_Survey.py tools --plateform str2hex --target 1.1.1.1 --output str2hex.txt

    Note:
        mode=personal   查询个人信息(hunter/github)
            --plateform=github_email      查询最近的仓库活动账户的 email
            --plateform=hunter_search     查询公司邮箱是否在互联网泄露
            --plateform=hunter_verify     查询个人的公司邮箱是否存在
            --plateform=download_find     查询 ip 所下载的种子文件
        mode=leak   查询泄露信息(fofa/google/shodan/github)
            --plateform=google_leak         通过谷歌语法查询在互联网上泄露的文件
            --plateform=internat_endpoint   查询互联网上泄露的端点,如废弃的 js,html,主要调用了 github api,commoncrawl,wayback machine
        mode=dork   查询(fofa/shodan/google dork)
            --plateform=google
            --plateform=fofa
            --plateform=shodan
            --plateform=github
        mode=ti             查询威胁情报(otx/alienvault)
            --plateform inquest             inquest 威胁情报
            --plateform otx                 alienvault 威胁情报
            --plateform all                 结合上面情报源
        mode=tools          小工具
            --plateform ico                 ico 转化 hash
            --plateform cert                解析证书
            --plateform exif                图片信息
            --plateform file                文件信息
            --plateform str2hex             字符串16进制相互转化

    :param str  target      根据不同模块选择输入 域名/user id/user email/
    :param str  targets     根据不同模块选择输入文件名,文件包含上述内容,一行一个
    :param str  plateform   根据选择的模块不同,调用的 plateform 也不同,例如 shodan fofa hunter...
    :param str  output      选择是否需要保存路径
    :param bool personal:   Use personal module (default True)
    :param bool dork:       Use dork module (default True)
    :param bool tools:      Use tools module (default True)
    :param bool ti:         Use ti module (default True)
    """

    def __init__(self, target=None, targets=None, plateform=None, output=None):
        self.target = target
        self.targets = targets
        self.plateform = plateform
        self.output = output

    def personal(self):
        self.deal_targets_result = utils.get_targets(self.target, self.targets)
        if self.plateform == 'hunter_search':
            search_data = hunter_search.run(self.deal_targets_result)
        elif self.plateform == 'hunter_verify':
            search_data = hunter_verify.run(self.deal_targets_result)
        elif self.plateform == 'github_email':
            search_data = github_email.run(self.deal_targets_result)
        elif self.plateform == 'download_find':
            search_data = download_find.run(self.deal_targets_result)
        if self.output and search_data:
            module.Module.save_json(self, search_data)

    def leak(self):
        self.deal_targets_result = utils.get_targets(self.target, self.targets)
        if self.plateform == 'google_leak':
            search_data = google_leak.run(self.deal_targets_result)
        elif self.plateform == 'internet_endpoint':
            search_data = internet_endpoint.run(self.deal_targets_result)
        if self.output and search_data:
            module.Module.save_json(self, search_data)

    def dork(self):
        if self.plateform and self.plateform == 'fofa':
            search_data = fofa_search.run()
            if self.output:
                fofa_search.Fofa.save_json(self, search_data)
        elif self.plateform and self.plateform == 'shodan':
            search_data = shodan_search.run()
            if self.output:
                shodan_search.ShodanAPI.save_json(self, search_data)
        elif self.plateform and self.plateform == 'google':
            search_data = google_search.run()
        elif self.plateform and self.plateform == 'github':
            search_data = github_search.run()
        if self.output:
            module.Module.save_json(self, search_data)

    def ti(self):
        self.deal_targets_result = utils.get_targets(self.target, self.targets)
        if self.plateform and self.plateform == 'inquest':
            search_data = ti_inquest.run(self.deal_targets_result)
        if self.plateform and self.plateform == 'otx':
            search_data = ti_alienvault.run(self.deal_targets_result)
        if self.plateform and self.plateform == 'all':
            search_data = []
            search_data.append(ti_alienvault.run(self.deal_targets_result))
            search_data.append(ti_inquest.run(self.deal_targets_result))
        if self.output:
            module.Module.save_json(self, search_data)

    def tools(self):
        self.deal_targets_result = utils.get_targets(self.target, self.targets)
        if self.plateform and self.plateform == 'ico':
            search_data = tools_ico.run(self.deal_targets_result)
        if self.plateform and self.plateform == 'cert':
            search_data = tools_cert.run(self.deal_targets_result)
        if self.plateform and self.plateform == 'exif':
            search_data = tools_exif.run(self.deal_targets_result)
        if self.plateform and self.plateform == 'file':
            search_data = tools_file.run(self.deal_targets_result)
        if self.plateform and self.plateform == 'str2hex':
            search_data = str2hex.run(self.deal_targets_result)
        if self.output:
            module.Module.save_json(self, search_data)

    @staticmethod
    def version():
        """
        Print version information and exit
        """
        print(script_banner())
        exit(0)

if __name__ == '__main__':
    fire.Fire(Cyberspace_Survey)