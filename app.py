from flask import Flask, render_template, request
import openai
app = Flask(__name__)


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
        text = file.read().decode("utf-8")
        return analyze_text(text)


def analyze_text(text):
    api_key = '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'
    openai.api_key = api_key

    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=f"What is the overall sentiment of the following text: {text}?",
        max_tokens=150,  
        n=1,  
        temperature=0.5  
    )
    sentiment = response['choices'][0]['text'].strip(
    )

    return sentiment


if __name__ == '__main__':
    app.run(debug=False)
