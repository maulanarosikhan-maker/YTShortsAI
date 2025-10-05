from moviepy.editor import ImageClip, CompositeVideoClip, ColorClip, AudioFileClip
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

# ======== 1. Buat audio dari teks ========
text = "Halo! Ini adalah video Shorts otomatis yang dibuat dengan AI!"
tts = gTTS(text, lang='id')
tts.save("audio.mp3")

# ======== 2. Buat background warna ========
background = ColorClip(size=(720, 1280), color=(0, 0, 255), duration=10)

# ======== 3. Buat gambar teks manual dengan PIL ========
img = Image.new("RGBA", (700, 200), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Gunakan font default sistem (tanpa install font)
font = ImageFont.load_default()
text_width, text_height = draw.textsize(text, font=font)
x = (700 - text_width) / 2
y = (200 - text_height) / 2
draw.text((x, y), text, fill="white", font=font)

# Simpan ke file sementara
text_image_path = "text.png"
img.save(text_image_path)

# ======== 4. Konversi gambar teks jadi klip video ========
text_clip = ImageClip(text_image_path).set_duration(10).set_position(("center", "center"))

# ======== 5. Gabungkan background dan teks ========
final_clip = CompositeVideoClip([background, text_clip])

# ======== 6. Tambahkan audio ========
audio = AudioFileClip("audio.mp3")
final_clip = final_clip.set_audio(audio)

# ======== 7. Simpan hasil video ========
output_path = "output.mp4"
final_clip.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')

print("✅ Video berhasil dibuat:", output_path)

# ======== 8. Upload otomatis ke YouTube ========
if os.path.exists("client_secret.json"):
    try:
        creds = Credentials.from_authorized_user_file("client_secret.json")
        youtube = build('youtube', 'v3', credentials=creds)

        request_body = {
            'snippet': {
                'categoryId': '22',
                'title': 'Video Shorts Otomatis AI',
                'description': 'Video ini dibuat otomatis oleh AI!',
                'tags': ['AI', 'Shorts', 'Automation']
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False
            }
        }

        mediaFile = MediaFileUpload(output_path)
        response = youtube.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body=mediaFile
        ).execute()

        print("✅ Video berhasil diupload! ID:", response['id'])
    except Exception as e:
        print("❌ Gagal upload ke YouTube:", e)
else:
    print("⚠️ File client_secret.json tidak ditemukan, upload manual.")

