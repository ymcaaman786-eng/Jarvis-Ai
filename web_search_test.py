
import os
import json
import urllib.request
import urllib.error

api_key = os.getenv("OLLAMA_API_KEY")

if not api_key:
    print("API KEY NOT FOUND")
else:
    print("API KEY FOUND")
    print("Connecting to Ollama Web Search...")

    url = "https://ollama.com/api/web_search"

    data = json.dumps({
        "query": "Who is the current Chief Minister of Delhi?",
        "max_results": 5
    }).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))

        print("\nSEARCH SUCCESSFUL!")

        for item in result.get("results", []):
            print("\nTitle:", item.get("title"))
            print("URL:", item.get("url"))
            print("Content:", item.get("content"))

    except urllib.error.HTTPError as e:
        print("HTTP ERROR:", e.code)
        print("MESSAGE:", e.reason)

    except Exception as e:
        print("ERROR:", str(e))

