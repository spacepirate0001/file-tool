import os
from pathlib import Path

import pytest

from src.utils.exceptions import FileToolError
from src.utils.helpers import validate_path


def test_validate_path_special_chars(tmp_path):
    @validate_path(path_args=[0])
    def dummy_func(self, path):
        return path

    # Test with various invalid characters
    invalid_chars = [
        "<",
        ">",
        '"',
        "|",
        "?",
        "*",
    ]  # Removed : as it's needed for Windows paths
    for char in invalid_chars:
        try:
            test_path = str(tmp_path / f"test{char}file.txt")
            dummy_func(None, test_path)
            pytest.fail(f"Expected FileToolError for character: {char}")
        except FileToolError:
            continue


def test_validate_path_with_directories(tmp_path):
    @validate_path(path_args=[0])
    def dummy_func(self, path):
        return path

    # Test valid directory paths
    valid_path = str(tmp_path / "valid_dir" / "test.txt")
    result = dummy_func(None, valid_path)
    assert Path(result).is_absolute()


def test_validate_path_platform_specific(tmp_path):
    @validate_path(path_args=[0])
    def dummy_func(self, path):
        return path

    # Test Windows-style path
    windows_path = str(tmp_path / "folder" / "file.txt").replace("/", "\\")
    result = dummy_func(None, windows_path)
    assert Path(result).is_absolute()

    # Test Unix-style path
    unix_path = str(tmp_path / "folder" / "file.txt")
    result = dummy_func(None, unix_path)
    assert Path(result).is_absolute()


def test_validate_path_nested_directories(tmp_path):
    @validate_path(path_args=[0])
    def dummy_func(self, path):
        return path

    nested_path = str(tmp_path / "dir1" / "dir2" / "test.txt")
    result = dummy_func(None, nested_path)
    assert Path(result).is_absolute()


def test_validate_path_separators(tmp_path):
    @validate_path(path_args=[0])
    def dummy_func(self, path):
        return path

    # Test valid path with proper system separator
    valid_path = str(tmp_path / "dir" / "subdir" / "file.txt")
    result = dummy_func(None, valid_path)
    assert os.path.normpath(result) == os.path.normpath(valid_path)


def test_validate_path_with_unicode(tmp_path):
    @validate_path(path_args=[0])
    def dummy_func(self, path):
        return path

    test_path = str(tmp_path / "тест.txt")
    result = dummy_func(None, test_path)
    assert result == test_path


def test_validate_path_with_spaces(tmp_path):
    @validate_path(path_args=[0])
    def dummy_func(self, path):
        return path

    test_path = str(tmp_path / "file with spaces.txt")
    result = dummy_func(None, test_path)
    assert result == test_path


def test_validate_path_with_relative_path(tmp_path):
    @validate_path(path_args=[0])
    def dummy_func(self, path):
        return path

    rel_path = "./test.txt"
    result = dummy_func(None, rel_path)
    assert os.path.isabs(result)
    assert Path(result).is_absolute()


def test_validate_path_with_multiple_args():
    @validate_path(path_args=[0, 1])
    def dummy_func(self, first_path, second_path, non_path_arg):
        return first_path, second_path, non_path_arg

    result = dummy_func(None, "test1.txt", "test2.txt", "not a path")
    assert len(result) == 3


# tests/test_helpers.py
def test_validate_path_with_invalid_parent_directory(tmp_path):
    @validate_path(path_args=[0])
    def dummy_func(self, path):
        return path

    # Test with nonexistent parent directory
    test_path = str(tmp_path / "nonexistent_dir" / "test.txt")
    result = dummy_func(None, test_path)
    assert os.path.isabs(result)
    parent_dir = os.path.dirname(result)
    assert os.path.exists(parent_dir)


def test_validate_path_with_non_string_argument():
    @validate_path(path_args=[0])
    def dummy_func(self, path):
        return path

    # Test with non-string argument
    result = dummy_func(None, 123)
    assert result == 123
