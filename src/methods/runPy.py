import requests
import re
def runPython(code: str):
    print("执行python程序")
    # 获取token
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    }
    url1 = "https://www.jyshare.com/compile/9/"
    try:
        response = requests.get(url1, headers=headers)
        html = response.text
        pattern = r"token = '([^']*)'"
        # 使用re.search查找匹配项
        match = re.search(pattern, html)  
        token = match.group(1)
    except:
        print("获取token失败")

    # 在线编译
    url = "https://www.runoob.com/try/compile2.php"
    data = {
        "code": code,
        "token": token,
        "stdin": "",
        "language": "15",
        "fileext": "py3",
    }
    try:
        data = requests.post(url, headers=headers, data=data).json()
        print(data)
        output = data["output"].strip()
        error = data["errors"].strip()
        if error != "":
            return "错辣~:" + error
        else:
            return output
    except:
        print("在线编译失败")

if __name__ == "__main__":
    code = """print(1)"""
    print(runPython(code))
