import logging

# the flashair SD card IP address, usually no need to change
FLASHAIR_HOST = '192.168.0.1'

# how often do you want to scan for new files (in seconds)?
SCAN_FREQUENCY = 3

# in case something goes wrong, how long to wait for a retry (in seconds)?
RETRY_FREQUENCY = 1

# folder to store your images in. can be relative or absolute.
IMAGE_TARGET_DIR = 'pics'

# logging verbosity
LOGLEVEL = logging.DEBUG

# commands to launch and exit image viewer application
IMAGE_VIEWER_COMMANDS = {
    'Windows': {
        'start': 'start "" /max %(image_file_path)s',       # lets windows decide which application to launch
        'close': 'taskkill /IM i_view64.exe'                 # optional. how to close image viewer window. Change or remove if you use a different application than IrfanViewer.
    },
    'Darwin': {
        'start': 'open -a Preview "%(image_file_path)s"; /usr/bin/osascript -e \'tell application "Preview"\' -e "activate" -e \'tell application "System Events"\' -e \'keystroke "f" using {control down, command down}\' -e "end tell" -e "end tell"',
        'close': 'killall Preview'
    },
    'Linux': {
        'start': 'eog -w "%(image_file_path)s"',            # default image viewer for GNOME, -w opens images in single window
#        'close': 'killall eog'
}
