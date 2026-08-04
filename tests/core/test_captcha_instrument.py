"""Tests for ``core.captcha_instrument`` — file handling (``FileInstrument``)
and the base instrument's error constant (``CaptchaInstrument``).

These run against the real filesystem using ``tmp_path`` so the file lifecycle
(save → clean) is actually observed, not just call-counted.
"""

import base64

import pytest

from python3_anticaptcha.core.captcha_instrument import CaptchaInstrument, FileInstrument
from python3_anticaptcha.core.serializer import GetTaskResultResponseSer


class TestLocalFileCaptcha:
    def test_reads_exact_file_bytes(self, tmp_path):
        data = b"\x89PNG\r\n\x1a\nbinary-bytes"
        f = tmp_path / "img.png"
        f.write_bytes(data)

        assert FileInstrument._local_file_captcha(captcha_file=str(f)) == data

    def test_base64_encoded_form_matches(self, tmp_path):
        # the instruments base64-encode this output before sending — verify the
        # round-trip that the instruments depend on
        data = b"abc"
        f = tmp_path / "img.png"
        f.write_bytes(data)
        raw = FileInstrument._local_file_captcha(captcha_file=str(f))
        assert base64.b64encode(raw).decode("utf-8") == "YWJj"

    def test_missing_file_raises(self):
        with pytest.raises(FileNotFoundError):
            FileInstrument._local_file_captcha(captcha_file="/no/such/file.png")


class TestFileConstSaver:
    def test_creates_dir_and_file_and_returns_path(self, tmp_path):
        target_dir = tmp_path / "out"
        path = FileInstrument._file_const_saver(content=b"hello", file_path=str(target_dir), file_extension="png")

        # returned path exists and was written
        from pathlib import Path

        p = Path(path)
        assert p.exists()
        assert p.read_bytes() == b"hello"
        # the directory was created
        assert target_dir.is_dir()

    def test_is_idempotent_when_dir_exists(self, tmp_path):
        target_dir = tmp_path / "out"
        target_dir.mkdir()
        # must not raise even though the dir already exists
        path = FileInstrument._file_const_saver(content=b"x", file_path=str(target_dir))
        from pathlib import Path

        assert Path(path).exists()

    def test_filename_has_chosen_extension(self, tmp_path):
        path = FileInstrument._file_const_saver(content=b"", file_path=str(tmp_path), file_extension="jpg")
        assert path.endswith(".jpg")


class TestFileClean:
    def test_removes_existing_directory_tree(self, tmp_path):
        # _file_clean must remove a directory tree (rmtree path).
        target = tmp_path / "captchas"
        target.mkdir()
        (target / "file-uuid.png").write_bytes(b"x")
        FileInstrument._file_clean(full_file_path=str(target))
        assert not target.exists()

    def test_removes_plain_file(self, tmp_path):
        # img_clearing passes the *file* path returned by _file_const_saver,
        # so a plain file must also be removed.
        f = tmp_path / "file.png"
        f.write_bytes(b"x")
        FileInstrument._file_clean(full_file_path=str(f))
        assert not f.exists()

    def test_missing_path_is_silent(self):
        # must not raise on absent path
        FileInstrument._file_clean(full_file_path="/definitely/not/here")


class TestCaptchaInstrumentBase:
    def test_result_is_fresh_get_task_result_response(self):
        inst = CaptchaInstrument()
        assert isinstance(inst.result, GetTaskResultResponseSer)
        # default sentinel used by every error path
        assert inst.result.errorId == 0

    def test_no_captcha_err_constant(self):
        assert CaptchaInstrument.NO_CAPTCHA_ERR == "You did not send any file, local link or URL."
