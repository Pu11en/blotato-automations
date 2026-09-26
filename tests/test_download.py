import io
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

from blotato.download import DownloadTooLarge, download, extension_for


class ExtensionForTest(unittest.TestCase):
    def test_plain_url(self):
        self.assertEqual(extension_for("https://cdn.x/out.jpg", fallback=".bin"), ".jpg")

    def test_query_string_is_not_part_of_the_extension(self):
        # This produced "generated.jpg?token=abc&e=1" as a filename.
        self.assertEqual(
            extension_for("https://cdn.x/out.jpg?token=abc&e=1", fallback=".bin"), ".jpg"
        )

    def test_fragment_is_ignored(self):
        self.assertEqual(extension_for("https://cdn.x/out.mp4#t=3", fallback=".bin"), ".mp4")

    def test_extensionless_url_uses_the_fallback(self):
        self.assertEqual(extension_for("https://cdn.x/render?id=9", fallback=".mp4"), ".mp4")

    def test_unknown_extension_uses_the_fallback(self):
        self.assertEqual(extension_for("https://cdn.x/out.exe", fallback=".jpg"), ".jpg")

    def test_uppercase_is_normalised(self):
        self.assertEqual(extension_for("https://cdn.x/OUT.JPG", fallback=".bin"), ".jpg")

    def test_percent_encoded_path(self):
        self.assertEqual(extension_for("https://cdn.x/my%20file.png", fallback=".bin"), ".png")


class _FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
        return False


class DownloadTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dest = Path(self._tmp.name) / "nested" / "out.jpg"

    def tearDown(self):
        self._tmp.cleanup()

    def test_writes_the_body_and_creates_parents(self):
        with mock.patch("urllib.request.urlopen", return_value=_FakeResponse(b"abc" * 100)):
            written = download("https://cdn.x/out.jpg", self.dest)
        self.assertEqual(written, 300)
        self.assertEqual(self.dest.read_bytes(), b"abc" * 100)

    def test_passes_a_timeout_so_a_stalled_cdn_cannot_hang_forever(self):
        with mock.patch("urllib.request.urlopen", return_value=_FakeResponse(b"x")) as opened:
            download("https://cdn.x/out.jpg", self.dest, timeout=12.5)
        self.assertEqual(opened.call_args.kwargs["timeout"], 12.5)

    def test_refuses_a_body_over_the_ceiling(self):
        with mock.patch("urllib.request.urlopen", return_value=_FakeResponse(b"y" * 5000)):
            with self.assertRaises(DownloadTooLarge):
                download("https://cdn.x/out.jpg", self.dest, max_bytes=1000)

    def test_leaves_no_partial_file_when_the_ceiling_trips(self):
        with mock.patch("urllib.request.urlopen", return_value=_FakeResponse(b"y" * 5000)):
            with self.assertRaises(DownloadTooLarge):
                download("https://cdn.x/out.jpg", self.dest, max_bytes=1000)
        self.assertFalse(self.dest.exists())

    def test_leaves_no_partial_file_when_the_connection_drops(self):
        with mock.patch("urllib.request.urlopen", side_effect=urllib.error.URLError("dropped")):
            with self.assertRaises(urllib.error.URLError):
                download("https://cdn.x/out.jpg", self.dest)
        self.assertFalse(self.dest.exists())


if __name__ == "__main__":
    unittest.main()
