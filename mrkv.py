import sys

from src.files import check_file, wait_new_file_size
from src.io import get_all_mrkv_commands, elaborate_mrkv_commands
from src.messages import send_info_message


def routine(fp):
    print("Merkava started")
    i = 0
    while True:
        wait_new_file_size(fp)
        cmds = get_all_mrkv_commands(fp)
        try:
            elaborate_mrkv_commands(cmds, fp)
        except Exception as e:
            print(e)
            break

        # send os message that file changed now
        send_info_message("file {} changed".format(fp))
        print(f"{i} - completion finished")
        i += 1

    print("Merkava finished")


if __name__ == "__main__":
    check_file(sys.argv)
    file_path = sys.argv[1]

    routine(file_path)

