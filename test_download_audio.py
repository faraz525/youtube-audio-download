from contextlib import redirect_stdout
from io import StringIO
import unittest
from unittest.mock import patch

from yt_dlp.utils import DownloadError

from download_audio import (
    describe_download_error,
    download_audio,
    should_retry_with_fallback,
)


class DownloadErrorHandlingTests(unittest.TestCase):
    def test_drm_error_explains_that_the_track_cannot_be_downloaded(self):
        error = Exception("ERROR: [soundcloud] This video is DRM protected")

        message = describe_download_error(error)

        self.assertIn("DRM-protected", message)
        self.assertIn("cannot be downloaded with yt-dlp", message)
        self.assertFalse(should_retry_with_fallback(error))

    def test_old_soundcloud_404_recommends_upgrading_dependencies(self):
        error = Exception(
            "ERROR: [soundcloud] Unable to download JSON metadata: "
            "HTTP Error 404: Not Found"
        )

        message = describe_download_error(error)

        self.assertIn("pip3 install --upgrade -r requirements.txt", message)
        self.assertFalse(should_retry_with_fallback(error))

    def test_missing_requested_format_uses_fallback_selector(self):
        error = Exception("ERROR: Requested format is not available")

        self.assertTrue(should_retry_with_fallback(error))

    def test_unknown_download_error_preserves_original_message(self):
        error = Exception("ERROR: network connection failed")

        self.assertEqual(
            "Download failed: ERROR: network connection failed",
            describe_download_error(error),
        )
        self.assertFalse(should_retry_with_fallback(error))

    @patch("download_audio.yt_dlp.YoutubeDL")
    def test_drm_download_error_stops_without_retrying(self, youtube_dl):
        downloader = youtube_dl.return_value.__enter__.return_value
        downloader.download.side_effect = DownloadError(
            "ERROR: [soundcloud] This video is DRM protected"
        )

        with redirect_stdout(StringIO()) as output:
            result = download_audio("https://soundcloud.com/example/drm-track")

        self.assertFalse(result)
        youtube_dl.assert_called_once()
        self.assertIn("cannot be downloaded with yt-dlp", output.getvalue())


if __name__ == "__main__":
    unittest.main()
