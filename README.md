# 🏛️ Project-Wide Code Archaeology & Restoration

An advanced AI-driven utility designed to scan, audit, and refactor legacy Python codebases into production-ready, PEP8-compliant systems. Built with a focus on **Resilience, Security, and Financial Intelligence (FinOps).**

## 🚀 Key Features

### 🛡️ 1. Security-First: PII & Secret Scrubbing
Before any code is sent to the LLM, the system performs a local scan to identify and mask sensitive information:
* **API Keys & Tokens:** Automated masking of potential credentials.
* **Emails:** Identification and scrubbing of developer/user emails.
* **No Data Leakage:** Ensures your proprietary secrets never leave your local environment.

### 📉 2. FinOps: Token & Cost Intelligence
The engine calculates the economic impact of the restoration *before* execution:
* **Heuristic Estimation:** Uses a 4:1 character-to-token ratio for budget forecasting.
* **Cost Projection:** Integration with `.env` pricing models (Input/Output).
* **Free Tier Awareness:** Real-time monitoring of Google Gemini Free Tier limits.

### 🏛️ 3. Resilient Architecture: Circuit Breaker Pattern
Built to handle the instability of external APIs and rate limits:
* **Fault Tolerance:** If a 429 (Resource Exhausted) error occurs, the **Circuit Breaker trips**, aborting the process to protect system health and prevent IP bans.
* **Exponential Backoff:** Automated "Cooling Down" periods (65s - 120s) to maximize success rates on free-tier quotas.

## 📊 System Flow & Resilience

```mermaid
graph TD
    A[Start: Run main.py] --> B[Local Scan: Get Python Files]
    B --> C[FinOps: Estimate Token Costs]
    C --> D[Step 1: PII Scrubber & Masking]
    D --> E[Step 2: Global AI Analysis]
    
    E -- Success --> F[Step 3: Individual File Restoration]
    E -- API Error 429 / Quota Exhausted --> G{🚨 CIRCUIT BREAKER}
    
    G -->|Tripped| H[Abort Process: Safety Stop]
    G -->|Manual Reset| E
    
    F --> I[Final Output: /restored_project]
    I --> J[End: Process Complete]
    
    style G fill:#f96,stroke:#333,stroke-width:4px
    style H fill:#ff9999,stroke:#333