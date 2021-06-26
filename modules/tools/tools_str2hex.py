import struct
import json
from config import settings
from common.search import Search
import binascii
import socket
from config.log import logger


class STR2HEX(Search):
    def __init__(self):
        Search.__init__(self)
        self.source = 'STR2HEX'
        self.module = 'TOOLS'
        self.search_data = []
        self.usage = settings.str2hex_usage

    def ip2int(self, addr):
        return struct.unpack("!I", socket.inet_aton(addr))[0]

    def str2hex(self, targets):
        bytes_list, hex_list, ip_list = self.judge_hex(targets)
        try:
            if bytes_list:
                for i in bytes_list:
                    string_content = i.decode('utf-8')
                    hex_content = binascii.b2a_hex(i).decode('utf-8')
                    content_info = {'string_content': string_content, 'hex_content': hex_content}
                    self.search_data.append(content_info)
            if hex_list:
                for i in hex_list:
                    string_content = binascii.a2b_hex(i).decode('unicode-escape')
                    hex_content = i
                    content_info = {'string_content': string_content, 'hex_content': hex_content}
                    self.search_data.append(content_info)
            if ip_list:
                for i in ip_list:
                    string_content = i
                    hex_content = self.ip2int(i)
                    content_info = {'string_content': string_content, 'hex_content': hex_content}
                    self.search_data.append(content_info)
        except Exception as e:
            logger.log('ERROR', e)


    def run(self, targets):
        print(self.usage)
        self.begin()
        STR2HEX.str2hex(self, targets)
        print(json.dumps(self.search_data, sort_keys=False, indent=4))
        self.finish()
        return json.dumps(self.search_data, ensure_ascii=False)

def run(targets):
    search = STR2HEX()
    search_data = search.run(targets)
    return json.dumps(search_data)

if __name__ == '__main__':
    run(['218.201.28.150', '3231382e3230312e32382e313530'])






