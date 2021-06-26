import random
import re
from pathlib import Path
from config import settings
from config.log import logger


user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/68.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) '
    'Gecko/20100101 Firefox/68.0',
    'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/68.0']

def gen_fake_header():
    """
    Generate fake request headers
    """
    headers = settings.request_default_headers
    if not isinstance(headers, dict):
        headers = dict()
    if settings.enable_random_ua:
        ua = random.choice(user_agents)
        headers['User-Agent'] = ua
    headers['Accept-Encoding'] = 'gzip, deflate'
    return headers

def get_random_header():
    """
    Get random header
    """
    headers = gen_fake_header()
    if not isinstance(headers, dict):
        headers = None
    return headers


def get_random_proxy():
    """
    Get random proxy
    """
    try:
        return random.choice(settings.request_proxy_pool)
    except IndexError:
        return None


def get_proxy():
    """
    Get proxy
    """
    if settings.enable_request_proxy:
        return get_random_proxy()
    return None

def check_response(method, resp):
    """
    检查响应 输出非正常响应返回json的信息

    :param method: 请求方法
    :param resp: 响应体
    :return: 是否正常响应
    """
    if resp.status_code == 200 and resp.content:
        return True
    logger.log('ALERT', f'{method} {resp.url} {resp.status_code} - '
                        f'{resp.reason} {len(resp.content)}')
    content_type = resp.headers.get('Content-Type')
    if content_type and 'json' in content_type and resp.content:
        try:
            msg = resp.json()
        except Exception as e:
            logger.log('DEBUG', e.args)
        else:
            logger.log('ALERT', msg)
    return False

def get_from_target(target):
    target_results = set()
    if isinstance(target, str):
        if target.endswith('.txt'):
            logger.log('FATAL', 'Use targets parameter for multiple query')
            exit(1)
        target_results.add(target)
    elif type(target) == list or type(target) == tuple:
        for i in target:
            target_results.add(i)
    return target_results

def get_from_targets(targets):
    targets_results = set()
    if not isinstance(targets, str):
        return targets_results
    try:
        path = Path(targets)
    except Exception as e:
        logger.log('ERROR', e.args)
        return targets_results
    if path.exists() and path.is_file():
        with open(path, 'r') as file:
            for i in file.readlines():
                targets_results.add(i.strip())
    return targets_results

def get_targets(target, targets=None):
    logger.log('DEBUG', f'Getting domains')
    target_results = get_from_target(target)
    targets_results = get_from_targets(targets)
    results = list(target_results.union(targets_results))
    # if targets_results:
    #     results = sorted(results, key=targets_results.index)  # 按照targets原本的index排序
    if not results:
        logger.log('ERROR', f'Did not get a valid targets name')
    logger.log('DEBUG', f'The obtained targets \n{results}')
    return results

