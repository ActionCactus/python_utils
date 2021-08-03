from argparse import ArgumentParser
from typing import List, Generator

from progressbar.bar import ProgressBar
from photo_tagger.operations.factory import OperationFactory
import progressbar
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

# Allow the progress bar to remain in a stationary location on screen
progressbar.streams.wrap_stderr()
progressbar.streams.wrap_stdout()

# Configure global loggers
logging.basicConfig(level=logging.INFO)
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
print(args)
factory = OperationFactory()

# Get file counts
num_files = get_file_count(args.directories)
logger.info(f"Found {num_files} files to process.")

# Create operations
operations = factory.gather_operations(vars(args))

# Process files
with progressbar.ProgressBar(max_value=num_files) as progress_bar:
    idx = 0
    for file in get_files(args.directories):
        for operation in operations:
            operation.process_file(file)
        progress_bar.update(idx)
        idx += 1

for operation in operations:
    results: dict = operation.gather_results()
    for filename, lines in results.items():
        file_path = "%s/%s.txt" % (args.output, filename)
        with open(file_path, "w") as fh:
            fh.write("\n".join(lines))
            logger.info(f"{len(lines)} files tagged in {file_path}")
