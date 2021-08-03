from argparse import ArgumentParser
from typing import List, Generator
from photo_tagger.operations.factory import OperationFactory
import os
import logging

parser = ArgumentParser(description="Script for categorizing directories of image files by writing their filenames to text files corresponding to their classifications.")
parser.add_argument(
    "directories",
    type=str,
    nargs="+",
    help="The directories to process.",
)
parser.add_argument(
    "--aspect_ratio",
    action="store_true",
    help="Enable categorization of items by aspect ratio."
)
parser.add_argument(
    "--output",
    help="Where to output the metadata files to.  Defaults to each of the directories provided."
)
parser.add_argument(
    "-v",
    help="The output verbosity to use.  More v's to increase the verbosity."
)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

supported_extensions = {".jpg", ".jpeg", ".png"}

def get_file_count(dirs: list) -> int:
    count = 0
    for dir_arg in dirs:
        for file in os.scandir(dir_arg):
            if not file.is_file():
                continue

            _trimmed_path, extension = os.path.splitext(file.path)
            if extension not in supported_extensions:
                continue

            count += 1

    return count

def get_files(dirs: list) -> Generator[str, None, None]:
    for dir_arg in dirs:
        for file in os.scandir(dir_arg):
            if not file.is_file():
                continue

            _trimmed_path, extension = os.path.splitext(file.path)
            if extension not in supported_extensions:
                continue

            yield file.path

args = parser.parse_args()
factory = OperationFactory()

# Get file counts
num_files = get_file_count(args.directories)
logger.info(f"Found {num_files} files to process.")

# Create operations
operations = factory.gather_operations(vars(args))

# Process files
for file in get_files(args.directories):
    for operation in operations:
        logger.info(f"Running {operation.name}")
        pass

