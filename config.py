import os
from langchain_ollama.llms import OllamaLLM

os.environ["OPENAI_API_KEY"] = "NA"
model = OllamaLLM(model="llama3.1", base_url="http://localhost:11434")
