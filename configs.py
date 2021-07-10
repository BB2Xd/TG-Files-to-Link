import os

class Config(object):
    JTU_ENABLE = os.environ.get("JTU_ENABLE", True)
