yellow = '\033[01;33m'
white = '\033[01;37m'
green = '\033[01;32m'
blue = '\033[01;34m'
red = '\033[1;31m'
end = '\033[0m'
from termcolor import colored


# usage
shodan_usage = f"""{red}shodan usage:{yellow}
搜集某个城市的特定设备: 
tplink city:"nanjing"

搜索特定版本的操作系统及端口: 
Apache city:"Seoul" port:"8080"
Apache city:"Hong Kong" port:"8080"  product:"Apache Tomcat/Coyote JSP engine"
hostname:".polyu.edu.hk" os:"windows"

搜索指定国家地域特定类型的工具服务 
port:"8080" jboss country:CN

搜索指定 hostname
hostname:".fofa.so"

搜索指定 ip
net:"158.247.211.17"

扫描指定网段内的所有特定数据库服务器:
product:"Mysql"  net:"140.117.13.0/24" port:"3306"

搜各类路由的特定web管理端口:
port:"21" net:"107.160.1.0/24"

搜缺省密码:
"default password" city:"Hong Kong"

搜索使用 ico 的资产
http.favicon.hash:"-247388890"

搜索各类漏洞摄像头:
netcam net:"187.189.82.0/24"

shodan init [API_Key]
查看指定主机的相关信息，如地理位置信息，开放端口，甚至是否存在某些漏洞等信息。
shodan host 192.168.111.111

易受心脏滴血漏洞影响的设备数量
shodan count vuln:cve-2014-0160 

获取域的子域名列表
shodan domain cnn.com

查找位于瑞士的服务器最常见的10个漏洞
shodan stats --facets vuln country:CH 

you can see more in https://snippets.shodan.io/tag/shodan{end}
"""

fofa_usage = f"""{red}fofa usage:{yellow}
奇技淫巧:
title="Burp Suite" && body="Proxy History"\t未授权burp
body="indeterminate" && body="MainController" && header="X-Powered-By:Express"\tShadowsocks-Manager登陆界面
body="get all proxy from proxy pool"\t获取免费的的代理池
body="miner start"\t挖矿
(header="uc-httped 1.0.0" &&server="JBoss-5.0") || server="Apache,Tomcat,Jboss,weblogic,phpstudy,struts"\t一些蜜罐
title="疫情" && (title="防控" || title="监控") &&country="CN"\t疫情监控防控系统
body="hacked by"\t黑页
title="指挥" && title="登陆"\t指挥系统的登陆后台
(body="password.txt" || body="密码.txt") && title="index of"\t密码文件
body="img/mhn_logo.png" && body="world-map"\t蜜罐捕获攻击情况(红色为攻击者，黄色为蜜罐部署位置)
body="选择区服" && body="充值" && body="后台"\t游戏充值后台
body="intitle:"index of" squirrelmail/"\t搜索邮箱配置文件
title="GM管理后台" title="传奇后台" body="GM校验码"\t私服GM管理后台一般都有默认密码，数据库弱口令，后门或者注入
body="admin" && body="123456" && title="登陆"\t明文显示用户名密码
body="UA-111801619-3"\t各种机场登陆注册
body="SSPanel-Uim"\tss 机场框架
body="<a href="/staff\">STAFF</a>" && body="<a href=\"/tos\">"\t机场【科学上网】
title="Index of" && body="rar"\t搜索源代码等文件
body="x.aspx" && body="asp"\twebshell
title="X-Ray Report" || body="Powered by xray"\txray扫描结果
title="Site not found " && server == "cloudflare"\t
header="Set-Cookie: TWFID="\t深信服VPN远程代码执行
app="深信服-SSL-VPN"\t深信服 VPN 口令爆破
"Fortigate" && port=10443\tFortigate SSL VPN 文件读取/远程代码执行
protocol=="java-rmi"\tRMI 对外开放

cobalt strike:(仅供参考)
header="HTTP/1.1 404 Not Found Content-Type: text/plain Date:"||protocol="cobaltstrike"||cert="Serial Number: 146473198"\tCobalt Strike 3.13三个特征
cs3.14
cert="A6:F6:B4:60:64:3F:25:75:CA:54:AA:DE:FB:F5:83:24:BE:C1:C6:B9" && before="2020-01-01"
cs4.0
cert="7E:80:01:F2:F6:C1:53:51:89:52:36:55:BB:92:D9:99:A1:C2:39:10" && before="2020-01-01"
cs4.1
cert="16:FC:06:61:2D:C2:20:8E:90:83:56:2D:04:4C:6F:FA:5D:2A:3F:4E" && before="2020-01-01"
header="HTTP/1.1 404" && header="Content-Type: text/plain" && header="Content-Length: 0" && header != "Server: " && header!="Connection: "\tCobaltStrike Beacon Staging Server


产品:
app="Nexus-Repository-Manager"
app="FIT2CLOUD-JumpServer-堡垒机"
intext:"Powered by vBulletin" 或者 app="vBulletin"
app="SALTSTACK-产品"
app="XXL-JOB"
app="ThinkAdmin"
app="APACHE-kylin"
Apache Shiro
app="Apache-Shiro"
app="泛微-协同办公OA"
app="通达OA"
app="用友-致远OA"
app="致远互联-OA"
app="shterm-堡垒机"
app="Microsoft-Exchange"
app="Coremail"
app="Winmail-Server"\tWinmail 相关漏洞
app="Zabbix"
app="ThinkPHP"
app="Spring-Framework"
app="phpStudy 探针"\tPhpstudy 后门远程代码执行{end}
"""

