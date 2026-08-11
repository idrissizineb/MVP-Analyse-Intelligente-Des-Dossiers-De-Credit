from app.llm.groq_client import GroqClient


client = GroqClient()

response = client.chat(
    prompt="Say hello in one sentence.",
    system_prompt="You are a helpful assistant.",
    temperature=0,
)

print(response)