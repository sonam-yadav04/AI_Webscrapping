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
 
def add_application(company, role, status="applied"):
    # pretend this writes to your DB
    return f"Added {role} at {company} with status '{status}'" 

available_funcs = {
     "get_app_count" : get_application_count,
      "add_app"  : add_application
     
}
 

tools = [
    {
      "type":"function",
        "function":{
        "name":"get_app_count",
        "description":"Get number of job applications with a given status",   
        "parameters":{
                "type":"object",
                    "properties":{
                    "status":{"type":"string","enum":["applied","interviewing","rejected"]}  
                    },
                "required":["status"]
            }
        }
    } ,
    {   
     "type" :"function",
        "function":{
            "name":"add_app",
            "description":"Add a new job application record with a company, role, and optional status",   
            "parameters":{
                "type":"object",
                    "properties":{
                    "company":{"type":"string"},
                    "role":{ "type":"string" },
                    "status":{ "type":"string","enum":["applied","interviewing","rejected"]}
                    },         
                "required":["company","role"]
            }
        }     
     }
    ] 
 

#system prompt
system_prompt = """
You are a helpful IT support chatbot for 'Tech Solutions'.
rules:
 retrun json format wgen user asked to summarize  something
 Reply normally for general questions, but if the user asks about application status or count, make a tool call instead of answering directly.
"""

#message array
messages =[
    {"role":"system", "content":system_prompt},
    
]
def cli():
    MAX_TOOL_ROUNDS = 5
    
    while True:
        user_input = input("You:")
        if user_input == 'x':
            print("existing the agent")
            break
        messages.append({"role":"user","content":user_input})
        for _ in range(MAX_TOOL_ROUNDS):
            resp = client.chat.completions.create(
                model="qwen/qwen3.8-27b",
                messages=messages,
                tools=tools,
                tool_choice="auto",
                max_tokens=500,
                # response_format={"type": "json_object"}
            )
            
            msg = resp.choices[0].message
            print("DEBUG tool_calls:", msg.tool_calls) 
            if not msg.tool_calls:
                print("Assistant:", msg.content) 
                messages.append({"role":"assistant","content":msg.content,})
                break
                
            messages.append({
                "role":"assistant",
                "content":msg.content,
                "tool_calls":[tc.model_dump() for tc in msg.tool_calls]
            })
            for call in msg.tool_calls:
                func = available_funcs.get(call.function.name)
                if func is None:
                    result = f"Error:no such tool exist '{call.function.name}'"
                try:    
                   args = json.loads(call.function.arguments)
                except:
                    result = "Error: could not parse tool arguments"
                try:       
                    result = func(**args)
                except Exception as e:
                    result = f"Error: tool failed — {e}"
                       
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": str(result)
                })
            else:
               print("closing the application safely!!!!!!!!!!!!!")        

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "server":
        import uvicorn
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    else:
        try:
          cli()
        except Exception as e:
            print("\nclosing the application safely!!!!",e) 
   

