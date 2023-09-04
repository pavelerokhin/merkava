from langchain.schema import AIMessage, HumanMessage

from src.models import openai_chat
from src.utils import *


def parse_and_exec_mrkv_commands(file_path, log):
    i = 0
    file_tail = ""
    while True:
        f = open(file_path, 'r+')
        try:
            file_text = f.read()

            # where starts the first prompt
            prompt_start = file_text.find("#mrkv")
            # where ends the first prompt
            prompt_end = file_text.find("#end")

            if prompt_start == -1 or prompt_end == -1:
                log.info(f"{GREY}finished parse and exec {i} commands{WHITE}")
                break
            i += 1
            log.info(f"{GREY}parsing and executing command {i}{WHITE}")

            # delete prompt from file
            file_head = file_text[:prompt_start]
            file_tail = file_text[prompt_end + 4:]
            prompt = file_text[prompt_start + 5:prompt_end]

            # delete text from file
            f.seek(0)
            f.truncate()

            f.write(file_head)
            f.write('"""\n')

            response = openai_chat([AIMessage(content=file_head), HumanMessage(content=prompt)])
            log.info("OPENAI response: " + response.content)
            f.write(response.content)
            f.write('\n"""')
            f.write(file_tail)
        except Exception as e:
            raise e
        finally:
            f.close()
