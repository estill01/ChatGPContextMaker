import os
import tempfile
from pathlib import Path
from gpcontext_maker import make_context

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


# tests concatenation, but accounts for different orders files might be accessed in
def test_make_context():
    with tempfile.TemporaryDirectory() as temp_dir:
        test_files = create_test_files(temp_dir)
        output_file = os.path.join(temp_dir, "output.txt")
        make_context(temp_dir, output_file)

        assert Path(output_file).is_file(), "Output file not created"

        expected_output_sections = []
        for path, content in test_files.items():
            delimiter = f"\n{'#' * 80}\n# File: {path}\n{'#' * 80}\n\n"
            expected_output_sections.append(delimiter + content + "\n\n")

        with open(output_file, "r") as f:
            output_content = f.read()

        output_sections = output_content.split("\n" + "#" * 80)[1:]

        # Sort sections for comparison
        expected_output_sections.sort()
        output_sections.sort()

        assert output_sections == expected_output_sections, "Output content mismatch"


if __name__ == "__main__":
    test_make_context()
    print("Test passed!")

