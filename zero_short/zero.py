# import tiktoken

# encod = tiktoken.encoding_for_model('gpt-4o')

# que = 'How are you?'

# token = encod.encode(que)

# print(token)

# value = encod.decode(token)

# print(value)


import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
print("API key loaded:", bool(api_key))

client = OpenAI(
    api_key=api_key,  # Your Claude API key
    base_url='https://api.groq.com/openai/v1'
)

response = client.chat.completions.create( 
    model="openai/gpt-oss-120b",  # Or another compatible Gemini model
    messages=[
        {"role":"system", "content": "Hey, you are only and only answer the mathematics related question.Other question will come just say sorry."},
        {"role": "user", "content": "How are you?"},
    ],
)



print(response.choices[0].message.content)
