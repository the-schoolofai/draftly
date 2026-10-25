# Step 00 - Plain LLM call (no agent yet)
from langchain.chat_models import init_chat_model


# LLM
llm = init_chat_model(
    model="ollama:gemma3:1b",
    temperature=0.3,
)

# Single call
q = input("Enter email draft idea: ")
response = llm.invoke(q)

print(response.text)
