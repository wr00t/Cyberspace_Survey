import json
import random
import time

import requests
from config import settings
from common.search import Search
from config.log import logger


class GithubEmail(Search):
    def __init__(self):
        Search.__init__(self)
        self.source = 'GithubEmailAPI'
        self.url = "https://api.github.com/"
        self.token = random.choice(settings.github_token_list)
        self.module = 'Personal'
        self.session = requests.Session()
        self.proxy = self.get_proxy(self.source)
        self.search_data = []
        self.usage = settings.github_usage

    def search(self, targets):
        self.session.headers = self.get_header()
        self.session.proxies = self.get_proxy(self.source)
        self.session.verify = self.verify
        self.session.headers.update(
            {'Accept': 'application/vnd.github.v3.text-match+json', 'Authorization': 'token ' + self.token})
        if not self.auth_github(self.url):
            logger.log('ERROR', f'{self.source} module login failed')
            return
        github_results = self.session.get(self.url + 'users/%s' % targets).json()
        if 'repos_url' in github_results:
            logger.log('INFOR', f'github 用户 {targets} 存在,继续查询.')
            recent_commits = requests.get(self.url + 'users/%s/events' % targets).json()
            for i in recent_commits:
                # Emails from recent commits 从最近的 commits 查看是否存在邮箱
                if 'commits' in i['payload']:
                    for j in i['payload']['commits']:
                        tmp = {'name': j['author']['name'], 'email': j['author']['email'], 'repo': i['repo']['name'],
                               'url': i['repo']['url'], 'source': 'Emails from recent commits'}
                        self.search_data.append(tmp)

            # 获得 repo 名
            try:
                # Emails from owned-repo recent activity 从用户最近的仓库活动查看是否存在邮箱
                recent_repo = self.session.get(self.url + 'users/%s/repos?type=owner&sort=updated' % targets, timeout=(5, 10)).json()
                for i in recent_repo:
                    owned_repo = i['name']
                    # 获得 email author
                    recent_activity = requests.get(self.url + 'repos/%s/%s/commits' % (targets, owned_repo)).json()
                    time.sleep(random.random())
                    for j in recent_activity:
                        # j['committer'] 也有个 author
                        tmp = {'name': j['commit']['author']['name'], 'email': j['commit']['author']['email'],
                               'repo': owned_repo, 'url': j['url'], 'source': 'Emails from owned-repo recent activity'}
                        self.search_data.append(tmp)
            except Exception as e:
                logger.log('ERROR', e.args)


    def github_email(self, targets):
        deal_target_results = self.deal_target(targets)
        for i in deal_target_results:
            self.search(i)
            if self.search_data:
                self.search_data = self.deleteDuplicate(self.search_data)
            else:
                logger.log('ERROR', f'{self.source}: Not Found，可能是请求次数的原因')


    def run(self, targets):
        print(self.usage)
        if not self.have_api(self.token):
            return
        self.begin()
        GithubEmail.github_email(self, targets)
        print(json.dumps(self.search_data, sort_keys=False, indent=4))
        self.finish()
        return json.dumps(self.search_data, ensure_ascii=False)

def run(targets):
    search = GithubEmail()
    search_data = search.run(targets)
    return search_data

if __name__ == '__main__':
    run(['githb_id'])
