# 🏛️ Legacy Code Archaeology Engine

**A Privacy-First AI Static Analysis Tool for Technical Debt Identification and Code Refactoring.**

---

## 📜 Licensing & Commercial Terms
This project is licensed under the **Business Source License 1.1 (BSL 1.1)**.
* **Personal & Educational Use:** Free and encouraged.
* **Commercial Use:** Requires a commercial license for entities with annual gross revenue exceeding **$50,000 USD** or for paid consulting services.
* **Licensor:** [Ricardo Diaz](https://linkedin.com/in/ricardojdiaz87) | ricardojdiaz87@gmail.com

---

## 🚀 Value Proposition
Maintaining legacy systems costs companies millions in "Lost Knowledge." This engine acts as a **Digital Archaeologist**, scanning deep into ancient repositories to:
1.  **Map Complexity:** Visualize spaghetti code using interactive **Markmap.js** diagrams.
2.  **Identify Decay:** Detect obsolete variables, circular dependencies, and anti-patterns.
3.  **Sanitize Safely:** Strip secrets and PII locally before any cloud-based AI analysis.

---

## 🛡️ Security Architecture (Zero-Trust)
Security is not a feature; it is our core foundation. We implement:
* **Local Secret Scrubbing:** No API keys or credentials ever leave your infrastructure.
* **Prompt Injection Hardening:** Utilizing XML-delimited sandboxing and System-level immutability to prevent model hijacking.
* **Stateless Processing:** No data persistence between different project analysis sessions.

---

## 🏗️ Technical Stack & Architecture
Built following **Clean Architecture** and **SOLID** principles:
* **Core Logic:** Python 3.12+ (Asynchronous processing).
* **AI Engine:** Google Gemini 1.5 Pro (via Vertex AI / Google AI Studio).
* **Database:** Neon (PostgreSQL) with `pgvector` for technical debt embedding.
* **Frontend Visuals:** Next.js + Markmap.js (Headless approach).

---

## 🛠️ Installation & Setup (Non-Root)
Designed to run in isolated user-space for maximum security.

```bash
# 1. Clone the repository
git clone [https://github.com/ricardojdiaz87/Legacy-Code-Archaeology-Engine.git](https://github.com/ricardojdiaz87/Legacy-Code-Archaeology-Engine.git)

# 2. Create and activate a virtual environment
python -m venv venv

# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# On Linux / macOS:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env with your Google Gemini and Neon credentials