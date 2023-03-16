#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

def concat_files_recursive(directory, output_file):
    with open(output_file, 'w') as outfile:
        for root, _, files in os.walk(directory):
            for file in files:
                if file != os.path.basename(output_file):
                    filepath = os.path.join(root, file)
                    relative_path = os.path.relpath(filepath, directory)
                    
                    delimiter = f"\n{'#' * 80}\n# File: {relative_path}\n{'#' * 80}\n\n"
                    outfile.write(delimiter)
                    
                    with open(filepath, 'r') as infile:
                        outfile.write(infile.read())
                        outfile.write('\n\n')

def main():
    parser = argparse.ArgumentParser(description='Concatenate files in a directory and its subdirectories into a single file.')
    parser.add_argument('source_directory', help='The directory containing files to concatenate')
    parser.add_argument('-o', '--output', help='Output directory (default: current directory)', default=os.getcwd())
    parser.add_argument('-f', '--file', help='Output file name (default: context)', default='context')

    args = parser.parse_args()

    source_directory = args.source_directory
    output_directory = args.output
    output_file_name = args.file

    output_file_path = os.path.join(output_directory, output_file_name)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    if os.path.isfile(output_file_path):
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file_name = f"{output_file_name}_{now}"
        output_file_path = os.path.join(output_directory, output_file_name)

    concat_files_recursive(source_directory, output_file_path)

if __name__ == '__main__':
    main()
