import os
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

# === 1. Generate Ide Konten Otomatis ===
def generate_idea():
    ideas = [
        "Fakta unik tentang luar angkasa",
        "Kisah misteri yang belum terpecahkan",
        "Motivasi hidup 15 detik",
        "AI menjelaskan sejarah singkat dunia",
        "Tips sukses singkat dari Elon Musk"
    ]
    import random
    return random.choice(ideas)

# === 2. Buat suara otomatis dari teks ===
def generate_audio(text, filename="audio.mp3"):
    tts = gTTS(text=text, lang="id")
    tts.save(filename)
    print(f"🎤 Audio berhasil dibuat: {filename}")

# === 3. Buat video pendek otomatis ===
def create_video(audio_file, output_file="output.mp4"):
    # Buat background dari warna hitam polos
    image = ImageClip("https://picsum.photos/720/1280", duration=15)  # gambar acak
    audio = AudioFileClip(audio_file)
    video = image.set_audio(audio)
    video = video.set_duration(audio.duration)
    video.write_videofile(output_file, fps=24)
    print(f"🎬 Video berhasil dibuat: {output_file}")

# === 4. Upload ke YouTube Shorts ===
def upload_to_youtube(video_file, title, description="Video otomatis oleh AI"):
    if not os.path.exists("client_secret.json"):
        raise Exception("client_secret.json tidak ditemukan!")

    creds = Credentials.from_authorized_user_file("client_secret.json", ["https://www.googleapis.com/auth/youtube.upload"])
    youtube = build("youtube", "v3", credentials=creds)

    request_body = {
        "snippet": {
            "categoryId": "22",
            "title": title,
            "description": description,
            "tags": ["AI", "Shorts", "Automation"]
        },
        "status": {"privacyStatus": "public"}
    }

    media = MediaFileUpload(video_file, chunksize=-1, resumable=True, mimetype="video/mp4")
    upload = youtube.videos().insert(part="snippet,status", body=request_body, media_body=media)
    response = upload.execute()
    print(f"✅ Video berhasil diupload: https://youtu.be/{response['id']}")

# === 5. Jalankan otomatis ===
if __name__ == "__main__":
    idea = generate_idea()
    print(f"💡 Ide konten: {idea}")

    generate_audio(idea)
    create_video("audio.mp3", "shorts.mp4")
    upload_to_youtube("shorts.mp4", idea)
