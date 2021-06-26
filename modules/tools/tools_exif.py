import exifread
import json
from config import settings
from common.search import Search
import requests
from config.log import logger


class PHOTOEXIF(Search):
    def __init__(self):
        Search.__init__(self)
        self.source = 'EXIF'
        self.module = 'TOOLS'
        self.key = settings.baidumap_api_key
        self.url = 'http://api.map.baidu.com/'
        self.search_data = []
        self.usage = settings.baidumap_usage

    def get_photo_info(self, photo_file):
        try:
            with open(photo_file, 'rb') as f:
                tags = exifread.process_file(f)
            if tags and 'GPS GPSLatitudeRef' in tags:
                # 纬度
                lat_ref = tags["GPS GPSLatitudeRef"].printable
                lat = tags["GPS GPSLatitude"].printable[1:-1].replace(" ", "").replace("/", ",").split(",")
                lat = float(lat[0]) + float(lat[1]) / 60 + float(lat[2]) / float(lat[3]) / 3600
                if lat_ref != "N":
                    lat = lat * (-1)
                # 经度
                lon_ref = tags["GPS GPSLongitudeRef"].printable
                lon = tags["GPS GPSLongitude"].printable[1:-1].replace(" ", "").replace("/", ",").split(",")
                lon = float(lon[0]) + float(lon[1]) / 60 + float(lon[2]) / float(lon[3]) / 3600
                if lon_ref != "E":
                    lon = lon * (-1)
                location = self.get_location(lat, lon)
                if not location:
                    location = 'NOT FOUND'
                tmp = {'拍摄时间：': str(tags['EXIF DateTimeOriginal']), '照相机制造商：': str(tags['Image Make']),
                       '照相机型号：': str(tags['Image Model']), '照片尺寸': (str(tags['EXIF ExifImageWidth']), str(tags['EXIF ExifImageLength'])),
                       '经纬度': (str(lat), str(lon)), '详细地址': location}
                self.search_data.append(tmp)
        except Exception as e:
            logger.log('ERROR', e)

    def get_location(self, lat, lon):
        headers = self.get_header()
        url = self.url + 'reverse_geocoding/v3/?ak={}&output=json' \
              '&coordtype=wgs84ll&location={},{}'.format(self.key, lat, lon)
        response = requests.get(url, headers=headers, timeout=(5, 10)).json()
        status = response['status']
        if status == 0:
            address = response['result']['formatted_address']
        return address


    def run(self, targets):
        print(self.usage)
        self.begin()
        for i in targets:
            PHOTOEXIF.get_photo_info(self, i)
        self.finish()
        print(json.dumps(self.search_data, sort_keys=False, indent=4, ensure_ascii=False))
        return json.dumps(self.search_data, ensure_ascii=False)

def run(targets):
    search = PHOTOEXIF()
    search_data = search.run(targets)
    return search_data

if __name__ == '__main__':
    run(['im2.jpg'])


