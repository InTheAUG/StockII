import sys
import os
from pathlib import Path
from stock import paths

if __name__ == "__main__":
    assert 'linux' in sys.platform
    os.mkdir(paths.DATA_BASEPATH)
    os.mkdir(paths.STOCKFILES)

