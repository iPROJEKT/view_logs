import logging

from app.core.app import MyApp
from app.const import (
    LOG_FORM,
    LOG_FILEMOD,
    LOG_FILENAME,
)


logger = logging.getLogger(__name__)


def main() -> None:
    app = MyApp()
    app.run()


if __name__ == '__main__':
    logging.basicConfig(
        format=LOG_FORM,
        filemode=LOG_FILEMOD,
        filename=LOG_FILENAME,
        level=logging.INFO,
    )
    main()

