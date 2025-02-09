import pytest
import zipfile
from src.utils.zip_folder import zip_folder

@pytest.fixture
def create_test_folders(tmp_path):
    folder = tmp_path / "test_folder"
    folder.mkdir()
    (folder / "file1.txt").write_text("content1")
    (folder / "file2.txt").write_text("content2")
    return str(folder)

def test_zip_folder(create_test_folders, tmp_path):
    output_dir = tmp_path / "output"
    zip_name = "test.zip"
    zip_folder(create_test_folders, str(output_dir), zip_name)

    output_zip = output_dir / zip_name
    assert output_zip.exists()

    with zipfile.ZipFile(output_zip, 'r') as zipf:
        assert "file1.txt" in zipf.namelist()
        assert "file2.txt" in zipf.namelist()

def test_zip_folder_non_existing_folder(tmp_path):
    non_existing_folder = tmp_path / "non_existing_folder"
    output_dir = tmp_path / "output"
    zip_name = "test.zip"

    zip_folder(str(non_existing_folder), str(output_dir), zip_name)

    output_zip = output_dir / zip_name
    assert not output_zip.exists()
