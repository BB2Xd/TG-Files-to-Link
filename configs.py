import os

class Config(object):
    JTU_ENABLE = os.environ.get("JTU_ENABLE", True)
    CHANNEL_USERNAME = os.environ.get("CHANNEL_USERNAME", None)
