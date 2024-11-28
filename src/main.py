from bot import *

ip = "118.178.238.108"
httpPort = "3000"
websocketPort = "3001"

# 功能模块
from methods.runPy import runPython
from methods.askAI import askAI
from methods.bqb import bqb
from methods.everydayUp import everydayUp

mBot = MBot(ip, websocketPort, httpPort)
mBot.register("/bqb", bqb)
mBot.register("/dayup", everydayUp)

mBot.run()
