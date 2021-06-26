import json
import tldextract
from dateutil import parser
from config import settings
from common.search import Search
from config.log import logger
import ssl
import OpenSSL


class CERT(Search):
    def __init__(self):
        Search.__init__(self)
        self.source = 'CERT'
        self.module = 'TOOLS'
        self.proxy = self.get_proxy(self.source)
        self.search_data = []
        self.usage = settings.tools_cert_usage
        self.cert = None

    def get_cert_from_endpoint(self, server, port):
        try:
            self.cert = ssl.get_server_certificate((server, port))  # 证书
        except Exception as e:
            logger.log('ERROR', e)
        if not self.cert:
            return

        result = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, self.cert)

        cert_version = result.get_version() + 1  # 证书版本
        cert_serial_number = hex(result.get_serial_number())  # 证书序列号
        cert_signature_algorithm = result.get_signature_algorithm().decode("UTF-8")  # 证书中使用的签名算法
        cert_has_expired = result.has_expired  # 证书是否已经过期
        cert_pubkey = OpenSSL.crypto.dump_publickey(OpenSSL.crypto.FILETYPE_PEM, result.get_pubkey()).decode(
            "utf-8")  # 证书公钥
        cert_pubkey_length = result.get_pubkey().bits()  # 公钥长度

        datetime_struct_before = parser.parse(result.get_notBefore().decode("UTF-8")).strftime('%Y-%m-%d %H:%M:%S')
        datetime_struct_after = parser.parse(result.get_notAfter().decode("UTF-8")).strftime('%Y-%m-%d %H:%M:%S')
        cert_expired_time = datetime_struct_before + ' - ' + datetime_struct_after

        subject = result.get_subject()  # 主体信息
        country_name = subject.C  # 国家
        state_province = subject.ST  # 省份
        locality_name = subject.L  # 市
        organization_name = subject.O  # 公司名称
        organizational_unit = subject.OU  # 组织单位
        common_name = subject.CN  # 通用名称
        issuer = result.get_issuer()
        issued_by = issuer.CN  # 颁发者
        tmp = {"cert": self.cert, "subject": str(subject), "issuer": str(issuer), "country_name": country_name,
               "subject_hash": subject.hash(),
                "issued_by": issued_by,
                "state_province": state_province, "locality_name": locality_name,
                "organization_name": organization_name,
                "organizational_unit": organizational_unit, "common_name": common_name,
                "cert_signature_algorithm": cert_signature_algorithm, "cert_version": cert_version,
                "cert_serial_number":
                    cert_serial_number, "cert_expired_time": cert_expired_time,
                "cert_pubkey_length": cert_pubkey_length}
        self.search_data.append(tmp)

    def search(self, targets):
        if 'http' in targets:
            targets = tldextract.extract(targets).fqdn
        if ':' in targets:
            server = targets.split(':')[0]
            port = targets.split(':')[1]
        else:
            server = targets
            port = 443
        self.get_cert_from_endpoint(server, port)

    def run(self, targets):
        print(self.usage)
        self.begin()
        for i in targets:
            CERT.search(self, i)
        print(json.dumps(self.search_data, sort_keys=False, indent=4))
        self.finish()
        return json.dumps(self.search_data, ensure_ascii=False)

def run(targets):
    search = CERT()
    search_data = search.run(targets)
    return json.dumps(search_data)

if __name__ == '__main__':
    run(['https://www.baidu.com/favicon.ico'])


