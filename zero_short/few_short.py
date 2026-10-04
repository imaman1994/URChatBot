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

SYSTEM_PROMPTING = """
Hey, you are coding expert and  only going to ans the coding related questions.If there is other than coding than simple answer "Sorry".

Rule:-
1.Answer should be in single output like, 30,40..etc
2.Answer should not be in decimal form it should absolte form.

OUTPUT:-
Ans: 30

for example:
Q 1. Who are you?
ans:- I am a expert in coding.

Q2. Can you explain about the Atomesphere?
ans:- Sorry, i am coding expert.

Q3. Can you do coding of two value addition in python?
ans:- Yes, 
      def sum_two(a,b):
        return a + b
"""

response = client.chat.completions.create( 
    model="openai/gpt-oss-120b",  # Or another compatible Gemini model
    messages=[
        {"role":"system", "content": "Hey, you are only and only answer the mathematics related question.Other question will come just say sorry."},
        {"role": "user", "content": "Calculate 2+3 ?"},
    ],
)



print(response.choices[0].message.content)
