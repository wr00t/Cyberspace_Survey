import exifread
import json
from config import settings
from common.search import Search
import hashlib
from config.log import logger


class FILEINFO(Search):
    def __init__(self):
        Search.__init__(self)
        self.source = 'FILEINFO'
        self.module = 'TOOLS'
        self.search_data = []
        self.usage = settings.file_usage
        self.seach_data = []

    def calculate_hex(self, file_content):
        file_hex = ''
        i = 0
        while i < len(file_content):
            tmp = file_content[i]
            i += 1
            if tmp <= 15:
                file_hex += '0' + hex(tmp)[2:]
            else:
                file_hex += hex(tmp)

            file_hex = file_hex.replace('0x', '')
        return file_hex

    def file_info(self, targets):
        with open(targets, 'rb') as file:
            file_content = file.read()
            file_md5 = hashlib.md5(file_content).hexdigest()
            file_sha1 = hashlib.sha1(file_content).hexdigest()
            file_sha256 = hashlib.sha256(file_content).hexdigest()
            file_sha512 = hashlib.sha512(file_content).hexdigest()
            file_hex = self.calculate_hex(file_content)

            file_info = {'md5': file_md5, 'sha1': file_sha1, 'sha256': file_sha256, 'sha512': file_sha512, 'hex': file_hex}
        self.search_data.append(file_info)

    def run(self, targets):
        print(self.usage)
        self.begin()
        for i in targets:
            FILEINFO.file_info(self, i)
        print(json.dumps(self.search_data, sort_keys=False, indent=4))
        self.finish()
        return json.dumps(self.search_data, ensure_ascii=False)

def run(targets):
    search = FILEINFO()
    search_data = search.run(targets)
    return json.dumps(search_data)

if __name__ == '__main__':
    run(['1.jpg'])






