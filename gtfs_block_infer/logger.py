
from rich.console import Console
from rich.logging import RichHandler
import logging

def get_logger(name="gtfs_block_infer"):
    console = Console()
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = RichHandler(console=console, markup=True)
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    return logger
