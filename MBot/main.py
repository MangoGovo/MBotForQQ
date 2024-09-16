from Bot import *

ip = "127.0.0.1"
httpPort = "3000"
websocketPort = "3001"

mBot = MBot(ip, websocketPort,httpPort)
mBot.run()

