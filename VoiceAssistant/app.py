import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
import pyttsx3
import datetime
import webbrowser
import os


# Text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 170)


# Whisper model load
# "base" = balanced model, CPU par bhi chal jayega
model = WhisperModel("base", device="cpu", compute_type="int8")


def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()


def record_audio(filename="voice.wav", duration=5, fs=16000):
    print("\nSpeak now...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    write(filename, fs, audio)
    print("Recording completed.")
    return filename


def listen():
    audio_file = record_audio()

    print("Converting voice to text...")
    segments, info = model.transcribe(audio_file)

    text = ""
    for segment in segments:
        text += segment.text + " "

    text = text.strip()
    print("You:", text)

    return text.lower()


def process_command(command):
    if command == "":
        return "I could not hear anything."

    elif "hello" in command or "hi" in command:
        return "Hello bhai, how can I help you?"

    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}"

    elif "date" in command:
        current_date = datetime.datetime.now().strftime("%d %B %Y")
        return f"Today's date is {current_date}"

    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube"

    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        return "Opening Google"

    elif "open github" in command:
        webbrowser.open("https://www.github.com")
        return "Opening GitHub"

    elif "open notepad" in command:
        os.system("notepad")
        return "Opening Notepad"

    elif "open calculator" in command:
        os.system("calc")
        return "Opening Calculator"

    elif "your name" in command:
        return "My name is Voice Assistant."

    elif "stop" in command or "exit" in command or "bye" in command:
        speak("Okay bhai, assistant is shutting down.")
        exit()

    else:
        return "Sorry bhai, I did not understand this command."


def main():
    speak("Voice assistant started. Say a command.")

    while True:
        command = listen()
        response = process_command(command)
        speak(response)


if __name__ == "__main__":
    main()