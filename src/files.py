import sys
import time


def check_file(args):
    # get file path from args, if none, exit
    if len(args) < 2:
        print('Please specify file path')
        sys.exit(0)
    file_path = sys.argv[1]
    if file_path == '':
        print('Please specify file path')
        sys.exit(0)

    # if file doesn't exist, exit
    try:
        file = open(file_path, 'r')
        file.close()
    except FileNotFoundError:
        print('File does not exist')
        sys.exit(0)


def wait_new_file_size(path):
    file = open(path, 'r')
    initial_size = len(file.read())
    file.close()

    while True:
        with open(path, 'r') as f:
            new_size = len(f.read())
            if initial_size != new_size:
                print(f'File {path} changed')
                break
        time.sleep(0.5)
