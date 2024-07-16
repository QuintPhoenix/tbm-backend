import os
from together import Together
client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))

def llama_gen(title: str, section: str):
    prompt =  f"you are a travel blogger write about {section} in {title}"
    stream = client.chat.completions.create(
  model="meta-llama/Llama-3-8b-chat-hf",
  messages=[{"role": "user", "content": prompt}],
  stream=True,
)
    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content or ""
    
    return response


