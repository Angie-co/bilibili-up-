# -*- coding: utf-8 -*-
# $ Time    :2022/6/12 16:56
# $ Author  :@柒筱暮
# $ GitHub  :https://github.com/Angie-co
# $ File    :up-query.py


from rich import print
import requests
uid = 0

print("""[blue]

██████╗ ██╗   ██╗████████╗██╗  ██╗ ██████╗ ███╗   ██╗
██╔══██╗╚██╗ ██╔╝╚══██╔══╝██║  ██║██╔═══██╗████╗  ██║
██████╔╝ ╚████╔╝    ██║   ███████║██║   ██║██╔██╗ ██║
██╔═══╝   ╚██╔╝     ██║   ██╔══██║██║   ██║██║╚██╗██║
██║        ██║      ██║   ██║  ██║╚██████╔╝██║ ╚████║
╚═╝        ╚═╝      ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
                                                                                                                                                                              
[/blue]""")


def construct_url():
    global uid
    try:
        uid = int(input("输入B站UID："))
    except ValueError:
        print("UID输入非数字!退出程序！")
        exit()
    url = f"https://api.bilibili.com/x/space/acc/info?mid={uid}&jsonp=jsonp"
    return url


def request_code(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/100.0.1185.39",
        "cookie": "buvid3=5E2E32BC-D8A7-4F78-A193-A7E8F29B33E4184979infoc; LIVE_BUVID=AUTO8316162371483785; rpdid=|(mmJmm)YRY0J'uYuYkJ)Yuu; CURRENT_BLACKGAP=0; buvid4=12CF0A1A-4BC7-AAC2-E164-32E01087988B40777-022031316-uDqRMFcPR8562Dnk/2VxYw%3D%3D; buvid_fp_plain=undefined; blackside_state=0; _uuid=A26C5EC8-8AF8-E3A4-7C2B-C9BED1F1B23412078infoc; nostalgia_conf=-1; is-2022-channel=1; CURRENT_QUALITY=80; PVID=2; b_lsid=BD1F1104E_181579A5B9C; bsource=search_bing; fingerprint=066cfe4316b6b2b5bfe74d39f4765ded; i-wanna-go-back=-1; b_ut=7; SESSDATA=d587a650%2C1670584208%2C9a44d%2A61; bili_jct=ea1d93a4767bed16d7d0b8165c5c1e6d; DedeUserID=1609755646; DedeUserID__ckMd5=93ad2e0d5cb5ed6a; sid=jcc6aqdk; innersign=1; CURRENT_FNVAL=4048; b_timer=%7B%22ffp%22%3A%7B%22333.851.fp.risk_5E2E32BC%22%3A%22181579A626E%22%2C%22333.42.fp.risk_5E2E32BC%22%3A%22181579A73FE%22%2C%22333.1007.fp.risk_5E2E32BC%22%3A%22181579A7DF1%22%2C%22333.788.fp.risk_5E2E32BC%22%3A%22181579B8F41%22%7D%7D; buvid_fp=066cfe4316b6b2b5bfe74d39f4765ded"
    }
    date = {
        "jsonp": "jsonp",
        "vmid": uid
    }
    fans_url = "https://api.bilibili.com/x/relation/stat"
    view_url = f"https://api.bilibili.com/x/space/upstat?mid={uid}&jsonp=jsonp"
    resp_code = requests.get(url=url, headers=headers, params=date)
    resp_api = requests.get(url=fans_url, headers=headers, params=date)
    resp_view = requests.get(url=view_url, headers=headers, params={
        "jsonp": "jsonp",
        "mid": uid
    })
    return resp_code.json(), resp_api.json(), resp_view.json()


def fans_num(json):
    # 粉丝数
    fansnum = json["data"]["follower"]
    # 关注数
    following = json["data"]["following"]
    return fansnum, following


def up_name(json):
    # 名字
    upname = json["data"]["name"]
    # 性别
    upsex = json["data"]["sex"]
    # 简介
    upintroduction = json["data"]["sign"]
    # 认证
    upcertification = json["data"]["official"]["title"]
    # 认证补充
    updesc = json["data"]["official"]["desc"]
    return upname, upsex, upintroduction, upcertification, updesc


def up_data(json):
    play_data = json["data"]["archive"]["view"]
    article_data = json["data"]["article"]["view"]
    like = json["data"]["likes"]
    return play_data, article_data, like


if __name__ == '__main__':
    url = construct_url()
    resp_src, api_json, view_json = request_code(url=url)
    try:
        play, article, likes = up_data(view_json)
        fans, followings = fans_num(api_json)
        name, sex, introduction, certification, desc = up_name(resp_src)
        info_dict = {"UP主名字": name, "性别": sex, "关注数": followings, "粉丝数": fans, "播放量": play, "阅读量": article, "获赞数": likes, "简介": introduction, "认证": certification, "认证补充": desc}
        print("\n" + "查找结果：")
        print(f"UP主名字：{name}", f"性别：{sex}", f"B站关注数：{followings}", f"B站粉丝数：{fans}", sep="\n")
        print(f"播放量：{play}", f"阅读量：{article}", f"获赞数：{likes}", sep="\n")
        print(f"简介：{introduction}", f"✅认证：{certification}", f"认证补充：{desc}", sep="\n")
        print("*" * 100)
        print(info_dict)
    except TypeError:
        print("无此UID！")
