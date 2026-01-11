import os
import yt_dlp


def detect_platform(url):
    """Detect the platform from the URL."""
    if 'youtube.com' in url or 'youtu.be' in url:
        return 'YouTube'
    elif 'soundcloud.com' in url:
        return 'SoundCloud'
    else:
        return 'Unknown'


def get_best_audio_format(video_url):
    ydl_opts = {
        'format': 'bestaudio',
        'quiet': True,
        'noplaylist': True,
        'forcetitle': True,
        'skip_download': True,
        'nocheckcertificate': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(video_url, download=False)
            # Filter out HLS formats and get audio-only formats
            audio_formats = [
                f for f in info_dict.get('formats', [])
                if f.get('acodec', 'none') != 'none' 
                and f.get('vcodec') == 'none'  # Audio-only formats
                and 'hls' not in f.get('protocol', '').lower()  # Exclude HLS
                and 'm3u8' not in f.get('url', '').lower()  # Exclude m3u8
            ]
            
            if not audio_formats:
                # Fallback: try to get any audio format if no audio-only formats found
                audio_formats = [
                    f for f in info_dict.get('formats', [])
                    if f.get('acodec', 'none') != 'none'
                    and 'hls' not in f.get('protocol', '').lower()
                    and 'm3u8' not in f.get('url', '').lower()
                ]
            
            if audio_formats:
                print("\nAvailable audio qualities:")
                for f in audio_formats:
                    abr = f.get('abr', 'Unknown')
                    print(f"- {abr} kbps (format: {f.get('format_id', 'unknown')})")
                highest_quality = max(audio_formats, key=lambda x: int(x.get('abr', 0) or 0))
                return highest_quality.get('abr')
            else:
                print("\nWarning: No suitable audio formats found. Will use default format.")
                return None
        except Exception as e:
            print(f"Error getting audio format info: {e}")
            return None

def download_audio(video_url, format='mp3'):
    """Download audio from YouTube, SoundCloud, or other supported platforms."""
    downloads_folder = os.path.expanduser('~/Downloads')
    
    # Format selector: prefer best audio, avoid HLS/m3u8 formats
    # This selector prioritizes non-HLS audio formats (http_dash_segments, http, https)
    # and explicitly excludes HLS protocols
    format_selector = 'bestaudio[protocol!=m3u8_native][protocol!=m3u8]/bestaudio/best[height<=480]'
    
    options = {
        'format': format_selector,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': format,
            'preferredquality': '192',  # Good quality without being too large
        }],
        'outtmpl': os.path.join(downloads_folder, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'nocheckcertificate': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        },
        # Additional options to handle problematic videos
        'ignoreerrors': False,
        'no_warnings': False,
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([video_url])
            print(f"\nDownload complete! File saved to {downloads_folder}")
    except Exception as e:
        print(f"\nError during download: {e}")
        print("\nTrying alternative format selector...")
        # Fallback: try with simpler format selector that avoids HLS
        options['format'] = 'bestaudio[protocol!=m3u8_native][protocol!=m3u8]/bestaudio/best'
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([video_url])
            print(f"\nDownload complete! File saved to {downloads_folder}")

if __name__ == "__main__":
    print("Audio Downloader (YouTube, SoundCloud, and more)")
    print("Type 'quit' or 'q' to exit\n")

    while True:
        video_url = input("Enter URL: ").strip()

        if video_url.lower() in ['quit', 'q', 'exit']:
            print("Goodbye!")
            break

        if not video_url:
            continue

        platform = detect_platform(video_url)
        print(f"Detected platform: {platform}")

        format_choice = input("Enter format (mp3/wav) [mp3]: ").lower().strip() or 'mp3'
        if format_choice not in ['mp3', 'wav']:
            print("Invalid format. Defaulting to mp3.")
            format_choice = 'mp3'

        best_quality = get_best_audio_format(video_url)
        download_audio(video_url, format_choice)
        print()  # Blank line between downloads
