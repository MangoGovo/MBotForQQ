import requests
import random
import emoji
from utils.message import *

templates = [
    "1_紫色渐变",
    "2_紫色闪光",
    "3_活力炫彩",
    "4_梦幻渐变",
    "5_经典幻蓝",
    "6_七彩迷离",
    "7_炫如闪电",
    "8_彩色炫影",
    "9_爆闪出击",
    "10_黑白无限",
    "11_微信绿色",
    "12_帽子绿色",
    "13_橙色活力",
    "14_红包的红",
    "15_红色警告",
    "16_魅力粉色",
    "17_清新水蓝",
    "18_五颜六色",
    "19_珊瑚金色",
    "20_炫彩超闪",
    "21_绽放花火",
    "22_黑白眩晕",
    "23_红紫烈焰",
    "24_黄红快炫",
    "25_流金岁月",
    "26_金色烟火",
    "27_热情火花",
    "28_灿烂金星",
    "29_暗绿湖光",
    "30_浅蓝浮光",
    "31_流动泡泡",
    "32_红光闪烁",
    "33_炫空闪耀",
    "34_海浪滚滚",
    "35_波浪闪动",
    "36_烟花灿烂",
    "37_暗夜星火",
    "38_粉红心动",
    "39_量子爆炸",
]


def isContaionEmoji(text: str) -> bool:
    for c in text:
        if emoji.is_emoji(c):
            return True
    return False


def getGifUrl(text: str) -> str | None:
    url = "https://wenzi.biaoqingbao999.cn/submit"
    if isContaionEmoji(text):
        font = "猫啃什锦黑.ttf"
    else:
        font = "Alibaba-PuHuiTi-Bold.ttf"

    data = {
        "user_text": text,
        "duration": "0.2",
        "max_font_size": "50",
        "raw_font_path": font,
        "raw_background_dir": random.choice(templates),
        "line_spacing": "0.9",
        "shape": "正方形",
    }

    resp = requests.post(url, data=data)
    try:
        return "https://wenzi.biaoqingbao999.cn" + resp.json()["data"]["gif_url"]
    except:
        return None


def bqb(message: dict, executor) -> None:
    # Group Only
    if message["message_type"] != "group":
        return

    command = parseCommand(message)
    if command == None:
        return
    text = command["arg"]
    url = getGifUrl(text)
    if url == None:
        return

    executor.sendGroupMsg(message["group_id"], f"[CQ:image,file={url}]")


# if __name__ == "__main__":
#     print(bqb("12311"))
