# FlashAir Tethered

FlashAir Tethered allows you to shoot tethered with your digital camera (i.e. shoot & view) using the Toshiba FlashAir WiFi SD-Card.

It scans your FlashAir SD-Card for new JPEG files periodically while you shoot and displays new pictures automatically on your computer. 

I created this tool to give me tethered shooting capabilities using my Fuji X-T10. It should however work with almost any digital camera which uses the Toshiba FlashAir SD-Card.

## Requirements

FlashAir Tethered is written in python, so you need a python interpreter to be installed on your system.

Tested on macOS and Windows, but should work on Linux as well (to use it on Linux an image viewer command needs to be added to the config).

## Installation

### Linux // macOS
```
virtualenv pyenv
pyenv/bin/pip install -r requirements.txt
```

### Windows
```
virtualenv pyenv
pyenv\Scripts\pip install -r requirements.txt
```

## Configuration

The tool should work out of the box using the default configuration. Adjustments can be made in the file `config.py`.  

## Start

Make sure you are connected to the FlashAir network. Also make sure you're still inside your virtualenv.

To start scanning for new files on your SD card (and download and display them of course), execute:

### Linux // macOS
```
pyenv/bin/python src\tethered.py
```

### Windows

```
pyenv\Scripts\python.exe src\tethered.py
```

Now pick your camera and shoot. Wait a few seconds for the pictures to be downloaded and displayed on your screen.
All pictures are downloaded to the `pics/` folder by default.
