import sys
from app.application import Application

def main():
    config_file = None
    if len(sys.argv) > 1:
        config_file = sys.argv[1]

    app = Application(config_file)
    app.run()

if __name__ == "__main__":
    main()