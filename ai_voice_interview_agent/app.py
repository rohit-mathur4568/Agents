import os
import re
import imageio_ffmpeg

# FFmpeg path automatically set
os.environ["PATH"] += os.pathsep + os.path.dirname(
    imageio_ffmpeg.get_ffmpeg_exe()
)

import sounddevice as sd
from scipy.io.wavfile import write
import whisper
import pyttsx3

from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM
)

MODEL_NAME = "google/flan-t5-base"


# ------------------------
# Text To Speech
# ------------------------
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 160)
    engine.say(text)
    engine.runAndWait()


# ------------------------
# Record Audio
# ------------------------
def record_audio(filename="answer.wav", duration=10, fs=16000):

    print("\n🎤 Recording Started...")

    recording = sd.rec(
        int(duration * fs),
        samplerate=fs,
        channels=1
    )

    sd.wait()

    write(filename, fs, recording)

    print("✅ Recording Saved")

    return filename


# ------------------------
# Whisper Speech To Text
# ------------------------
def transcribe_audio(whisper_model, audio_file):

    print("🧠 Converting Speech To Text...")

    result = whisper_model.transcribe(
        audio_file,
        fp16=False
    )

    return result["text"].strip()


# ------------------------
# Load FLAN-T5
# ------------------------
def load_ai_model():

    print("🤖 Loading AI Model...")

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME
    )

    model = AutoModelForSeq2SeqLM.from_pretrained(
        MODEL_NAME
    )

    return tokenizer, model


# ------------------------
# Generate AI Response
# ------------------------
def ask_ai(ai_model, prompt, max_tokens=100):

    tokenizer, model = ai_model

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True
    )

    outputs = model.generate(
        **inputs,
        max_new_tokens=max_tokens,
        do_sample=True,
        temperature=0.7
    )

    response = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return response.strip()


# ------------------------
# Score Extractor
# ------------------------
def extract_score(text):

    match = re.search(
        r"(\d+)\s*/\s*10",
        text
    )

    if match:
        return int(match.group(1))

    return 0


# ------------------------
# Main
# ------------------------
def main():

    print("\n==============================")
    print(" AI Voice Interview Agent")
    print("==============================\n")

    role = input("Enter target role: ")
    level = input("Enter level beginner/intermediate/advanced: ")

    try:
        total_questions = int(
            input("How many questions? ")
        )
    except:
        total_questions = 3

    os.makedirs(
        "reports",
        exist_ok=True
    )

    print("\nLoading Whisper Model...")
    whisper_model = whisper.load_model("base")

    ai_model = load_ai_model()

    total_score = 0
    report_data = []

    speak("Welcome to AI Interview Agent")

    for i in range(total_questions):

        print(f"\n{'='*50}")
        print(f"QUESTION {i+1}")
        print(f"{'='*50}")

        question_prompt = f"""
        You are a professional technical interviewer.

        Generate ONE realistic interview question.

        Role: {role}
        Level: {level}

        Rules:
        - Ask only interview questions.
        - Keep it under 20 words.
        - Return only question.
        """

        question = ask_ai(
            ai_model,
            question_prompt,
            60
        )

        print("\n🤖 Question:")
        print(question)

        speak(question)

        audio_file = record_audio(
            duration=10
        )

        answer = transcribe_audio(
            whisper_model,
            audio_file
        )

        print("\n📝 Your Answer:")
        print(answer)

        feedback_prompt = f"""
        Evaluate interview answer.

        Question:
        {question}

        Candidate Answer:
        {answer}

        Give output exactly:

        Score: x/10

        Strength:
        one line

        Improvement:
        one line
        """

        feedback = ask_ai(
            ai_model,
            feedback_prompt,
            150
        )

        print("\n📊 Feedback:")
        print(feedback)

        score = extract_score(
            feedback
        )

        total_score += score

        report_data.append({
            "question": question,
            "answer": answer,
            "feedback": feedback
        })

    average = total_score / total_questions

    report_file = "reports/interview_report.txt"

    with open(
        report_file,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            "AI INTERVIEW REPORT\n"
        )

        f.write(
            "="*50 + "\n\n"
        )

        f.write(
            f"Role: {role}\n"
        )

        f.write(
            f"Level: {level}\n"
        )

        f.write(
            f"Average Score: {average:.2f}/10\n\n"
        )

        for item in report_data:

            f.write(
                f"Question: {item['question']}\n"
            )

            f.write(
                f"Answer: {item['answer']}\n"
            )

            f.write(
                f"Feedback: {item['feedback']}\n"
            )

            f.write(
                "-"*50 + "\n"
            )

    print("\n==============================")
    print(" INTERVIEW COMPLETED")
    print("==============================")

    print(
        f"\nAverage Score: {average:.2f}/10"
    )

    print(
        f"Report Saved: {report_file}"
    )

    speak(
        "Interview completed. Report saved."
    )


if __name__ == "__main__":
    main()