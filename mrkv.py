import os
import re
import sys
import platform
import time
import tkinter as tk

from langchain.schema import (
    HumanMessage,
)

from models import openai_chat


# function which controls if text file changed
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


def send_info_message(message):
	def close_window():
		time.sleep(0.1)
		window.destroy()
	# Create the main window
	window = tk.Tk()
	window.title("MRKV: file updated")

	# Create a frame for better layout
	frame = tk.Frame(window, padx=20, pady=20)
	frame.pack()

	# Get OS information
	os_label = tk.Label(frame, text=message, font=("Helvetica", 14))
	os_label.pack(pady=10)

	# Create a button to close the window
	close_button = tk.Button(frame, text="Ok", command=close_window)
	close_button.pack()

	# Run the GUI main loop
	window.mainloop()


if __name__ == "__main__":
	# get file path from args, if none, exit
	if len(sys.argv) < 2:
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

	i = 0
	while True:
		if i >= 2:
			break
		wait_new_file_size(file_path)
		with open(file_path, 'r') as f:
			text = f.read()

		# get all groups of text between #mrkv and #end, using regex groups
		matches = re.findall(r'(#mrkv(.*?)#end)', text, re.DOTALL)
		# if there are matches
		for i, match in enumerate(matches):
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
				file_tail = file_text[prompt_end+4:]

				# delete text from file
				f.seek(0)
				f.truncate()

				f.write(file_head)
				f.write('"""\n')
				file.close()

				with open(file_path, 'a') as f:
					try:
						response = openai_chat([HumanMessage(content=prompt)])
						print(response)
						# write in place of match
						f.write(response.content)
					except Exception as e:
						print(e)
					f.write('\n"""')
					f.write(file_tail)
				os.utime(file_path, None)

			# send os message that file changed now
			send_info_message("file {} changed".format(file_path))
			print("finished")
		i += 1
