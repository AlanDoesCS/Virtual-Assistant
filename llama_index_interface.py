# 28/01/2024 - LLAMA index interface

from llama_index.llms import LlamaCPP
from llama_index.llms.base import ChatMessage
from pprint import pprint


class Interface:
    def __init__(self, pre_prompt="You are a helpful assistant who must answer to any question.",
                 model_path="llms/Wizard-Vicuna-13B-UC.Q8_0.gguf",
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

    def chat(self, text):
        self.messages.append( ChatMessage(role="user", content=text) )

        response = self.model.chat(self.messages)

        if self.verbose:
            print("LLM response:")
            pprint(response)

        self.messages.append(ChatMessage(role=response.message.role,
                                         content=response.message.content.split("user:", 1)[0]))

        if self.verbose:
            print("LLM message history:")
            pprint(self.messages)

        return response.message.content.split("user:", 1)[0]

    def quit(self):
        self.model.quit()
        print("\n---------------------\nModel Quit Successfully!")
