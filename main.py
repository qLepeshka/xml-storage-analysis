import os
import sys

mpl_cache_dir = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Temp', 'matplotlib_cache')
try:
    os.makedirs(mpl_cache_dir, exist_ok=True)
except FileExistsError:
    pass

os.environ['MPLCONFIGDIR'] = mpl_cache_dir

import matplotlib
matplotlib.use('Agg')

from app.application import Application

def main():
    config_file = None
    if len(sys.argv) > 1:
        config_file = sys.argv[1]

    app = Application(config_file)
    app.run()

if __name__ == "__main__":
    main()