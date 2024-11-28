import requests
import random
from bs4 import BeautifulSoup

from utils.message import *


def getQuestion() -> str | None:

    url = "https://www.haotiw.com/Haoti/DisplayCategory"
    params = {
        "tid": "45k37ycz37y1t31c3x4egwkq5x",
        "cid": "4ax0649z1q92grrh9jx2acc2ww",
        "Options.IsAscending": "False",
        "pagenum": random.randint(1, 20),
    }
    response = requests.get(url, params=params)

    soup = BeautifulSoup(response.text, "html.parser")

    quesList = [
        "https://www.haotiw.com/" + e.attrs["href"] for e in soup.select("header>h1>a")
    ]
    ques = random.choice(quesList)
    return getQuestionPic(ques)


def getQuestionPic(ques: str) -> str | None:
    html = requests.get(ques).text
    soup = BeautifulSoup(html, "html.parser")
    img = soup.select_one("#free-answer img")
    if img == None:
        return None
    return "https://www.haotiw.com" + img.attrs["src"]


#     try:
#         return "https://wenzi.biaoqingbao999.cn" + resp.json()["data"]["gif_url"]
#     except:
#         return None


def everydayUp(message: dict, executor) -> None:
    # Group Only
    if message["message_type"] != "group":
        return
    print("天天向上")
    command = parseCommand(message)
    if command == None:
        return
    text = command["arg"]
    url = getQuestion()
    if url == None:
        return

    executor.sendGroupMsg(message["group_id"], f"[CQ:image,file={url}]")
