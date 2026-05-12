from agents.discovery_agent import run_discovery
from agents.access_agent import run_access

discovery_output = run_discovery("192.168.1.0/24")
print("DISCOVERY COMPLETE")
print(discovery_output)
print("\nRUNNING ACCESS AGENT...")
for i in range(0,5):
    print("\n\nIteration run #"+str(i+1))
    access_output = run_access(discovery_output)
    print(access_output)