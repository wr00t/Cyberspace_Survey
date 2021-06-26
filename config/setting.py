import pathlib

# 路径设置
relative_directory = pathlib.Path(__file__).parent.parent  # 代码相对路径
data_storage_dir = relative_directory.joinpath('data')  # 数据存放目录
result_save_dir = relative_directory.joinpath('results')  # 结果保存目录

# 代理设置
enable_request_proxy = True  # 是否使用代理(全局开关)
proxy_all_module = True  # 代理所有模块
request_proxy_pool = [{'http': 'http://127.0.0.1:7890',}]  # 随机代理池

# 请求设置
request_thread_count = None  # 请求线程数量(默认None，则根据情况自动设置)
request_timeout_second = (13, 27)  # 请求超时秒数(默认connect timout推荐略大于3秒)
request_ssl_verify = False  # 请求SSL验证(默认False)
request_allow_redirect = True  # 请求允许重定向(默认True)
request_redirect_limit = 10  # 请求跳转限制(默认10次)
# 默认请求头 可以在headers里添加自定义请求头
request_default_headers = {
    'Accept': 'text/html,application/xhtml+xml,'
              'application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Cache-Control': 'max-age=0',
    'DNT': '1',
    'Referer': 'https://www.google.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
    'X-Forwarded-For': '127.0.0.1'
}
enable_random_ua = True  # 使用随机UA(默认True，开启可以覆盖request_default_headers的UA)

commoncrawl_search_page = 'CC-MAIN-2021-10-index'