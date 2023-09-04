import logging

from src.files import *
from src.io import *
from src.utils import *


def routine(fp, log):
    log.info("Merkava started")
    i = 0

    while True:
        wait_new_file_size(fp, log)
        make_file_copy(fp, log)
        try:
            parse_and_exec_mrkv_commands(fp, log)
        except Exception as e:
            log.error(e)
            recover_file(fp, log)
            break

        # send os message that file changed now
        delete_file_copy(fp, log)
        log.info(f"{GREEN}File {fp} changed{WHITE}")
        i += 1

    log.info("Merkava finished")


if __name__ == "__main__":
    # logger to stdout
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s mrkv: %(message)s',)
    log = logging.getLogger()

    check_file(sys.argv, log)
    file_path = sys.argv[1]

    routine(file_path, log)

