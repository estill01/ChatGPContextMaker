import os
import tempfile
from pathlib import Path
from gpcontext_maker import concat_files_recursive

def create_test_files(base_dir):
    test_files = {
        "file1.txt": "This is file 1.",
        "file2.txt": "This is file 2.",
        "subdir1/file3.txt": "This is file 3 in subdir1.",
        "subdir2/file4.txt": "This is file 4 in subdir2.",
    }

    for path, content in test_files.items():
        file_path = os.path.join(base_dir, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            f.write(content)

    return test_files

def test_concat_files_recursive():
    with tempfile.TemporaryDirectory() as temp_dir:
        test_files = create_test_files(temp_dir)
        output_file = os.path.join(temp_dir, "output.txt")
        concat_files_recursive(temp_dir, output_file)

        assert Path(output_file).is_file(), "Output file not created"

        expected_output = ""
        for path, content in test_files.items():
            delimiter = f"\n{'#' * 80}\n# File: {path}\n{'#' * 80}\n\n"
            expected_output += delimiter + content + "\n\n"

        with open(output_file, "r") as f:
            output_content = f.read()

        assert output_content == expected_output, "Output content mismatch"

if __name__ == "__main__":
    test_concat_files_recursive()
    print("Test passed!")