google_usage = f"""{red}google usage:{yellow}
利用 Google 搜索C段服务器信息
site:218.87.21.*

Google Google搜索后缀名
ext:inc "pwd=" "UID="
ext:ini intext:env.ini

搜集各种账号密码
inurl:password.txt

重要配置文件泄露
inurl:/application/configs/  配置文件名为/application/configs/application.ini

Google 搜索目录遍历
intext:"#mysql dump" filetype:sql

Google 查找web入口
intext:$CATALINA_HOME/webapps/ROOT/ inurl:8080/ 

搜集 weblogic 入口
inurl:/console/login/LoginForm.jsp intitle:Oracle WebLogic Server

搜集 jboss 入口
inurl:/jmx-console/htmladaptor

搜集websphere入口:
inurl:/ibm/console/logon.jsp

搜集phpmyadmin入口:
inurl:/phpMyAdmin/index.php intext:phpMyAdmin 2.7.0 

搜 wordpress 程序
index of /wp-content/uploads inurl:/wp-login.php

批量搜 joomla 程序
inurl:index.php?option=com_advertisementboard 

owa入口
inurl:/owa/auth/logon intitle:outlook
inurl:/owa/auth/logon intext:outlook

vpn入口
inurl:/sslvpn site:hk{end}
"""

hunter_usage = f"""{red}hunter usage:{yellow}
--target baidu.com
--targets baidu.com google.com
--plateform hunter_search

--mode search  (无返回结果不计入消费次数)
有两个功能
1.输入为 bytedance.com 则为查询bytedance泄露的所有个人(可以在源码上讲类型改为general邮箱,这样做会导致hr@bytedance.com也会进行保存)邮箱
2.输入为 https://hunter.io/blog/how-to-know-if-someone-read-your-email/,它会找到文章的作者以及给定域名上最有可能的电子邮件地址。(鸡肋)

--plateform hunter_verify (无返回结果不计入消费次数)
输入为邮箱,会验证该邮箱是否存在且是否在互联网上披露{end}
"""

github_usage = f"""{red}github usage:{yellow}
输入为 github id
github email(reference: https://github.com/paulirish/github-email) 
Emails from recent commits 从最近的 commits 查看是否存在邮箱
Emails from owned-repo recent activity 从用户最近的仓库活动查看是否存在邮箱{end}
"""

google_leak_usage = f"""{red}google_leak usage:{yellow}
输入为域名如 freebuf.com
(Directory Traversal) site:freebuf.com AND intitle:index.of | inurl:/.svn/entries | inurl:/.git | inurl:/.DS_Store | inurl:/phpMyAdmin | inurl:/application | inurl:key | inurl:rsa
(Leak File) site:freebuf.com AND ext:xml | ext:conf | ext:cnf | ext:reg | ext:inf | ext:rdp | ext:cfg | ext:txt | ext:ora | ext:ini | ext:sql | ext:dbf | ext:mdb | ext:log |ext:bkf | ext:bkp | ext:bak | ext:old | ext:backup | ext:doc | ext:docx | ext:odt | ext:pdf | ext:rtf | ext:sxw | ext:psw | ext:ppt | ext:pptx | ext:pps | ext:csv | ext:php | intitle:phpinfo | inurl:pass"{end}
"""

