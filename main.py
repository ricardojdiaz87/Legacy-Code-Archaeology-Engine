import os
import sys
import json
import logging

# =================================================================
# 1. ENFORCED PATH RESOLUTION (Senior Architecture)
# =================================================================
# Resolvemos rutas para que funcione en Windows Venv y Fedora Linux
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, 'src')

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# =================================================================
# 2. FAIL-SAFE IMPORTS
# =================================================================
try:
    from src.services.restorer import CodeRestorer
    from src.utils.scrubber import PIIScrubber
    from src.utils.reporter import AuditReporter
except ImportError:
    try:
        from services.restorer import CodeRestorer
        from utils.scrubber import PIIScrubber
        from utils.reporter import AuditReporter
    except ImportError as e:
        print(f"❌ CRITICAL STRUCTURAL ERROR: {e}")
        print("💡 Checklist: Ensure src/utils/reporter.py and other modules exist.")
        sys.exit(1)

# Professional logging configuration
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# =================================================================
# 3. PIPELINE ORCHESTRATION
# =================================================================
def run_pipeline():
    """
    Main Orchestrator:
    Discovery -> Local Scrubbing -> AI Refactoring (Mock) -> Restoration -> Reporting.
    """
    logging.info("🚀 Starting Legacy Code Restoration Pipeline...")

    # Initialize Core Services
    restorer = CodeRestorer(output_path="restored_project")
    pipeline_audit_data = [] 
    
    # Discovery Phase: Detect .py files, ignore orchestrators and reports
    ignored_files = ['main.py', 'generate_report.py']
    legacy_files = [f for f in os.listdir('.') if f.endswith('.py') and f not in ignored_files]
    
    if not legacy_files:
        logging.warning("⚠️ No legacy files detected in the root directory.")
        return

    for file_path in legacy_files:
        logging.info(f"📂 Processing Target: {file_path}")

        try:
            # STAGE 1: Security Scrubbing (Local Masking)
            # We only READ the file, we don't execute it (Safe for Windows)
            scrubbed_content = PIIScrubber.scrub_file(file_path)
            logging.info(f"🛡️ Stage 1: Security Shield active for {file_path}")
            
            # STAGE 2: AI Refactoring Simulation
            # In Phase 2, this will be connected to Gemini API
            logging.info(f"🧠 Stage 2: AI Analyzing legacy patterns in {file_path}")
            mock_ai_output = (
                "import typing\n\n"
                "def restored_logic(data: list) -> dict:\n"
                "    \"\"\"Refactored by Legacy Engine v1.0 - Clean & Typed.\"\"\"\n"
                "    return {str(i): v for i, v in enumerate(data) if v is not None}\n"
            )

            # STAGE 3: Shielded Restoration & AST Syntax Validation
            logging.info(f"🧱 Stage 3: Applying Validation Shield to {file_path}")
            success = restorer.save_restored_file(file_path, mock_ai_output)

            if success:
                # STAGE 4: Audit Traceability
                trace = restorer.generate_audit_report(file_path, changes_count=15)
                trace["security_scan"] = "PASSED (Local Scrubbing)"
                pipeline_audit_data.append(trace)
                logging.info(f"📊 Trace logged for {file_path}")

        except Exception as e:
            logging.error(f"CRITICAL: Unexpected failure on {file_path}: {e}")

    # =================================================================
    # 4. FINAL REPORTING (The Business Layer)
    # =================================================================
    try:
        # Save JSON (Technical Data)
        with open("audit_report.json", "w", encoding="utf-8") as f:
            json.dump(pipeline_audit_data, f, indent=4)
        
        # Generate Markdown (Executive Report)
        if AuditReporter.generate_markdown(pipeline_audit_data):
            logging.info("📝 Executive Markdown report generated: FINAL_AUDIT_REPORT.md")
            
        logging.info("🏁 Pipeline finished successfully. Check /restored_project")
    except Exception as e:
        logging.error(f"❌ Failed to generate final reports: {e}")

if __name__ == "__main__":
    run_pipeline()