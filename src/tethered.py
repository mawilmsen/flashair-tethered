import os
import sys
import time
import logging
import platform

from requests.exceptions import ConnectionError
from requests.exceptions import ReadTimeout

from config import IMAGE_VIEWER_COMMANDS
from config import LOGLEVEL
from config import FLASHAIR_HOST
from config import IMAGE_TARGET_DIR
from config import RETRY_FREQUENCY
from config import SCAN_FREQUENCY

from flashair_api import FlashairAPI


logger = logging.getLogger(__name__)


def open_image_viewer(filename, _platform):
    if _platform not in IMAGE_VIEWER_COMMANDS:
        logger.error('no image viewer configured for platform %s' % _platform)
        return

    if 'close' in IMAGE_VIEWER_COMMANDS[_platform]:
        os.popen(IMAGE_VIEWER_COMMANDS[_platform]['close'])

    os.popen(IMAGE_VIEWER_COMMANDS[_platform]['start'] % {'image_file_path': filename})


if __name__ == "__main__":
    logging.basicConfig(level=LOGLEVEL,
                        format='%(asctime)s %(levelname)s %(message)s')

    _platform = platform.system()
    logger.info('detected platform: %s' % _platform)

    if _platform not in IMAGE_VIEWER_COMMANDS:
        logger.error('no image viewer configured for platform %s' % _platform)
        sys.exit(1)

    flashair = FlashairAPI(host=FLASHAIR_HOST, target_dir=IMAGE_TARGET_DIR)

    while True:
        try:
            if flashair.has_updates():
                updated_files = flashair.get_updates()
                for filename in updated_files:
                    flashair.download_file(filename)
                    open_image_viewer(os.path.abspath('%s%s' % (IMAGE_TARGET_DIR, filename)), _platform)

        except ConnectionError:
            logger.error('flashair connection error.')
            time.sleep(RETRY_FREQUENCY)
            continue
        except ReadTimeout:
            logger.error('flashair timeout error.')
            time.sleep(RETRY_FREQUENCY)
            continue

        time.sleep(SCAN_FREQUENCY)
