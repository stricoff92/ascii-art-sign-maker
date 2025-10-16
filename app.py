
# standard library imports
import argparse
import datetime as dt
from math import floor, ceil
import os
import sys

# 3rd party library imports
import numpy as np
from PIL import Image
from ascii_magic import AsciiArt, from_image

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

def get_out_file_chunk_name(start_ts: str, path_to_input_file: str, w_ix: int, h_ix: int):
    input_file_parts = path_to_input_file.split("/")
    input_file = input_file_parts[len(input_file_parts) - 1]
    input_file_root = input_file.split(".")[0]
    return os.path.join(get_out_directory(), f"{start_ts}-{input_file_root}-{w_ix}-{h_ix}.txt")

def get_out_file_full_img(start_ts: str, path_to_input_file: str):
    input_file_parts = path_to_input_file.split("/")
    input_file = input_file_parts[len(input_file_parts) - 1]
    input_file_root = input_file.split(".")[0]
    return os.path.join(get_out_directory(), f"{start_ts}-{input_file_root}-full.txt")


def transform_pixels_to_text(
    dryrun: bool,
    start_ts: str,
    path_to_file: str,
    columns: int,
    width_ratio: float,
    chars_per_page_width: int,
    chars_per_page_height: int
):
    aa = AsciiArt.from_image(path_to_file)
    text = aa.to_ascii(columns=columns, monochrome=True, width_ratio=width_ratio)
    if not dryrun:
        with open(get_out_file_full_img(start_ts, path_to_file), "w") as fp:
            fp.write(text)

    text_rows = text.split("\n")
    text_rows_count = len(text_rows)
    log_info(f"text rows {text_rows_count}")

    column_count_values = set()
    for row in text_rows:
        column_count_values.add(len(row))
    if len(column_count_values) != 1:
        raise Exception(f"column_count_values len is not 1: {column_count_values}")
    text_column_count = column_count_values.pop()
    log_info(f"text columns {text_column_count}")


    x_page_count = ceil(text_column_count / chars_per_page_width)
    y_page_count = ceil(text_rows_count / chars_per_page_height)
    log_info(f"pages count {x_page_count}x{y_page_count}")

    for page_y in range(y_page_count):
        row_start_ix = page_y * chars_per_page_height
        for page_x in range(x_page_count):
            chunk_rows = []
            col_start_ix = page_x * chars_per_page_width
            for row_ix in range(chars_per_page_height):
                try:
                    chunk_rows.append(text_rows[row_start_ix + row_ix][col_start_ix: col_start_ix+chars_per_page_width])
                except IndexError:
                    pass
            if dryrun:
                continue
            out_name = get_out_file_chunk_name(start_ts, path_to_file, page_x, page_y)
            with open(out_name, "w") as fp:
                for r in chunk_rows:
                    fp.write(r + "\n")


def parse_args():
    parser = argparse.ArgumentParser(description="ASCII Art Sign Maker")
    parser.add_argument("path_to_file", type=str, help="Full path to input image")
    parser.add_argument("columns", type=int)
    parser.add_argument("width_ratio", type=float)
    parser.add_argument("chars_per_page_width", type=int)
    parser.add_argument("chars_per_page_height", type=int)
    parser.add_argument('-d', '--dryrun', action='store_true', help="Calculate meta data but don't create any files")
    return parser.parse_args()

def app():
    start_ts = dt.datetime.now().isoformat()
    log_info("script starting")
    args = parse_args()
    log_debug(f"arg: path_to_file: {args.path_to_file}")
    log_debug(f"arg: columns: {args.columns}")
    log_debug(f"arg: width_ratio: {args.width_ratio}")
    log_debug(f"arg: chars_per_page_width: {args.chars_per_page_width}")
    log_debug(f"arg: chars_per_page_height: {args.chars_per_page_height}")
    log_debug(f"arg: dryrun {args.dryrun}")

    transform_pixels_to_text(
        args.dryrun,
        start_ts,
        args.path_to_file,
        args.columns,
        args.width_ratio,
        args.chars_per_page_width,
        args.chars_per_page_height,
    )


if __name__ == "__main__":
    # App Entry Point
    app()
    sys.exit(0)

