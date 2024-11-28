def parseCommand(message: dict) -> dict | None:
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
