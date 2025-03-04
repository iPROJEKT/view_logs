import logging

from app.core.logic import LogicApp
from app.core.tools.const import (
    LOG_FORM,
    LOG_FILEMOD,
    LOG_FILENAME,
)
from app_ref.sceen_manager import ScreenManager

logger = logging.getLogger(__name__)


def main() -> None:
    app = ScreenManager()
    app.run()


if __name__ == '__main__':
    logging.basicConfig(
        format=LOG_FORM,
        filemode=LOG_FILEMOD,
        filename=LOG_FILENAME,
        level=logging.INFO,
    )
    main()

