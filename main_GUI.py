# 08/11/2023 - Virtual assistant
#
#   Important Note:
#
#   To run this program, open LM Studio, start the LLM and start a server on
#   port 1234, with all options enabled.
#

import os
import customtkinter as ctk
from threading import Thread  # Necessary to prevent window from "freezing"
from customthread import CustomThread as cThread
from customthread import CustomThreadTest
import tkinter as tk
import webbrowser
import openai

# ------- OpenAI ------- #
openai.api_key = ""  # no need for an API key
openai.api_type = "open_ai"
openai.api_base = "http://localhost:1234/v1"  # point to the local server

# ----- LLM Memory ----- #
messages = [{"role": "system", "content": "You are a helpful assistant who must answer to any question."}]


# ------ Functions ------ #
def insert_newlines(string, every=144):
    string = string.split(" ")
    new_str = ""
    for index in range(len(string)):
        new_str += string[index] + " "
        if (index + 1) % every == 0:
            new_str += "\n"
    return new_str


# ------ CTkinter ------ #
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("CheapGPT")
root.geometry("950x700")
root.resizable(0, 0)  # Don't allow resizing in the x or y direction

frame = ctk.CTkFrame(master=root)
frame.grid(row=0, column=0, padx=10, pady=10)

label = ctk.CTkLabel(master=frame, text="CheapGPT", font=("Roboto", 36, "bold"))
label.grid(row=1, column=0, pady=12, columnspan=3)

conversation_frame = ctk.CTkScrollableFrame(master=frame, width=890, height=525)
conversation_frame.grid(row=3, column=0, padx=10, pady=10, columnspan=3)


def get_llm_response(modelname, context, temperature, max_tokens):
    completion = openai.ChatCompletion.create(
        model=modelname,  # this field is currently unused
        messages=context,
        temperature=temperature,
        max_tokens=max_tokens
    )
    return completion.choices[0].message.content


def prompt_via_ui(prompt):
    global conversation_frame
    frame_rows = conversation_frame.grid_size()[1]  # Number of rows from tuple

    # Add prompt to history:
    print("You:", prompt)
    global messages
    messages.append({"role": "user", "content": prompt})

    # Start LLM with prompt on new thread
    llm_thread = cThread(target=get_llm_response, args=("local-model", messages, 0.9, -1))
    llm_thread.start()

    # Signature
    new_user_signature_frame = ctk.CTkFrame(master=conversation_frame, width=30)
    new_user_signature_frame.grid(row=int(frame_rows), column=0, pady=5, padx=5, columnspan=1, sticky="NW")
    new_user_signature = ctk.CTkLabel(master=new_user_signature_frame, text="User", font=("Roboto", 14, "bold"),
                                     wraplength=700, justify="left", anchor="w", text_color="orange")
    new_user_signature.grid(row=int(frame_rows), column=0, pady=5, padx=10, columnspan=1, sticky="W")

    # Text
    new_user_label = ctk.CTkLabel(master=conversation_frame, text=prompt, font=("Roboto", 14),
                                  wraplength=700, justify="left", anchor="w")
    new_user_label.grid(row=int(frame_rows), column=1, pady=5, padx=10, columnspan=2, sticky="W")

    # Get LLM Response
    response = str(llm_thread.join())

    # Add response to history:
    print("AI:", response)

    # Signature
    new_llm_signature_frame = ctk.CTkFrame(master=conversation_frame, width=30)
    new_llm_signature_frame.grid(row=int(frame_rows+1), column=0, pady=5, padx=5, columnspan=1, sticky="NW")
    new_llm_signature = ctk.CTkLabel(master=new_llm_signature_frame, text="AI", font=("Roboto", 14, "bold"),
                                 wraplength=700, justify="left", anchor="w", text_color="green")
    new_llm_signature.grid(row=int(frame_rows+1), column=0, pady=5, padx=10, columnspan=1, sticky="W")

    # Text
    new_llm_label = ctk.CTkLabel(master=conversation_frame, text=response, font=("Roboto", 14),
                                 wraplength=700, justify="left", anchor="w")
    new_llm_label.grid(row=int(frame_rows + 1), column=1, pady=5, padx=10, columnspan=2, sticky="W")

    messages.append({"role": "assistant", "content": response})


input_frame = ctk.CTkFrame(master=frame, width=800, height=50)
input_frame.grid(row=4, column=0, padx=0, pady=10, columnspan=3)

user_inp = ctk.CTkEntry(master=input_frame, placeholder_text="Enter Prompt:", width=600, font=("Roboto", 14))
user_inp.grid(row=0, column=0, pady=5, padx=(10, 2), columnspan=2, sticky="ew")

button = ctk.CTkButton(master=input_frame, text="Send", command=lambda: prompt_via_ui(user_inp.get()), anchor="w",
                       width=30, font=("Roboto", 14, "bold"))
button.grid(row=0, column=2, pady=5, padx=(2, 10), columnspan=1)

# DO NOT TOUCH ( please :) )
root.mainloop()
