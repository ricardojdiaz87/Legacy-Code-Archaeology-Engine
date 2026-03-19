import os
import sys
import json
import logging

# 1. FORCE THE PROJECT ROOT INTO THE PATH
# This tells Python to look for 'src' first.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# 2. STARK ABSOLUTE IMPORTS
# We use 'src.folder.file' to be 100% explicit for Windows
try:
    from src.services.restorer import CodeRestorer
    from src.utils.scrubber import PIIScrubber
except ImportError as e:
    print(f"❌ CRITICAL STRUCTURAL ERROR: {e}")
    print("\n--- TROUBLESHOOTING CHECKLIST ---")
    print(f"1. Current Directory: {os.getcwd()}")
    print(f"2. Does this file exist? {os.path.join(BASE_DIR, 'src', 'utils', 'scrubber.py')}")
    print(f"3. Does this file exist? {os.path.join(BASE_DIR, 'src', 'utils', '__init__.py')}")
    sys.exit(1)

# Professional logging configuration
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def run_pipeline():
    logging.info("🚀 Starting Legacy Code Restoration Pipeline...")
    restorer = CodeRestorer(output_path="restored_project")
    pipeline_audit_data = []
    
    # Discovery: Finding legacy .py files
    legacy_files = [f for f in os.listdir('.') if f.endswith('.py') and f != 'main.py']
    
    for file_path in legacy_files:
        logging.info(f"📂 Processing Target: {file_path}")
        try:
            # Stage 1: Security Scrubbing
            scrubbed_content = PIIScrubber.scrub_file(file_path)
            logging.info(f"🛡️ Stage 1: Security Scan complete for {file_path}")
            
            # Stage 2: AI Simulation (Mocking the AI for now)
            mock_ai_output = "def restored_func():\n    return 'Refactored by Ricardo'\n"

            # Stage 3: Shielded Restoration
            success = restorer.save_restored_file(file_path, mock_ai_output)

            if success:
                trace = restorer.generate_audit_report(file_path, changes_count=15)
                trace["security_scan"] = "PASSED"
                pipeline_audit_data.append(trace)
                logging.info(f"📊 Trace logged for {file_path}")

        except Exception as e:
            logging.error(f"❌ Pipeline failure on {file_path}: {e}")

    # Final Audit Report
    report_path = "audit_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(pipeline_audit_data, f, indent=4)
    logging.info(f"🏁 Pipeline finished. Report saved: {report_path}")

if __name__ == "__main__":
    run_pipeline()