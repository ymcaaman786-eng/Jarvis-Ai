
import requests

def ask_jarvis(question):
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "qwen2.5:3b",
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ],
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()
    data = response.json()

    return data["message"]["content"]


answer = ask_jarvis("Hello Jarvis, introduce yourself.")
print("Jarvis:", answer)
