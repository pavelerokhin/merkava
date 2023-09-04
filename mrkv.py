import logging
import sys

from src.files import wait_new_file_size, make_file_copy, delete_file_copy, recover_file, check_file
from src.io import exec_commands_to_file
from src.utils import WHITE, GREEN, GREY


def routine(fp, log):
    log.info("Merkava started")

    while True:
        wait_new_file_size(fp, log)
        make_file_copy(fp, log)
        try:
            exec_commands_to_file(fp, log)
        except Exception as e:
            log.error(e)
            recover_file(fp, log)
            break

        # send os message that file changed now
        delete_file_copy(fp, log)
        log.info(f"{GREEN}File {fp} ready {WHITE}")
    log.info(f"{GREY}Merkava finished{WHITE}")


if __name__ == "__main__":
    # logger to stdout
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s mrkv: %(message)s',)
    log = logging.getLogger()

    check_file(sys.argv, log)
    file_path = sys.argv[1]

    # TODO: do routine as a background process
    routine(file_path, log)
