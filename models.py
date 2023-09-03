import os

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings

# take environment variable OPENAI_API_KEY
key = os.environ.get("OPENAI_API_KEY")
if not key:
    # take key from file
    with open("OPENAI_API_KEY", "r") as f:
        key = f.read()

if not key:
    raise ValueError("Please add your OpenAI API key to the file OPENAI_API_KEY")

# initialize the models

# ada_embeddings = OpenAIEmbeddings(
#     openai_api_key=key
# )

# openai = OpenAI(
#     model_name="gpt-3.5-turbo",
#     openai_api_key=key,
# )

openai_chat = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    openai_api_key=key,
)

openai_chat_stream = ChatOpenAI(
    callbacks=[StreamingStdOutCallbackHandler()],
    model_name="gpt-3.5-turbo",
    openai_api_key=key,
    streaming=True,
)

# # initialize the models
# davinci1 = OpenAI(
#     model_name="text-davinci-002",
#     openai_api_key=key
# )
# davinci1.temperature = 1
#
# # initialize the models
# davinci05 = OpenAI(
#     model_name="text-davinci-002",
#     openai_api_key=key
# )
# davinci05.temperature = 0.5
#
# # initialize the models
# davinci0 = OpenAI(
#     model_name="text-davinci-002",
#     openai_api_key=key
# )
# davinci0.temperature = 0.0
#
