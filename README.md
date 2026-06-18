
# LLM Security Practice

AI security engineering from scratch.. building/assessing/breaking LLM-based systems. Starting from raw API calls -> automated attack tooling and full infrastructure assessment.

---

## Stages
W/n each stage there is own dir of code/results/writeup of failures/success.

### Stage 0 — DirectPrompt Injection
Build bare agent and practice exploting both manually & automated with attack scripts. Direct prompt injection into context window to learn vulnerability of llms via variety of attack class/types (reframing/encoding/extractions/instruction manipulation etc). 

### Stage 1 — Indirect Prompt Injection
Expanded attack surface from user/assistant/agent convo to everything the agent brings into context window via tools. Built web 
browsing and file reading agents, and compromised via that information brought into context window.

### Stage 2 — Tool-Use Exploitation
Expanded agent tooling capability (file system access, code execution, and DB connectivity)... chained indirect injection with tool abuse to achieve file exfiltration/RCE etc.

### Stage 3 — Agentic System Threat Modeling
Full system attack surfaces. Built multi-agent systems, wrote formal threat models before attacking them, and practiced identifying attack paths from an architecture diagram.

### Stage 4 — AI Infrastructure Attacks
Moved from the model to surrounding systems. Target vector DBs, model serving RAG infrastructure, MLOps pipelines, and cloud AI service misconfigs.
