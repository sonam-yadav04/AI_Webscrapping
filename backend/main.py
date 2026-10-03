import os
from groq import Groq
from fastapi import FastAPI
from dotenv import load_dotenv
import httpx 
import json

app = FastAPI(title="Tavily Chatbot API")
# ── Load environment ────
load_dotenv()
api_key = os.environ.get("GROQ_API_KEY","gorq_test_1e2f3g4h5i6j7k8l9m0n")
# print(f"Using GROQ_API_KEY: {api_key}")

client = Groq(api_key=api_key)

# models = client.models.list()
# for m in models.data:
#     print(m.id)

def get_application_count(status):
     fake_db = {"applied": 12, "interviewing": 3, "rejected": 5}
     return fake_db.get(status, 0)

tools = [
    {
        "type":"function",
        "function":{
                      "name":"get_application_count",
                      "description":"Get number of job applications with a given status",   
                       "parameters":{
                                "type":"object",
                                 "properties":{
                                 "status":{
                                    "type":"string",
                                    "enum":["applied","interviewing","rejected"]
                                    }  
                                    },
                                "required":["status"]
                                  },
                    }     
         }    
       ] 
 

#system prompt
system_prompt = """
You are a helpful IT support chatbot for 'Tech Solutions'.
Reply normally for general questions, but if the user asks about application status or count, make a tool call instead of answering directly.
"""

#message array
messages =[
    {"role":"assistant", "content":system_prompt},
    
]

while iter < max_iterations:
   
    user_input = input("You:")
    if user_input == 'x':
        print("existing the agent")
        break
    messages.append({"role":"user","content":user_input})
    resp = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    
    msg = resp.choices[0].message
    print("DEBUG tool_calls:", msg.tool_calls) 
    if msg.tool_calls:
        call = msg.tool_calls[0]
        args= json.loads(call.function.arguments)
        result = get_application_count(**args)

        messages.append({
            "role":"assistant",
            "content":msg.content,
            "tool_calls":[tc.model_dump() for tc in msg.tool_calls]
        })
        messages.append({
            "role":"tool",
            "tool_call_id":call.id,
            "content":str(result)
        })
        
        final_res = client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=messages
            
        )
        print("Assistance:",final_res.choices[0].message.content)
        
    else:    
        print("Assistance:", msg.content)
        messages.append({"role":"assistant", "content": msg.content})

if __name__ == "__main__":
    import uvicorn
    try:
        uvicorn.run("main:app", host="0.0.0.0",port=8000,reload=True)   
    except KeyboardInterrupt:
        print("Server Stoped cleanly")    
    

