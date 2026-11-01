
import requests
import win32com.client
import speech_recognition as sr

# Windows voice engine
speaker = win32com.client.Dispatch("SAPI.SpVoice")
speaker.Rate = 0
speaker.Volume = 100

# Speech recognizer
recognizer = sr.Recognizer()


def speak(text):
    print("Jarvis:", text)
    speaker.Speak(text)



def ask_jarvis(question):

    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "qwen2.5:3b",
            "messages": [
                {
                    "role": "system",

                    "content": (
                        "You are Jarvis, Aman’s personal AI assistant. "

                        "LANGUAGE RULES: "
                        "Always respond in clear, grammatically correct English. "
                        "Understand questions in Hindi, English and Hinglish. "
                        "Never reply in Hindi or Devanagari script. "

                        "ACCURACY RULES: "
                        "Accuracy is more important than speed. "
                        "Never guess an answer when you are unsure. "
                        "Never invent names, dates, statistics or facts. "
                        "Do not confuse current and former office holders. "
                        "If you do not know an answer, clearly say that you are not sure. "
                        "Answer the exact question asked. "

                        "RESPONSE RULES: "
                        "Give relevant, factual and direct answers. "
                        "Do not provide unrelated information. "
                        "Keep spoken replies concise, natural and friendly."
                    ),

                },
                {
                    "role": "user",
                    "content": question,
                },
            ],
            "stream": False,
            "options": {
                "temperature": 0.3
            }
        },
        timeout=120,
    )

    response.raise_for_status()

    return response.json()["message"]["content"]




def listen(silent=False):
    try:
        with sr.Microphone() as source:
            if not silent:
                print("Listening...")

            audio = recognizer.listen(
                source,
                timeout=8,
                phrase_time_limit=10
            )

        try:
            question = recognizer.recognize_google(
                audio, language="en-IN"
            )
        except sr.UnknownValueError:
            question = recognizer.recognize_google(
                audio, language="hi-IN"
            )

        if not silent:
            print("You:", question)

        return question

    except (sr.WaitTimeoutError, sr.UnknownValueError):
        return ""

    except sr.RequestError:
        if not silent:
            speak("Speech recognition needs an internet connection.")
        return ""







def handle_command(question):


        command = question.lower().strip()

        # 1. SLEEP COMMAND
        if "go to sleep" in command:
            speak("Okay Aman, going to sleep.")
            return "sleep"

        # 2. EXIT COMMAND
        if command in ["exit jarvis", "quit jarvis", "stop jarvis"]:
            speak("Goodbye Aman.")
            return "exit"

        # 3. OPEN WEBSITES
        websites = {
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
            "github": "https://github.com",
            "wikipedia": "https://www.wikipedia.org",
            "instagram": "https://www.instagram.com",
            "chatgpt": "https://chatgpt.com",
        }

        for name, url in websites.items():

            if f"open {name}" in command:
                import webbrowser

                speak(f"Opening {name}.")
                webbrowser.open(url)

                return "active"

        # 4. OPEN NOTEPAD
        if "open notepad" in command:
            import subprocess

            speak("Opening Notepad.")
            subprocess.Popen(["notepad.exe"])

            return "active"

        # 5. OPEN CALCULATOR
        if "open calculator" in command:
            import subprocess

            speak("Opening Calculator.")
            subprocess.Popen(["calc.exe"])

            return "active"

        # 6. ASK LOCAL AI
        try:

            answer = ask_jarvis(question)

            print("Jarvis AI Response:", answer)

            speak(answer)

        except Exception as error:

            print("Error:", error)
            speak("Sorry, something went wrong.")

        return "active"



def main():
    sleeping = False

    speak("Hello Aman, I am Jarvis AI. How may I help you?")

    while True:
        question = listen()

        if not question:
            continue

        command = question.lower().strip()

        # SLEEP MODE
        if sleeping:

            # Only wake-up command will work
            if "wake up jarvis" in command:
                sleeping = False
                speak("Welcome back Aman. I am awake now.")
            else:
                print("Jarvis is sleeping. Say Wake up Jarvis.")

            continue

        # ACTIVE MODE
        result = handle_command(question)

        if result == "sleep":
            sleeping = True
            continue

        elif result == "exit":
            break


if __name__ == "__main__":
    main()

