import random, os
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

QUOTE_FILE = "quotes.txt"
BG_VIDEO = "bg.mp4"

# Ambil teks acak
with open(QUOTE_FILE, "r", encoding="utf-8") as f:
    quotes = f.readlines()
quote = random.choice(quotes).strip()
print("🎙️ Quote:", quote)

# Buat suara
tts = gTTS(quote, lang='id')
tts.save("voice.mp3")

# Buat video
video = VideoFileClip(BG_VIDEO).subclip(0, 15)
audio = AudioFileClip("voice.mp3")

# Tambah teks bergaya gelap (horor/sejarah)
txt = TextClip(quote, fontsize=45, color='white', font="Arial-Bold", size=(720,1280), method='caption')
txt = txt.set_pos('center').set_duration(15)

final = CompositeVideoClip([video.resize((720,1280)), txt])
final = final.set_audio(audio)
final.write_videofile("short.mp4", fps=24, codec="libx264")

# Upload ke YouTube
flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", ["https://www.googleapis.com/auth/youtube.upload"])
credentials = flow.run_console()
youtube = build('youtube', 'v3', credentials=credentials)

upload_request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": f"🕯️ Cerita Singkat | {quote[:30]}...",
            "description": "Video otomatis AI (horor, sejarah, motivasi, fakta)",
            "tags": ["horor", "sejarah", "motivasi", "ai", "shorts"]
        },
        "status": {"privacyStatus": "public"}
    },
    media_body=MediaFileUpload("short.mp4")
)
response = upload_request.execute()
print("✅ Upload selesai:", response["id"])
