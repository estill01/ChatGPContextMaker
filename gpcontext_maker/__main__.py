#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import argparse
import fnmatch
from datetime import datetime
from pathlib import Path
import pyperclip

def read_ignore_patterns(ignore_file):
    with open(ignore_file, "r") as f:
        patterns = [line.strip() for line in f.readlines()]
    return patterns

def save_ignore_patterns(ignore_file, patterns):
    with open(ignore_file, "w") as f:
        for pattern in patterns:
            f.write(pattern + "\n")

def concat_files_recursive(input_dir, output_file, ignore_patterns=None):
    if ignore_patterns is None:
        ignore_patterns = []

    with open(output_file, "w") as outfile:
        for root, dirs, files in os.walk(input_dir):
            dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d, pattern) for pattern in ignore_patterns)]

            for file in files:
                if any(fnmatch.fnmatch(file, pattern) for pattern in ignore_patterns):
                    continue

                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, input_dir)

                delimiter = f"\n{'#' * 80}\n# File: {relative_path}\n{'#' * 80}\n\n"
                outfile.write(delimiter)

                with open(file_path, "r") as infile:
                    content = infile.read()
                    outfile.write(content)
                    outfile.write("\n\n")


def main():
    parser = argparse.ArgumentParser(description="Concatenate files from a directory into a single file.")
    parser.add_argument("input_dir", help="The input directory to concatenate.")
    parser.add_argument("-c", "--clipboard", action="store_true", default=True, help="Copy the concatenated file content to the clipboard (default: True).")
    parser.add_argument("-i", "--ignore-file", help="A custom ignore file with patterns to ignore.", default=None)
    parser.add_argument("-l", "--list-ignore", action="store_true", help="List current ignore patterns.")
    parser.add_argument("-a", "--add-ignore", nargs="+", help="Add patterns to ignore.")
    parser.add_argument("-r", "--remove-ignore", nargs="+", help="Remove patterns from ignore list.")
    parser.add_argument("-m", "--merge-default", action="store_true", help="Merge the default ignore file with the .gpcontext_ignore file.")
    parser.add_argument("-f", "--force-custom", action="store_true", help="Force using only the custom ignore file.")
    args = parser.parse_args()

    input_dir = args.input_dir

    output_filename = "context_{}.txt".format(datetime.now().strftime("%Y%m%d_%H%M%S"))
    output_file = Path.cwd() / output_filename

    default_ignore_file = os.path.join(os.path.dirname(__file__), "default_gpcontext_ignore.txt")
    user_ignore_file = args.ignore_file or ".gpcontext_ignore"

    if os.path.isfile(default_ignore_file):
        default_patterns = read_ignore_patterns(default_ignore_file)
    else:
        print(f"Default ignore file '{default_ignore_file}' not found. No patterns will be ignored.")
        default_patterns = []

    user_patterns = []
    if os.path.isfile(user_ignore_file):
        user_patterns = read_ignore_patterns(user_ignore_file)

    if args.merge_default:
        user_patterns = list(set(user_patterns + default_patterns))
        save_ignore_patterns(user_ignore_file, user_patterns)

    if args.force_custom:
        ignore_patterns = user_patterns
    else:
        ignore_patterns = list(set(default_patterns + user_patterns))

    if args.list_ignore:
        print("Ignore patterns:")
        for pattern in ignore_patterns:
            print(f"  - {pattern}")
        return

    if args.add_ignore:
        user_patterns.extend(args.add_ignore)
        save_ignore_patterns(user_ignore_file, user_patterns)

    if args.remove_ignore:
        user_patterns = [pattern for pattern in user_patterns if pattern not in args.remove_ignore]
        save_ignore_patterns(user_ignore_file, user_patterns)

    if args.clipboard:
        with open(output_file, "r") as outfile:
            file_content = outfile.read()
            pyperclip.copy(file_content)
            print("The concatenated file content has been copied to the clipboard.")

    concat_files_recursive(input_dir, output_file, ignore_patterns)

if __name__ == "__main__":
    main()


