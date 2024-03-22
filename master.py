import json
import base64
from deepgram import (
    DeepgramClient,
    FileSource,
)
from openai import OpenAI
deepgram = DeepgramClient(
    "765934dbcf14be43b4183b66ccd5274357b8fae7")
openai = OpenAI(
    api_key="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")


def transcribe_and_analyze_audio(audio_file):
    try:

        payload: FileSource = {
            "file": audio_file}

        response = deepgram.transcription.prerecorded(
            payload)
        transcription = response["results"]["channels"][0]["alternatives"][0]["transcript"]


        sentiment = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=f"What is the overall sentiment of the following text: {transcription}?",
            max_tokens=150,
            n=1,
            temperature=0.5,
        )["choices"][0]["text"].strip()

        return {"transcription": transcription, "sentiment": sentiment}

    except Exception as e:
        return {"error": f"Exception: {e}"}


def lambda_handler(event, context):
    try:
        audio_file = event['audio']

        if isinstance(audio_file, str):
            with open("/tmp/audio.wav", "wb") as f:
                f.write(
                    base64.b64decode(audio_file))
            audio_file = "/tmp/audio.wav"

        result = transcribe_and_analyze_audio(
            audio_file)

        return {
            "statusCode": 200,
            "body": json.dumps(result),
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Exception: {e}"}),
        }
