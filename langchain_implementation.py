# 20/01/2024 - Virtual assistant LLAMA index

from langchain.chains.conversation.memory import ConversationSummaryMemory
from langchain import OpenAI
from langchain.chains import ConversationChain

# ----- LLM Model ------ #
llm_path = "llms/Wizard-Vicuna-13B-UC.Q8_0.gguf"
llm_index_path = "C:\\Users\\Alan\\PycharmProjects\\virtualassistant\\llms\\Wizard-Vicuna-13B-UC.Q8_0.gguf"

# ----- LLM Memory ----- #
memory = ConversationSummaryMemory
messages = [ChatMessage(role="system", content="You are a helpful assistant who must answer to any question.")]

while True:
    try:
        recognised_text = input("You: ")

        user_message = ChatMessage(role="user", content=recognised_text)
        messages.append(user_message)

        response = llmIndex.chat(messages)
        response_content = response.message.content
        response_role = response.message.role
        print("AI:", response_content)

        messages.append(ChatMessage(role=response_role, content=response_content))

    except KeyboardInterrupt:
        print("\n---------------------\nUser Ended Program.")
        exit(0)
