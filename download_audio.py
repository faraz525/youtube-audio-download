import os
import certifi
import ssl
import youtube_dl

# Setting the SSL context to use certifi's certificates
ssl_context = ssl.create_default_context(cafile=certifi.where())

def download_audio(video_url, format='mp3'):
    """Download video from YouTube and convert it to MP3 or WAV format."""
    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': format,
            'preferredquality': '192',
        }],
        'outtmpl': './youtube/%(title)s.%(ext)s',
        'noplaylist': True,
        'nocheckcertificate': True,
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_url])

if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    format_choice = input("Enter the audio format (mp3 or wav): ").lower()
    if format_choice not in ['mp3', 'wav']:
        print("Invalid format. Defaulting to mp3.")
        format_choice = 'mp3'

    download_audio(video_url, format_choice)
