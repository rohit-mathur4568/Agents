import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
import pyttsx3
import math
import re

engine = pyttsx3.init()
engine.setProperty("rate", 160)

def speak(text):
    print("🤖", text)
    engine.say(str(text))
    engine.runAndWait()

def listen():
    fs = 44100
    seconds = 6

    print("\n🎤 Speak your calculation...")
    recording = sd.rec(
        int(seconds * fs),
        samplerate=fs,
        channels=1,
        dtype="int16"
    )
    sd.wait()

    write("voice.wav", fs, recording)

    r = sr.Recognizer()
    with sr.AudioFile("voice.wav") as source:
        audio = r.record(source)

    try:
        text = r.recognize_google(audio)
        print("You said:", text)
        return text.lower()
    except:
        speak("Sorry, I could not understand.")
        return ""

def prepare_expression(text):
    text = text.lower()

    replacements = {
        "plus": "+",
        "add": "+",
        "minus": "-",
        "subtract": "-",
        "multiply by": "*",
        "multiplied by": "*",
        "multiply": "*",
        "times": "*",
        "into": "*",
        "divide by": "/",
        "divided by": "/",
        "divide": "/",
        "over": "/",
        "power of": "**",
        "to the power of": "**",
        "to the power": "**",
        "power": "**",
        "mod": "%",
        "modulus": "%",
        "point": ".",
        "pi": "math.pi",
        "pie": "math.pi",
        "e": "math.e",
    }

    for word, symbol in replacements.items():
        text = text.replace(word, symbol)

    # square root of 49
    text = re.sub(r"square root of (\d+)", r"math.sqrt(\1)", text)
    text = re.sub(r"square root (\d+)", r"math.sqrt(\1)", text)

    # cube root of 27
    text = re.sub(r"cube root of (\d+)", r"(\1 ** (1/3))", text)
    text = re.sub(r"cube root (\d+)", r"(\1 ** (1/3))", text)

    # sin 30 degree
    text = re.sub(r"sin (\d+) degree", r"math.sin(math.radians(\1))", text)
    text = re.sub(r"cos (\d+) degree", r"math.cos(math.radians(\1))", text)
    text = re.sub(r"tan (\d+) degree", r"math.tan(math.radians(\1))", text)

    # log 100
    text = re.sub(r"log (\d+)", r"math.log10(\1)", text)

    # natural log 10
    text = re.sub(r"natural log (\d+)", r"math.log(\1)", text)
    text = re.sub(r"ln (\d+)", r"math.log(\1)", text)

    # factorial 5
    text = re.sub(r"factorial of (\d+)", r"math.factorial(\1)", text)
    text = re.sub(r"factorial (\d+)", r"math.factorial(\1)", text)

    # percentage: 20 percent of 500
    text = re.sub(r"(\d+) percent of (\d+)", r"(\1/100)*\2", text)

    return text

def calculate(command):
    if command.strip() == "":
        return "Invalid calculation"

    expression = prepare_expression(command)

    allowed_chars = "0123456789+-*/().,% mathsqrtlogsincoatrdepi_"
    for ch in expression:
        if ch not in allowed_chars:
            return "Invalid calculation"

    try:
        result = eval(expression, {"math": math, "__builtins__": {}})
        return round(result, 6)
    except Exception:
        return "Invalid calculation"

def main():
    speak("Advanced Voice Calculator Agent started.")

    while True:
        command = listen()

        if "stop" in command or "exit" in command or "quit" in command:
            speak("Voice calculator stopped.")
            break

        result = calculate(command)
        speak(f"The answer is {result}")

if __name__ == "__main__":
    main()