
import argparse
import datetime as dt

# Loggers
def log(msg: str, level):
    print(f"[{level}] [{dt.datetime.now().isoformat()}] - {msg}")
def log_debug(msg: str):
    log(msg, "DEBUG")
def log_info(msg: str):
    log(msg, "INFO")
def log_warn(msg: str):
    log(msg, "WARN")
def log_err(msg: str):
    log(msg, "ERR")




# App Entry Point

def parse_args():
    parser = argparse.ArgumentParser(description="ASCII Art Sign Maker")
    parser.add_argument("path_to_file", type=str, help="Full path to input image")
    parser.add_argument("pixels_per_char", type=int, help="Number of pixels (width and height) per character")
    parser.add_argument("chars_per_page_width", type=int, help="Number of character columns per page")
    parser.add_argument("chars_per_page_height", type=int, help="Number of character rows per page")
    return parser.parse_args()


def app():
    log_info("script starting")

    args = parse_args()
    log_debug(f"path_to_file: {args.path_to_file}")
    log_debug(f"pixels_per_char: {args.pixels_per_char}")
    log_debug(f"chars_per_page_width: {args.chars_per_page_width}")
    log_debug(f"chars_per_page_height: {args.chars_per_page_height}")

if __name__ == "__main__":
    app()
