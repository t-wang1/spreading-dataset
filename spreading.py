from flask import Flask, request, render_template
import os
import openai
import logging
import re

log_file_path = "/Users/tiffanywang/Documents/spreading/transcription.log"

logging.basicConfig(filename = 'transcription.log', level = logging.DEBUG)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

UPLOAD_FOLDER = "Users/tiffanywang/Documents/spreading"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/upload", methods=["POST"])
def upload_file():

    # creates destination directory if it doesn't already exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    uploaded_file = request.files["file"]
    file_name = uploaded_file.filename

    if 'file' not in request.files or 'textFile' not in request.files:
        return "Both audio file and text file must be uploaded!"

    audio_file = request.files["file"]
    text_file = request.files["textFile"]

    if audio_file.filename == '' or text_file.filename == '':
        return "Both audio file and text file must be selected!"
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    uploaded_file.save(file_path)

    transcription = transcribe_file(file_path)
    result = count_mismatch()

    if transcription is not None:
        logging.debug(transcription)

    try:
        count_mismatch()
    except Exception as e:
        logging.error(f"Error in count_mismatch(): {str(e)}")
    
    return render_template("index.html", result = result)

def transcribe_file(file_path):
    API_KEY = "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"
    model_id = 'whisper-1'

    with open(file_path, "rb") as media_file:
        transcription = openai.Audio.transcribe(
            api_key = API_KEY,
            model = model_id,
            file = media_file,
            response_format = 'text'
        )
    
    output_file_path = "transcription.txt"
    with open(output_file_path, "w") as output_file:
        output_file.write(transcription)
    
    return transcription

# def convert_file():
    file_name = "Users/tiffanywang/Documents/spreading"
    output = pypandoc.convert_file(file_name, format = 'txt')
    assert output == ""

def count_mismatch():
    file1_path = "/Users/tiffanywang/Documents/spreading/transcription.txt"
    file2_path = "/Users/tiffanywang/Documents/spreading/fox-in-socks.txt"

    target_file = open(r"fox-in-socks.txt", "rt")
    data = target_file.read()
    words = data.split()
    total = len(words)

    with open(file1_path, "r") as file1, open(file2_path, "r") as file2:
        content1 = file1.read().split()
        content2 = file2.read().split()

    clean_content1 = [re.sub(r'\W+', '', word).lower() for word in content1]
    clean_content2 = [re.sub(r'\W+', '', word).lower() for word in content2]

    if clean_content1 == clean_content2:
        print("Both files have the same content.")
    else:
        error = sum(1 for w1, w2 in zip(clean_content1, clean_content2) if w1 != w2)
        return f"Number of differences: {error} Total number of words: {total}"
    
if __name__ == "__main__":
    app.run(port = 3000)