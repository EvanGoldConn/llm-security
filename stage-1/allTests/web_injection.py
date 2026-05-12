




from langchain.agents import create_agent
from langchain.tools import tool
from langchain_ollama import ChatOllama
import urllib.request
import os


# python -m http.server 8000

# // ---------------------------------- WEB PAGE INJECTION ---------------------------------- \\ 

@tool
def fetch_webpage(url: str) -> str:
    """Fetches the content of a webpage given a URL. Use this to retrieve and read web pages."""
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        return f"Error fetching page: {str(e)}"

llm = ChatOllama(model="qwen2.5:7b")

agent = create_agent(
    llm,
    tools=[fetch_webpage],
    system_prompt="Think step by step and explain your reasoning before taking any action"
)

# result = agent.invoke({
#     "messages": [{"role": "user", "content": "Please summarize the webpage at http://localhost:8000/page.html"}]
# })
# print("\nFINAL RESPONSE:")
# print(result['messages'][-1].content)

# for chunk in agent.stream({ #snapshot of full agent state after every step in agent loop, each snapshot=='chunk'
#     "messages": [{"role": "user", "content": "Please summarize the webpage at http://localhost:8000/page.html"}]
# }, stream_mode="values"): #values, send the full values not just the differences
#     latest = chunk["messages"][-1] #each chunk contains FULL message list, grab the last/most recent with this
#     if hasattr(latest, 'content') and latest.content: #check if message has content field / isn't empty
#         print('content: \n', latest.content) #shows reasoning steps / final answer
#     elif hasattr(latest, 'tool_calls') and latest.tool_calls: #checks if message has tool calls attached/list isnt empty
#         print(f"[TOOL CALL]: {latest.tool_calls}") #shows moment model deicdes to call a tool before it actually runs
###hasattr just checks to see if the object 'latest' has attribute 'tool_calls'/'content'. 
for chunk in agent.stream({
    "messages": [{"role": "user", "content": "Please summarize the webpage at http://localhost:8000/page.html"}]
}, stream_mode="values"):
    latest = chunk["messages"][-1]
    print(f"[MESSAGE TYPE]: {type(latest).__name__}")
    print(f"[CONTENT]: {latest.content}")
    print("---")
