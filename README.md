# ChatGPContextMaker

ChatGPContextMaker is a command-line utility that concatenates files in a directory and its subdirectories into a single file. It is particularly useful when you want to provide an entire program as context to an AI like ChatGPT to work on code projects.

# Features

- Recursively concatenate files from a directory and its subdirectories
- Provide a default output location (current working directory) and default output file name
- Prevent overwriting existing files by appending the current datetime to the output file name
- Easily installable and usable via pip and Poetry

## Installation

### Using pip

You can install ChatGPTContextMaker directly from PyPI using pip:

```
pip install chatgpcontextmaker
```

### Using Poetry

Alternatively, you can install ChatGPTContextMaker using Poetry:

1. Install Poetry, if you haven't already:
```
pip install poetry
```

2. Add ChatGPTContextMaker to your project's dependencies:
```
poetry add chatgpcontextmaker
```

## Usage

### As a command-line tool
To use ChatGPContextMaker as a command-line tool, you can run the following command in your terminal:

```
python -m chatgpcontextmaker /path/to/input/directory -o /path/to/output/directory -f output_file_name
```
* `/path/to/input/directory`: The directory containing the files you want to concatenate

* `/path/to/output/directory`: The directory where the concatenated file will be saved (default: current working directory)

* `output_file_name`: The name of the output file (default: context)

If a file with the same name already exists in the output directory, the current datetime will be appended to the output file name to prevent overwriting.

### As a module

You can also use ChatGPTContextMaker as a module in your Python script:

```
from chatgpcontextmaker import concat_files_recursive

source_directory = "/path/to/input/directory"
output_directory = "/path/to/output/directory"
output_file_name = "output_file_name"

output_file_path = os.path.join(output_directory, output_file_name)

concat_files_recursive(source_directory, output_file_path)
```

Replace `/path/to/input/directory`, `/path/to/output/directory`, and `output_file_name` with the appropriate paths and file name for your use case. The `concat_files_recursive` function will concatenate the files from the input directory and its subdirectories and save the result in the specified output file.


## Extending ChatGPTContextMaker

You can extend the functionality of ChatGPTContextMaker by modifying the `__main__.py` script in the chatgpcontextmaker package.

To contribute to the project, simply fork the [GitHub repository](https://github.com/estill01/ChatGPContextMaker), make your changes, and submit a pull request.
