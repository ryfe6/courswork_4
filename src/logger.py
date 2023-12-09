import logging
from typing import Any


def setup_logging() -> Any:
    logging.basicConfig(
        level=logging.DEBUG,
        filename="my_logging.log",
        format="%(levelname)s, (%(asctime)s): %(message)s " "Line %(lineno)d) [%(filename)s]",
        datefmt="%d/%m/%Y %I:%M:%S",
        encoding="utf-8",
        filemode="w",
    )
    return logging.getLogger()
