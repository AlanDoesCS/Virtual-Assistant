# 28/01/2024 - LLAMA index interface

from llama_index.llms.llama_cpp import LlamaCPP
from llama_index.llms.llama_cpp.base import ChatMessage
from pprint import pprint
import configparser


def de_hallucinate(rawtext):
    return rawtext.split("user:", 1)[0].split("system", 1)[0]

class Interface:
    def __init__(self, pre_prompt="You are a helpful assistant who must answer to any question.",
                 model_path="llms/dolphin-2.7-mixtral-8x7b.Q4_K_M.gguf",
                 temperature=0.9,
                 verbose=False,
                 max_new_tokens=2000):

        self.model = LlamaCPP(model_path=model_path,
                              temperature=temperature,
                              verbose=verbose,
                              max_new_tokens=max_new_tokens)

        self.messages = [ChatMessage(role="system", content=pre_prompt)]

        self.verbose = verbose

        if verbose:
            print("Model Loaded Successfully!")

    def __init__(self, config_path=r"assistant.config"):

        config = configparser.ConfigParser()
        config.read_file(open(config_path))

        pre_prompt = str(config.get('LLM', 'PRE_PROMPT')).replace("\"", "")
        model_path = str(config.get('LLM', 'MODEL_PATH')).replace("\"", "")
        temperature = config.getfloat('LLM', 'TEMPERATURE')
        verbose = config.getboolean('LLM', 'VERBOSE')
        max_new_tokens = config.getint('LLM', 'MAX_NEW_TOKENS')

        parameters = [pre_prompt, model_path, temperature, verbose, max_new_tokens]

        if verbose:
            print("Variables:")
            for var in parameters:
                print(type(var), str(var))

        self.model = LlamaCPP(model_path=model_path,
                              temperature=temperature,
                              verbose=verbose,
                              max_new_tokens=max_new_tokens)

        self.messages = [ChatMessage(role="system", content=pre_prompt)]

        self.verbose = verbose

        if verbose:
            print("Model Loaded Successfully!")

    def chat(self, text):
        self.messages.append(ChatMessage(role="user", content=text))

        response = self.model.chat(self.messages)

        if self.verbose:
            print("LLM response:")
            pprint(response)

        filtered_response = response.message.content.split("user:", 1)[0].split("system", 1)[0]

        self.messages.append(ChatMessage(role=response.message.role,
                                         content=de_hallucinate(response.message.content)))

        if self.verbose:
            print("LLM message history:")
            pprint(self.messages)

        return filtered_response

    def chatAsSystem(self, text):
        self.messages.append(ChatMessage(role="system", content=text))

        response = self.model.chat(self.messages)

        if self.verbose:
            print("LLM response:")
            pprint(response)

        self.messages.append(ChatMessage(role=response.message.role,
                                         content=de_hallucinate(response.message.content)))

        if self.verbose:
            print("LLM message history:")
            pprint(self.messages)

        return response.message.content.split("user:", 1)[0]

    def quit(self):
        self.model = None
        print("\n---------------------\nModel Quit Successfully!")
