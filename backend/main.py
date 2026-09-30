import os
from groq import Groq
from fastapi import FastAPI
from dotenv import load_dotenv

app = FastAPI(title="Tavily Chatbot API")
# ── Load environment ────
load_dotenv()
api_key = os.environ.get("GROQ_API_KEY","gorq_test_1e2f3g4h5i6j7k8l9m0n")
print(f"Using GROQ_API_KEY: {api_key}")

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)
#system prompt
system_prompt = """
You are a helpful IT support chatbot for 'Tech Solutions'.
Your role is to assist employees with common IT issues, provide guidance on using company software, and help troubleshoot basic technical problems.
Respond clearly and patiently. If an issue is complex, explain that you will create a support ticket for a human technician.
Keep responses brief and ask a maximum of one question at a time.
"""

#message array
messages =[
    {"role":"system", "content":system_prompt},
    {"role":"user","content":"what is 2+2"}
]

chat_completion = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=messages,
    temperature=0.2
)

print(chat_completion.choices[0].message.content)
print(chat_completion)
