from g4f.client import Client
from yt_dlp import YoutubeDL
import os

def generate_text(prompt):
    client = Client()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def get_video(url):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': 'cache/video',  # Задайте путь к папке и имя файла
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    if os.path.exists('cache/video'):
        os.rename('cache/video', 'cache/video.mp4')
