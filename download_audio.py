import os
import yt_dlp

def get_best_audio_format(video_url):
    ydl_opts = {
        'format': 'bestaudio',
        'quiet': True,
        'noplaylist': True,
        'forcetitle': True,
        'skip_download': True,
        'nocheckcertificate': True,
        'forceurl': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(video_url, download=False)
            audio_formats = [f for f in info_dict['formats'] if f.get('acodec', 'none') != 'none']
            print("\nAvailable audio qualities:")
            for f in audio_formats:
                print(f"- {f.get('abr', 'Unknown')} kbps")
            highest_quality = max(audio_formats, key=lambda x: int(x.get('abr', 0)))
            return highest_quality['abr']
        except Exception as e:
            print(f"Error: {e}")
            return None

def download_audio(video_url, format='mp3'):  # Set default format to 'wav'
    """Download video from YouTube and convert it to MP3 or WAV format."""
    downloads_folder = os.path.expanduser('~/Downloads')
    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': format,
            'preferredquality': '320',  # Updated to highest quality MP3
        }],
        'outtmpl': os.path.join(downloads_folder, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'nocheckcertificate': True,  # SSL certificate check bypassed
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([video_url])

if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    format_choice = input("Enter the audio format (mp3 or wav): ").lower()
    if format_choice not in ['mp3', 'wav']:
        print("Invalid format. Defaulting to wav.")  # Default to WAV if input is incorrect
        format_choice = 'wav'

    best_quality = get_best_audio_format(video_url)
    download_audio(video_url, format_choice)
