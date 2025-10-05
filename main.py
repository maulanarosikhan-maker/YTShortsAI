from moviepy.editor import ImageClip, CompositeVideoClip, ColorClip, AudioFileClip
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

text = "Halo! Ini adalah video Shorts otomatis yang dibuat dengan AI!"
tts = gTTS(text, lang='id')
tts.save("audio.mp3")

background = ColorClip(size=(720, 1280), color=(0, 0, 255), duration=10)

img_width, img_height = 700, 200
img = Image.new("RGBA", (img_width, img_height), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)
font = ImageFont.load_default()
bbox = draw.textbbox((0, 0), text, font=font)
text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
x, y = (img_width - text_w) // 2, (img_height - text_h) // 2
draw.text((x, y), text, fill="white", font=font)
text_image_path = "text.png"
img.save(text_image_path)

text_clip = ImageClip(text_image_path).set_duration(10).set_position("center")
final_clip = CompositeVideoClip([background, text_clip])
audio = AudioFileClip("audio.mp3")
final_clip = final_clip.set_audio(audio)
output_path = "output.mp4"
final_clip.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")

print("✅ Video berhasil dibuat:", output_path)

if os.path.exists("client_secret.json"):
    try:
        creds = Credentials.from_authorized_user_file("client_secret.json")
        youtube = build("youtube", "v3", credentials=creds)
        request_body = {
            "snippet": {
                "categoryId": "22",
                "title": "Video Shorts Otomatis AI",
                "description": "Video ini dibuat otomatis oleh AI!",
                "tags": ["AI", "Shorts", "Automation"]
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False
            }
        }
        mediaFile = MediaFileUpload(output_path)
        response = youtube.videos().insert(
            part="snippet,status",
            body=request_body,
            media_body=mediaFile
        ).execute()
        print("✅ Video berhasil diupload! ID:", response["id"])
    except Exception as e:
        print("❌ Gagal upload ke YouTube:", e)
else:
    print("⚠️ File client_secret.json tidak ditemukan, upload manual.")
