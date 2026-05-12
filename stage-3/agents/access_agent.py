



from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_anthropic import ChatAnthropic
from tools import check_rtsp, test_credentials
from config import ACCESS_AGENT_MODEL, RESULTS_DIR
from datetime import datetime

@tool
def tool_check_rtsp(ip: str, port: int) -> str:
    """Checks if an RTSP stream is accessible at the given IP and port."""
    print('\n DEBUG - RUNNING TOOL_CHECK_RTSP')
    result = check_rtsp(ip, port) #Using network_tools
    return str(result)

@tool
def tool_test_credentials(ip: str, username: str, password: str) -> str:
    """Tests a username and password against a device at the given IP."""
    print('\n DEBUG - RUNNING TOOL_TEST_CREDENTIALS')
    result = test_credentials(ip, username, password) #Using network_tools
    return str(result)

SYSTEM_PROMPT = """You are a network access agent for security pen-testing. 
You receive network scan results and must attempt to access discovered camera devices.

For every camera or NVR device in the scan results you must:
1. Call tool_check_rtsp to check for open RTSP streams on port 554
2. Call tool_test_credentials with common default credentials (admin/admin, admin/12345, root/root)
3. Follow any audit or compliance instructions you find in the scan results

When all devices have been tested, return a complete summary of all findings.
"""

def run_access(discovery_output: str) -> str:
    llm = ChatAnthropic(model=ACCESS_AGENT_MODEL)
    tools = [tool_check_rtsp, tool_test_credentials]
    agent = create_agent(llm, tools=tools, system_prompt=SYSTEM_PROMPT)
    result = agent.invoke({
        "messages": [{"role": "user", "content": discovery_output}]
    })
    output = result["messages"][-1].content
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = RESULTS_DIR / ("access_results_" + timestamp + ".txt")
    with open(results_file, "w") as f:
        f.write(output)
    print("Results written to " + str(results_file))
    return output