endpoint_search_usage = f"""{red}endpoint_search usage:{yellow}
输入为域名如 t00ls.net
调用接口: index.commoncrawl.org web.archive.org api.github.com
commoncrawl: 在 commoncrawl 查找域名为 *.t00ls.net 的所有爬取地址
wayback machine: 在 wayback 查找域名为 t00ls.net(包括子域名) 的所有网站快照
{end}
"""
iknowwhatyoudownload_find_usage = f"""{red}iknowwhatyoudownload usage:{yellow}
website: https://iknowwhatyoudownload.com/en/peer/
API server URL: https://api.antitor.com
Peer API: http://iknowwhatyoudownload.com/assets/docs/PeerAPI.html
Content APISpecification: http://iknowwhatyoudownload.com/assets/docs/ContentAPI.html
Torrent APISpecification: http://iknowwhatyoudownload.com/assets/docs/TorrentAPI.html
Free Total requests limit: 1000{end}
"""
github_dork_usage = f"""{red}github_leak usage:{yellow}
使用 github dork 搜索泄露数据,dork主要来自于 github-dorks(https://github.com/techgaun/github-dorks)项目中
调用 github 的 https://api.github.com/search/code 接口,使用 dork 进行查询
对于使用基本身份验证或OAuth的API请求，您每小时最多可以进行5,000个请求。无论使用了基本身份验证还是OAuth令牌，已身份验证的请求都与已身份验证的用户相关联。这意味着，当用户授权的所有OAuth应用程序使用同一用户拥有的不同令牌进行身份验证时，它们每小时共享5,000个请求的相同配额。
对于属于GitHub Enterprise Cloud帐户的用户，使用OAuth令牌向同一GitHub Enterprise Cloud帐户拥有的资源发出的请求每小时增加15,000个请求。
使用GITHUB_TOKENGitHub Actions中的内置功能时，每个存储库的速率限制为每小时1,000个请求。对于属于GitHub Enterprise Cloud帐户的组织，此限制为每个存储库每小时15,000个请求。
https://api.github.com/users/github_id
X-RateLimit-Limit	每小时允许您发出的最大请求数。
X-RateLimit-Remaining	当前速率限制窗口中剩余的请求数。
X-RateLimit-Reset	当前速率限制窗口重置的时间
dork(冒号后无空格):
user:github_id
repo:github_id/repo
java user:github_id language:java
用户可以自行输入 dork,程序会使用默认的泄露密钥的 dork 与用户输入 dork 进行拼接。(次数有限不推荐批量)
{end}
"""
ti_qax_usage = f"""{red}ti_qax usage:{yellow}
ip 信誉: 8.8.8.8
文件信誉: md5(32)/sha1(40)/sha256(64)
失陷检测: IP/域名/URL
请求参数: 
ignore_url	是否忽略IOC中的URL部分内容，true为忽略，false为不忽略。忽略后会产生更多报警，但精度不足可能存在误警 选填 true/false 默认值为true
ignore_port	是否忽略IOC中的port部分内容，true为忽略，false为不忽略。忽略后会产生更多报警，但精度不足可能存在误警 选填 true/false 默认值为true
ignore_top	是否忽略全球域名解析中TOP1000的域名，true为忽略，false为不忽略。不忽略TOP网站可以防止忽略URL、Port后由可能带来的大量误警 选填 true/false 默认值为true
{end}"""
ti_inquest_usage = f"""{red}ti_inquest usage:{yellow}
inquest 支持输入邮箱、ip、domain、url
{end}"""
ti_otx_usage = f"""{red}ti_alienvault usage:{yellow}
AlienVaultOTX 支持输入邮箱、ip、domain
hostname: https://otx.alienvault.com/api/v1/indicators/hostname/xred.mooo.com/general
domain: https://otx.alienvault.com/api/v1/indicators/domain/mooo.com/general
file: https://otx.alienvault.com/api/v1/indicators/file/f590e1b6a80cf3e8360388382eabb04b3e247b78/general
pluse_id: https://otx.alienvault.com/api/v1/pulses/6036b5265ae36030329f4ad9
{end}"""
tools_ico_usage = f"""{red}tools_ico usage:{yellow}
输入 ico 地址转化为hash
shodan 搜索语法: http.favicon.hash:"-1588080585"
fofa 搜索语法: icon_hash="-247388890"
{end}"""
tools_cert_usage = f"""{red}tools_cert usage:{yellow}
输入网站地址识别该网站的证书
输入格式为: www.baidu.com:443、111.111.111.111:50050
不输入端口默认为 443 端口
{end}"""
baidumap_usage = f"""{red}tools_exif usage:{yellow}
识别照片中的 exif 信息,调用百度地图接口获得详细地址
{end}"""
file_usage = f"""{red}tools_file usage:{yellow}
打印文件信息: hex、md5、sha1、sha256
{end}"""
dns_resvolve_usage = f"""{red}dns_resvolve usage:{yellow}
调用司南接口正向解析(支持正则如*.baidu.com)
默认取 100 条数据, 具体条数可以到 setting.py 进行修改
{end}"""
dns_reverse_usage = f"""{red}dns_reverse usage:{yellow}
调用司南接口反向解析
默认取 100 条数据, 具体条数可以到 setting.py 进行修改
{end}"""
dns_whois_usage = f"""{red}dns_whois usage:{yellow}
调用司南接口查询 whois 信息
{end}"""
dns_pdns_usage = f"""{red}dns_pdns usage:{yellow}
调用司南接口查询 pdns 信息
默认取 100 条数据, 具体条数可以到 setting.py 进行修改
{end}"""
dns_subdomain_usage = f"""{red}dns_subdomain usage:{yellow}
调用司南接口查询子域名信息
默认取 100 条数据, 具体条数可以到 setting.py 进行修改
{end}"""
ip_detail_usage = f"""{red}ip_detail usage:{yellow}
调用网络安全研究院查询 ip 位置信息
{end}"""
str2hex_usage = f"""{red}str2hex usage:{yellow}
IP/字符串 16 进制相互转换
字符串转16进制需要改为字节类型输入
如果是16进制或者ip则字符串类型输入
{end}"""
if __name__ == '__main__':
    print(shodan_usage)
    print(fofa_usage)
    print(google_usage)
    print(hunter_usage)
    print(github_usage)
    print(google_leak_usage)
    print(endpoint_search_usage)
    print(iknowwhatyoudownload_find_usage)
    print(github_dork_usage)
    print(ti_qax_usage)
    print(ti_inquest_usage)
    print(ti_otx_usage)
    print(tools_ico_usage)