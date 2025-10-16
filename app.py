
import datetime as dt
import sys


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
def app():
    log_info("script starting")

if __name__ == "__main__":
    app()
