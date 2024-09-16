# -*- coding:utf-8 -*-
# @author  : 勾勾
# @time    : ${DATE} ${TIME}
# @function: 群机器人
# @version : V1


import asyncio
import queue
import threading
import time
import json
import websockets
import requests

# 功能模块
from methods.runPy import runPython
from methods.askAI import askAI

sendInterval = 5

class MBot:

    def __init__(self, ip, wsPort, httpPort):
        self.uri = f"ws://{ip}:{wsPort}"
        self.httpURL = f"http://{ip}:{httpPort}"
        # 接收的消息 Dict
        self.msgRecvQueue = queue.Queue()
        # 等待发送的消息 Dict
        self.msgSendQueue = queue.Queue()

    async def wsReceiver(self):
        """接受WebSocket信息"""

        async with websockets.connect(self.uri) as websocket:
            while True:
                message = await websocket.recv()
                print(message)
                msg = json.loads(message)
                if msg["post_type"] == "message":
                    self.msgRecvQueue.put(msg)
                # time.sleep(1)

    async def wsSender(self):
        """发送WebSocket信息"""

        async with websockets.connect(self.uri) as websocket:
            while True:
                if(not self.msgSendQueue.empty()):
                    msg = self.msgSendQueue.get()
                    print(msg)
                    url = f"{self.httpURL}/send_msg"
                    threading.Thread(target=lambda: requests.get(url=url,params=msg)).start()

    def messageHandler(self):
        """处理消息服务"""

        while True:
            if not self.msgRecvQueue.empty():
                message = self.msgRecvQueue.get()
                threading.Thread(target=self.handle, args=[message]).start()

    def parseCommand(self, message: dict) -> dict:
        print(message)
        """获取消息指令
        指令需要以'/'开头
        """
        # 过滤消息
        if message["post_type"] != "message":
            return None

        # 过滤指令
        msgStr = message["raw_message"]
        if msgStr[0] != "/":
            return None

        # 解析指令
        command = msgStr.split("\n")[0].split(" ")[0]
        arg = msgStr[(len(command) + 1) :]
        return {
            "command": command,
            "arg": arg,
        }

    def sendGroupMsg(self, groupId: int, msg: str) -> None:
        self.msgSendQueue.put(
            {
                "message_type": "group",
                "group_id": groupId,
                "message": msg,
                "auto_escape": False,
            },
        )

    def handle(self,message):
        """处理消息"""
        # 解析参数
        cmd = self.parseCommand(message)
        if(cmd == None):
            return
        command = cmd["command"]
        arg = cmd["arg"].strip()

        if (message['message_type'] == "group"):
            """
            群功能
            """
            groupID = message["group_id"]
            if(command == "/hello"):
                """群打招呼"""
                # 判断是否是群消息
                self.sendGroupMsg(groupID,f"[CQ:at,qq={message['user_id']}]泥嚎~")
            elif(command == "/ai"):
                """ai功能"""
                ans = askAI(arg)
                self.sendGroupMsg(groupID, ans)
            elif(command == "/python"):
                "在线编译Pytohn"
                ans = runPython(arg)
                self.sendGroupMsg(groupID, ans)

    def run(self):
        threading.Thread(target=lambda: asyncio.run(self.wsReceiver())).start()
        threading.Thread(target=lambda: asyncio.run(self.wsSender())).start()
        threading.Thread(target=lambda: self.messageHandler()).start()
