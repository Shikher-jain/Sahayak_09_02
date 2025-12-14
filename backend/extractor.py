
import fitz
import pytesseract
from PIL import Image
import io
import requests
import youtube_transcript_api
from bs4 import BeautifulSoup
import whisper

# Lazy load tiny model for low memory usage
model_whisper = None

def extract_pdf(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_image(file_bytes):
    image = Image.open(io.BytesIO(file_bytes))
    return pytesseract.image_to_string(image)

def extract_audio(file_bytes):
    global model_whisper
    if model_whisper is None:
        model_whisper = whisper.load_model("tiny")
    temp = "temp_audio.wav"
    with open(temp, "wb") as f:
        f.write(file_bytes)
    result = model_whisper.transcribe(temp)
    return result["text"]

def extract_url(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()

def extract_youtube(video_id):
    transcript = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(video_id)
    return "\n".join([x["text"] for x in transcript])
