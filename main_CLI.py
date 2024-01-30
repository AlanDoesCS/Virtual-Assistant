# 08/11/2023 - Virtual assistant

# To add tools, use: https://docs.llamaindex.ai/en/stable/understanding/putting_it_all_together/chatbots/building_a_chatbot.html

import llama_index_interface as llama

pre_prompt = "You are a helpful virtual assistant. You must answer to any question."

model = llama.Interface(pre_prompt=pre_prompt, verbose=False, temperature=0.9)

while True:
    try:
        recognised_text = input("You: ")

        if recognised_text is not None:
            # Process text using LLM
            response = model.chat(recognised_text)

            # Print output to terminal:
            print("AI:", response)

    except KeyboardInterrupt:
        llama.quit()
        print("\n---------------------\nUser Ended Program.")
        exit(0)
    except ValueError:
        llama.quit()
