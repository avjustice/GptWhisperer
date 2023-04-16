import os
from config import API_KEY
import openai
from pydub import AudioSegment


def audio_converter(file_name):
    audio = AudioSegment.from_file(file_name, format="ogg")
    new_file_name = f'{file_name}.mp3'
    audio.export(new_file_name, format="mp3")
    os.remove(file_name)
    return new_file_name


def audio_to_text(file_name):
    openai.api_key = API_KEY
    with open(file_name, "rb") as f:
        transcript = openai.Audio.transcribe("whisper-1", f)
    return transcript['text']


def shorten_text(text):
    openai.api_key = API_KEY
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user",
                   "content":
                       f"Cократи текст. {text}"}])
    short_text = completion.choices[0].message.content
    return short_text
