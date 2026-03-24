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
from app.ui_utils import print_logo, print_info, Colors

def main():
    # Приветственное сообщение
    print_logo()
    print_info("Запуск приложения...")
    print()
    
    app = Application()
    app.run()

if __name__ == "__main__":
    main()