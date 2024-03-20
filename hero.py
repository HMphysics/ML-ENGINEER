from flask import Flask, render_template, request
from deepgram import DeepgramClient, PrerecordedOptions, FileSource
import openai
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)


api_key_2 = "765934dbcf14be43b4183b66ccd5274357b8fae7"


api_key = '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'


def transcribe_audio(audio_file):
    try:

        deepgram = DeepgramClient(
            api_key_2)

        with open(audio_file, "rb") as file:
            buffer_data = file.read()

        payload = FileSource(
            buffer_data=buffer_data)

        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
        )

        response = deepgram.listen.prerecorded.v(
            "1").transcribe_file(payload, options)

        return response["results"]["channels"][0]["alternatives"][0]["transcript"]

    except Exception as e:
        return f"Exception: {e}"


def analyze_text(text):
    openai.api_key = api_key

    response = openai.Completion.create(

        engine="gpt-3.5-turbo-instruct",
        prompt=f"What is the overall sentiment of the following text: {text}?",
        max_tokens=150,
        n=1,
        temperature=0.5,
    )

    sentiment = response["choices"][0]["text"].strip(
    )

    return sentiment


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        try:

            if not os.path.exists('uploads'):
                os.makedirs('uploads')

            file_path = os.path.join(
                'uploads', file.filename)
            file.save(file_path)

            transcription = transcribe_audio(
                file_path)

            result = analyze_text(
                transcription)

            return result
        except Exception as e:
            return f"Exception: {e}"


if __name__ == '__main__':
    app.run(debug=False)
