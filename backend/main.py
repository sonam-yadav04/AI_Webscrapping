import os
from groq import Groq
from fastapi import FastAPI
from dotenv import load_dotenv
import httpx 

app = FastAPI(title="Tavily Chatbot API")
# ── Load environment ────
load_dotenv()
api_key = os.environ.get("GROQ_API_KEY","gorq_test_1e2f3g4h5i6j7k8l9m0n")
print(f"Using GROQ_API_KEY: {api_key}")

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

models = client.models.list()
for m in models.data:
    print(m.id)
#system prompt
system_prompt = """
You are a helpful IT support chatbot for 'Tech Solutions'.
Your role is to assist employees with common IT issues, provide guidance on using company software, and help troubleshoot basic technical problems.
Respond clearly and patiently. If an issue is complex, explain that you will create a support ticket for a human technician.
Keep responses brief and ask a maximum of one question at a time.
"""

#message array
messages =[
    {"role":"assistant", "content":system_prompt},
    {"role":"user","content":"what is 2+2"}
]
while True:
    user_input = input("You:")
    if user_input == 'x':
        print("existing the agent")
        break
    messages.append({"role":"user","content":user_input})
    resp = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=messages,
        temperature=0.2
    )
    reply_txt  = resp.choices[0].message.content
    print("Assistance:", reply_txt)
    messages.append({"role":"assistant", "content": reply_txt})

if __name__ == "__main__":
    import uvicorn
    try:
        uvicorn.run("main:app", host="0.0.0.0",port=8000,reload=True)   
    except KeyboardInterrupt:
        print("Server Stoped cleanly")    
    

