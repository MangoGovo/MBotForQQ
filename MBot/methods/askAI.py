import requests


def askAI(ques: str) -> str:
    Api_Key = ""
    url = "https://api.fastgpt.in/api/v1/chat/completions"
    headers = {
            "Authorization": "Bearer " + Api_Key,
            "Content-Type": "application/json",
        }
    data = {
            "chatId": None,
            "stream": False,
            "detail": False,
            "variables": {},
            "messages": [
                {
                    "content": ques,
                    "role": "user",
                }
            ],
        }
    try:
        response = requests.post(url, headers=headers, json=data)
        return response.json()["choices"][0]["message"]["content"]
    except:
        return "AI晕哩~"
