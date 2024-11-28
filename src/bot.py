import asyncio
import queue
import threading
import json
import websockets
import requests

from route import Route
from utils.message import *
from handler import *

sendInterval = 5


class MBot:
    def __init__(self, ip, wsPort, httpPort):
        self.uri = f"ws://{ip}:{wsPort}"
        self.httpURL = f"http://{ip}:{httpPort}"

        # 接收的消息 Dict
        self.msgRecvQueue = queue.Queue()

        # 等待发送的消息 Dict
        self.msgSendQueue = queue.Queue()

        # 维护所有事件
        self.routes: list[Route] = []

    # register 注册一个事件
    def register(self, cmd, handler: HandlerFunc):
        self.routes.append(Route(cmd, handler))

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
                if not self.msgSendQueue.empty():
                    msg = self.msgSendQueue.get()
                    print(msg)
                    url = f"{self.httpURL}/send_msg"
                    threading.Thread(
                        target=lambda: requests.get(url=url, params=msg)
                    ).start()

    def messageHandler(self):
        """处理消息服务"""

        while True:
            if not self.msgRecvQueue.empty():
                message = self.msgRecvQueue.get()
                threading.Thread(target=self.handle, args=[message]).start()

    def sendGroupMsg(self, groupId: int, msg: str) -> None:
        self.msgSendQueue.put(
            {
                "message_type": "group",
                "group_id": groupId,
                "message": msg,
                "auto_escape": False,
            },
        )

    def handle(self, message: dict):
        """处理消息"""

        cmd = parseCommand(message)
        if cmd == None:
            return

        command = cmd["command"]

        for r in self.routes:
            if command == r.cmd:
                r.handler(message, self)
                return

    def run(self):
        threading.Thread(target=lambda: asyncio.run(self.wsReceiver())).start()
        threading.Thread(target=lambda: asyncio.run(self.wsSender())).start()
        threading.Thread(target=lambda: self.messageHandler()).start()
