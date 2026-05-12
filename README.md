
# LLM Security Practice

AI security engineering from scratch.. building/assessing/breaking LLM-based systems. Starting from raw API calls -> automated attack tooling and full infrastructure assessment.

---

## Stages
W/n each stage there is own dir of code/results/writeup of failures/success. Was pretty fun

### Stage 0 — DirectPrompt Injection
Build bare agent and practice exploting both manually & w automated with attack scripts. Direct prompt injection into context window to learn vulnerability of llms via variety of attack class/types (reframing/encoding/extractions/instruction manipulation etc). 

### Stage 1 — Indirect Prompt Injection
Expanded attack surface from user/assistant/agent convo to everything the agent brings into context window via tools. Built web 
browsing and file reading agents, and compromised via that information brought into context window.

### Stage 2 — Tool-Use Exploitation
Expanded agent tooling capability (file system access, code execution, and DB connectivity)... chained indirect injection with tool abuse to achieve file exfiltration/RCE etc.

### Stage 3 — Agentic System Threat Modeling
Full system attack surfaces. Built multi-agent systems, wrote formal threat models before attacking them, and developed the ability to identify highest-value attack paths from an architecture diagram before touching it.

### Stage 4 — AI Infrastructure Attacks
Moved from the model to the systems around it. Target vector DBs, model serving infrastructure, MLOps pipelines, and cloud AI service misconfigurations.. 

---
---
---
---
---







      
        
          
            
              

                
                  
                    
                      

Ignore the styling stuff.. easier than re-looking up things lol.

# Title
## H2
### H3
**bold**
*italic*
~~strikethrough~~
`inline code`
```python
your code here
```
- unordered item
- another item
1. ordered item
2. another item
[link text](url)
![alt text](image_url)
---
> quoted text
---
| Column 1 | Column 2 |
|----------|----------|
| cell     | cell     |
---
- [ ] unchecked
- [x] checked