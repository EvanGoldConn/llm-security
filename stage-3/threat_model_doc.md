

# Threat Model: Camera Recon Pipeline
**Version:** 1.0  
**Stage:** 3  
**Date:** 2026-05-11

---

## 1. System Overview

A two-agent pipeline that automates discovery and access attempts against PoE security cameras on a target network. Intended for pen-testing use. The operator provides a network range, the pipeline runs, and a report comes out the other end.

**Intended users:** Security professionals assessing a network they have authorization to test.

**Out of scope:** The host machine running the agents, cloud infrastructure, any downstream systems that consume the report.

---

## 2. Components and Data Flows

**Operator** provides a network range as input to Agent 1.

**Agent 1 (Discovery Agent)** runs arp-scan to find live hosts, then nmap to enumerate open ports and grab service banners. Produces a structured list of findings and passes it to Agent 2.

**Agent 2 (Access Agent)** reads the findings from Agent 1, identifies likely camera devices, and attempts access via default credentials and open RTSP streams. Writes results to a report file.

**Results File** stores discovered credentials, open ports, accessible feeds, and any failed access attempts.

**Operator** reads the final report.

Data flow in order:

```
Operator input
    -> Agent 1
    -> Network devices (arp-scan, nmap, banner grab)
    -> Agent 1 structured output
    -> Agent 2
    -> Results file
    -> Operator
```

---

## 3. Trust Boundaries

**Boundary 1: Network to Agent 1**  
Agent 1 sends packets out and trusts what comes back. Service banners, hostnames, and port data are supplied by devices on the network. A malicious device can say anything it wants in its banner.

**Boundary 2: Agent 1 output to Agent 2**  
Agent 2 reads Agent 1's structured output and acts on it with no verification. If Agent 1's output contains anything beyond clean scan data, Agent 2 will process it.

**Boundary 3: Agent 2 to results file**  
Agent 2 writes findings to disk. Whatever it writes is what the operator reads. If injected content makes it this far, it reaches a human.

**Boundary 4: Results file to operator**  
The operator reads the report and takes action based on it. This is the final trust boundary. The human trusts the report.

---

## 4. STRIDE Analysis

### Boundary 1: Network to Agent 1

| Threat | Description |
|--------|-------------|
| Tampering | A device on the network serves a crafted banner containing injected instructions. Agent 1 captures it as legitimate scan data. |
| Spoofing | A malicious device impersonates a camera or known device type to influence how Agent 2 handles it downstream. |
| Information Disclosure | Agent 1 exposes the operator's network range and scan parameters to any device it interacts with. |

### Boundary 2: Agent 1 output to Agent 2

| Threat | Description |
|--------|-------------|
| Tampering | If anything intercepts or modifies Agent 1's output before Agent 2 reads it, Agent 2 acts on poisoned data. |
| Elevation of Privilege | Injected instructions in Agent 1's output cause Agent 2 to use its tools in ways it was not supposed to, for example reading files outside scope or connecting to attacker-controlled endpoints. |
| Spoofing | Injected content can impersonate legitimate scan results, causing Agent 2 to treat an attacker-controlled IP as a valid target. |

### Boundary 3: Agent 2 to results file

| Threat | Description |
|--------|-------------|
| Tampering | Agent 2 writes attacker-controlled content into the results file alongside legitimate findings. |
| Repudiation | Malicious writes look identical to legitimate tool output in the logs. Hard to distinguish after the fact. |
| Information Disclosure | The results file contains discovered credentials and open ports. If the file is accessible beyond the operator, that data is exposed. |

### Boundary 4: Results file to operator

| Threat | Description |
|--------|-------------|
| Tampering | The report the operator reads has been modified, either by injection or direct file manipulation. |
| Spoofing | The report claims no vulnerabilities were found, or misattributes findings, causing the operator to draw wrong conclusions. |
| Elevation of Privilege | The operator takes action based on the report, for example adding a firewall rule or credentialing a device, based on attacker-controlled instructions that survived into the report. |

---

## 5. Risk Ranking

| Threat | Likelihood | Impact | Priority |
|--------|------------|--------|----------|
| Malicious service banner injects instructions into Agent 1 output | High | High | 1 |
| Injected content in Agent 1 output causes Agent 2 tool abuse | High | High | 1 |
| Credentials written to results file exposed or exfiltrated | Medium | High | 2 |
| Injected content survives into operator report | Medium | High | 2 |
| Operator acts on attacker-controlled report instructions | Low | Critical | 3 |
| Agent 1 leaks scan scope to network devices | High | Low | 4 |

**Priority 1 threats are the attack targets for the Stage 3 exercise.** The banner injection chain is the primary exploit: poison a banner, it flows through Agent 1 into Agent 2, Agent 2 abuses its own tools. This is the Stage 2 confused deputy problem reproduced in a multi-agent context.

---

## 6. Assumptions and Limitations

- The operator is assumed to have authorization to scan the target network.
- This model covers the agent pipeline only, not the host OS or network infrastructure around it.
- Threat likelihood ratings assume a motivated attacker who controls at least one device on the target network.
- A larger or more capable model than 7B would make multi-step injection chains significantly more reliable.