
# standard library imports
import argparse
import datetime as dt
from math import floor, ceil
import os
import sys

# 3rd party library imports
import numpy as np
from PIL import Image

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def log(msg: str, level):
    if len(level) > 6:
        raise Exception(f"level {level} has too many characters")
    padded_level = level + (" " * (6 - len(level)))
    print(f"[{padded_level}] [{dt.datetime.now().isoformat()}] - {msg}")
def log_debug(msg: str):
    log(msg, "DEBUG")
def log_info(msg: str):
    log(msg, "INFO")
def log_warn(msg: str):
    log(msg, "WARN")
def log_err(msg: str):
    log(msg, "ERR")



def get_out_directory():
    parent = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(parent, "outputs")
def get_out_file_name(start_ts: str, path_to_input_file: str, w_ix: int, h_ix: int):
    input_file_parts = path_to_input_file.split("/")
    input_file = input_file_parts[len(input_file_parts) - 1]
    input_file_root = input_file.split(".")[0]
    return os.path.join(get_out_directory(), f"{start_ts}-{input_file_root}-{w_ix}-{h_ix}.txt")


def get_chunk(
    frame: np.ndarray, x1: int, x2: int, y1: int, y2: int):
    return frame[y1:y2, x1:x2]

def transform_pixels_to_text(
    im,
    width_pixels_per_char: int,
    height_pixels_per_char: int,
    chars_per_page_width: int,
    chars_per_page_height: int
):
    img_w, img_h = im.size
    log_debug(f"img dims: {img_w}x{img_h}")

    full_chars_count_width = img_w / width_pixels_per_char
    full_chars_count_height = img_h / height_pixels_per_char
    log_debug(f"sign char count dims {full_chars_count_width}x{full_chars_count_height}")

    page_count_width = ceil(full_chars_count_width / chars_per_page_width)
    page_count_height = ceil(full_chars_count_height / chars_per_page_height)
    log_debug(f"sign page counts {page_count_width}x{page_count_height}")

    frame = np.asarray(im)

    for page_ix_w in range(page_count_width):
        for page_ix_h in range(page_count_height):
            log_info(f"preparing page ({page_ix_w}, {page_ix_h})")



def parse_args():
    parser = argparse.ArgumentParser(description="ASCII Art Sign Maker")
    parser.add_argument("path_to_file", type=str, help="Full path to input image")
    parser.add_argument("width_pixels_per_char", type=int, help="Number of pixels (width) per character")
    parser.add_argument("height_pixels_per_char", type=int, help="Number of pixels (width) per character")
    parser.add_argument("chars_per_page_width", type=int, help="Number of character columns per page")
    parser.add_argument("chars_per_page_height", type=int, help="Number of character rows per page")
    parser.add_argument('-d', '--dryrun', action='store_true', help="Calculate meta data but don't create any files")
    return parser.parse_args()

def app():
    start_ts = dt.datetime.now().isoformat()
    log_info("script starting")
    args = parse_args()
    log_debug(f"path_to_file: {args.path_to_file}")
    log_debug(f"width_pixels_per_char: {args.width_pixels_per_char}")
    log_debug(f"height_pixels_per_char: {args.height_pixels_per_char}")
    log_debug(f"chars_per_page_width: {args.chars_per_page_width}")
    log_debug(f"chars_per_page_height: {args.chars_per_page_height}")

    im = Image.open(args.path_to_file)
    text_generator = transform_pixels_to_text(
        im,
        args.width_pixels_per_char,
        args.height_pixels_per_char,
        args.chars_per_page_width,
        args.chars_per_page_height
    )

    if args.dryrun:
        log_debug("dryrun, program exiting now")
        sys.exit(0)
        return

    for ix, text in enumerate(text_generator):
        out_file = get_out_file_name(start_ts, args.path_to_file, ix)
        with open(out_file, "w") as fp:
            fp.write(text)
            log_info(f"{len(text)} chars written to {out_file}")

if __name__ == "__main__":
    # App Entry Point
    app()
    sys.exit(0)

