import re

from langchain.schema import HumanMessage

from src.models import openai_chat


def get_all_mrkv_commands(file_path):
    with open(file_path, 'r') as f:
        text = f.read()
    # get all groups of text between #mrkv and #end, using regex groups
    return re.findall(r'(#mrkv(.*?)#end)', text, re.DOTALL)


def elaborate_mrkv_commands(commands, file_path):
    for i, match in enumerate(commands):
        # get last group of text
        prompt = match[1]

        # response = '"""'
        # get response from openai in stream mode
        f = open(file_path, 'r+')
        file_text = f.read()
        # where starts the first prompt
        prompt_start = file_text.find("#mrkv")
        # where ends the first prompt
        prompt_end = file_text.find("#end")

        if prompt_start != -1 and prompt_end != -1:
            # delete prompt from file
            file_head = file_text[:prompt_start]
            file_tail = file_text[prompt_end + 4:]

            # delete text from file
            f.seek(0)
            f.truncate()

            f.write(file_head)
            f.write('"""\n')
            f.close()

            with open(file_path, 'a') as f:
                try:
                    response = openai_chat([HumanMessage(content=prompt), HumanMessage(content=prompt)])
                    print(response)
                    # write in place of match
                    f.write(response.content)
                except Exception as e:
                    f.write('\n"""')
                    f.write(file_tail)
                    raise e
