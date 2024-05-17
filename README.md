# YouTube Audio Downloader

This project provides a simple script to download audio from YouTube videos. It uses `youtube-dl` to extract audio in the highest quality available and saves the files in MP3 or WAV format.

## Requirements

- Python 3.x
- `youtube-dl` 
    
    you will need to - pip3 install --upgrade --force-reinstall "git+https://github.com/ytdl-org/youtube-dl.git" as main build of youtube-dl has bugs with `uploader-id`
- `ffmpeg` (for audio conversion)

## Installation

1. Clone this repository:

git clone https://github.com/yourusername/youtube-audio-downloader.git

2. Install the required packages:

pip3 install -r requirements.txt

pip3 install --upgrade --force-reinstall "git+https://github.com/ytdl-org/youtube-dl.git"

sudo apt-get install ffmpeg # For Ubuntu/Debian or brew install ffmpeg for macOS. IDK for windows.


## Usage

To use the script, run:

python download_audio.py

Then, follow the prompts to enter the YouTube video URL and desired audio format.

## Output

Audio files will be downloaded to the `/youtube/` directory. Ensure this directory exists on your system, or modify the script to point to a different directory.

## Contributing

Contributions to this project are welcome! Please fork the repository and submit a pull request with your enhancements.

## TODO

Will be adding support for different services such as soundcloud, spotify and more. Primarily meant for DJs who need to find a way to download audio. 

Enable SSL verification. Turned off due to some issues with youtube-dl not being able to recognize SSL. Be cautious with links that are uploaded.

## License

This project is released under the MIT License. See the LICENSE file for more details.

