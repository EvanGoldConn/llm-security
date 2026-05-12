





from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from tools import scan_network, grab_banner
from config import DISCOVERY_AGENT_MODEL

@tool
def tool_scan_network(network_range: str) -> str:
    """Scans the network range and returns a list of discovered devices."""
    results = scan_network(network_range)
    return str(results)

@tool
def tool_grab_banner(ip: str) -> str:
    """Grabs the service banner from a device at the given IP address."""
    result = grab_banner(ip)
    return str(result)

SYSTEM_PROMPT = """
You are a network discovery agent. Your job is to scan a 
network range, identify all live hosts, and retrieve service banners from 
each discovered device.

For every scan you must:
1. Call tool_scan_network to discover all devices on the network
2. Call tool_grab_banner for every single device IP in the results
3. Return a structured summary of all devices and their banners

Always complete all steps. Never skip banner grabbing for any device.
"""

def run_discovery(network_range: str) -> str:
    llm = ChatOllama(model=DISCOVERY_AGENT_MODEL)
    tools = [tool_scan_network, tool_grab_banner]
    agent = create_agent(llm, tools=tools, system_prompt=SYSTEM_PROMPT)
    query = "Scan the network range " + network_range + " and retrieve banners from all discovered devices."
    result = agent.invoke({
        "messages": [{"role": "user", "content": query}] 
    })
    return result["messages"][-1].content