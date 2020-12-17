#!/usr/bin/python3

import argparse
from pytube import YouTube
from pytube.streams import Stream
from console import bg


def get_configured_destination():
    return "."


def clean_vid_title(title: str):
    return title.replace(" ", "_")


def download_progress_callback(stream: Stream, chunk: bytes, bytes_remaining: int):
    percent_complete = (stream.filesize - bytes_remaining) / stream.filesize
    percent_complete_adj = percent_complete * 100
    rounded_percent_complete = round(percent_complete_adj, 2)
    end = "\r" if (rounded_percent_complete < 100) else "\n"
    print(f"Downloading...{rounded_percent_complete}%", end=end)


URLS_ARG = "urls"
DESTINATION_ARG = "to"

arg_parser = argparse.ArgumentParser(description="Download Youtube videos!")
arg_parser.add_argument(
    f"{URLS_ARG}",
    nargs="+",
    help="A space-delimited list of URLs containing videos to download.",
)
arg_parser.add_argument(
    f"--{DESTINATION_ARG}",
    help="The destination directory in which these videos should be saved.",
)


inputs = arg_parser.parse_known_args()[0].__dict__
urls = inputs[URLS_ARG]
destination = inputs.get(DESTINATION_ARG, get_configured_destination())

err = False
for url in urls:
    try:
        handle = YouTube(url, on_progress_callback=download_progress_callback)
        handle.prefetch()

        print(f"Downloading '{handle.title}' by '{handle.author}'")

        cleaned_title = clean_vid_title(handle.title)
        stream = handle.streams.get_highest_resolution()

        if not stream:
            raise Exception(f"No download stream could be located!")

        stream.download(output_path=destination, filename=cleaned_title)
    except Exception as e:
        err = True
        print(f"{bg.red}Issue while downloading {url}: {e}{bg.default}")

exit_code = 1 if err else 0
quit(exit_code)
