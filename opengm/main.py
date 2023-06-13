import logging
from sys import exit

from opengm.__init__ import LOG_LEVEL

from .opengm import Opengm

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.getLevelName(LOG_LEVEL),
)


def main():
    try:
        if __name__ == "__main__":
            Opengm().run()

    except KeyboardInterrupt:
        exit()
