from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="mistral")

response = llm.invoke(
    "Tell me about Java programming"
)

print(response)