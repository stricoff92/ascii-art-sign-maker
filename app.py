
# standard library imports
import argparse
import datetime as dt
import os

# 3rd party library imports
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

def get_out_file_name(start_ts: str, path_to_input_file: str, ix: int):
    input_file_parts = path_to_input_file.split("/")
    input_file = input_file_parts[len(input_file_parts) - 1]
    input_file_root = input_file.split(".")[0]
    return os.path.join(get_out_directory(), f"{start_ts}-{input_file_root}-{ix}.txt")



def transform_pixels_to_text(
    im,
    pixels_per_char: int,
    chars_per_page_width: int,
    chars_per_page_height: int
):
    pass



def parse_args():
    parser = argparse.ArgumentParser(description="ASCII Art Sign Maker")
    parser.add_argument("path_to_file", type=str, help="Full path to input image")
    parser.add_argument("pixels_per_char", type=int, help="Number of pixels (width and height) per character")
    parser.add_argument("chars_per_page_width", type=int, help="Number of character columns per page")
    parser.add_argument("chars_per_page_height", type=int, help="Number of character rows per page")
    return parser.parse_args()

def app():
    start_ts = dt.datetime.now().isoformat()
    log_info("script starting")
    args = parse_args()
    log_debug(f"path_to_file: {args.path_to_file}")
    log_debug(f"pixels_per_char: {args.pixels_per_char}")
    log_debug(f"chars_per_page_width: {args.chars_per_page_width}")
    log_debug(f"chars_per_page_height: {args.chars_per_page_height}")

    im = Image.open(args.path_to_file)
    pix = im.load()
    log_info(f"image size: {im.size}")

    text_generator = transform_pixels_to_text(im, args.pixels_per_char, args.chars_per_page_width, args.chars_per_page_height)
    for ix, text in enumerate(text_generator):
        out_file = get_out_file_name(start_ts, args.path_to_file, ix)
        with open(out_file, "w") as fp:
            fp.write(text)
            log_info(f"{len(text)} chars written to {out_file}")

if __name__ == "__main__":
    # App Entry Point
    app()
