from Bot import *

ip = "118.178.238.108"
httpPort = "3000"
websocketPort = "3001"

mBot = MBot(ip, websocketPort,httpPort)
mBot.run()

