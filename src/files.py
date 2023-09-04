import os
import shutil
import sys
import time


def check_file(args, log):
    # get file path from args, if none, exit
    if len(args) < 2:
        log.error('Please specify file path')
        sys.exit(0)
    file_path = sys.argv[1]
    if file_path == '':
        log.error('Please specify file path')
        sys.exit(0)
    # if file doesn't exist, exit
    try:
        file = open(file_path, 'r')
        file.close()
    except FileNotFoundError:
        log.error('File does not exist')
        sys.exit(0)


def delete_file_copy(file_path, log):
    os.remove(file_path + '.copy')
    log.info(f'File {file_path}, copy deleted')


def make_file_copy(file_path, log):
    shutil.copyfile(file_path, file_path + '.copy')
    log.info(f'File {file_path}, reserved copy')


def recover_file(file_path, log):
    shutil.copyfile(file_path + '.copy', file_path)
    delete_file_copy(file_path, log)
    log.info(f'File {file_path} recovered from the copy')


def wait_new_file_size(path, log):
    file = open(path, 'r')
    initial_size = len(file.read())
    file.close()

    while True:
        with open(path, 'r') as f:
            new_size = len(f.read())
            if initial_size != new_size:
                log.info(f'File {path} changed')
                break
        time.sleep(0.5)
