import os

# Application metadata
APP_VERSION = "1.0.0"
APP_PUBLISHER = "Luke Deaves"
APP_NAME = "National Rail Data Downloader"
APP_SERIAL = f"{APP_NAME} {APP_VERSION}"
CONFIG_DIR = os.path.join('~/Documents', APP_PUBLISHER, APP_NAME) # os.getenv('APPDATA')