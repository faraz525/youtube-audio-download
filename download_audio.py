import os
import certifi
import ssl
import youtube_dl

def get_best_audio_format(video_url):
    ydl_opts = {
        'format': 'bestaudio',
        'quiet': True,
        'noplaylist': True,
        'forcetitle': True,
        'skip_download': True,
        'nocheckcertificate': True,
        'forceurl': True,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(video_url, download=False)
            audio_formats = [f for f in info_dict['formats'] if f['acodec'] != 'none']
            highest_quality = max(audio_formats, key=lambda x: int(x['abr']))
            return highest_quality['abr']
        except Exception as e:
            print(f"Error: {e}")
            return None
        

def download_audio(video_url, format='wav'):  # Set default format to 'wav'
    """Download video from YouTube and convert it to MP3 or WAV format."""
    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': format,
            'preferredquality': '192',  # Not used for WAV, but needed for the option structure
        }],
        'outtmpl': './youtube/%(title)s.%(ext)s',
        'noplaylist': True,
        'nocheckcertificate': True,  # SSL certificate check bypassed
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_url])

if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    format_choice = input("Enter the audio format (mp3 or wav): ").lower()
    if format_choice not in ['mp3', 'wav']:
        print("Invalid format. Defaulting to wav.")  # Default to WAV if input is incorrect
        format_choice = 'wav'

    best_quality = get_best_audio_format(video_url)
    download_audio(video_url, format_choice)
