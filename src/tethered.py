import os
import time
import logging

from requests.exceptions import ConnectionError

from flashair_api import FlashairAPI

HOST = '192.168.0.1'

SCAN_FREQUENCY = 3
RETRY_FREQUENCY = 1
TARGET_DIR = 'pics'
OPEN_FULLSCREEN = True
LOGLEVEL = logging.DEBUG

logger = logging.getLogger(__name__)


def open_preview(filename, fullscreen=False):
    logger.debug('opening preview for %s...' % filename)
    os.popen(
        'open -a Preview "%s";' % filename + ('' if fullscreen is False else '/usr/bin/osascript -e \'tell application "Preview"\' -e "activate" -e \'tell application "System Events"\' -e \'keystroke "f" using {control down, command down}\' -e "end tell" -e "end tell"'))
    logger.debug('preview opened.')


if __name__ == "__main__":
    logging.basicConfig(level=LOGLEVEL,
                        format='%(asctime)s %(levelname)s %(message)s')

    flashair = FlashairAPI(host=HOST, target_dir=TARGET_DIR)

    while True:
        try:
            if flashair.has_updates():
                updated_files = flashair.get_updates()
                for filename in updated_files:
                    flashair.download_file(filename)
                    open_preview(os.path.abspath('%s%s' % (TARGET_DIR, filename)), OPEN_FULLSCREEN)

        except ConnectionError, e:
            logger.error('flashair connection error. are you connected to your flashiar wifi network?')
            time.sleep(RETRY_FREQUENCY)
            continue

        time.sleep(SCAN_FREQUENCY)


