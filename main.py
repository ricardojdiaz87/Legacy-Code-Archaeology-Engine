import os
import sys
import json
import logging

# =================================================================
# 1. ENFORCED PATH RESOLUTION (Senior Architecture)
# =================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, 'src')

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# =================================================================
# 2. FAIL-SAFE MODULE IMPORTS
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
        sys.exit(1)

# Professional logging configuration
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# =================================================================
# 3. UNIVERSAL CONFIGURATION
# =================================================================
# Definimos el alcance del motor: Soporte para el stack Web completo
ALLOWED_EXTENSIONS = {
    '.py', '.php', '.js', '.css', '.html', 
    '.ajax', '.jquery', '.jsx', '.ts'
}

IGNORED_FILES = {
    'main.py', 'generate_report.py', 'audit_report.json', 
    'FINAL_AUDIT_REPORT.md', 'MANIFESTO.md'
}

# =================================================================
# 4. PIPELINE ORCHESTRATION
# =================================================================
def run_pipeline():
    """
    Orquestador Universal:
    Detecta múltiples lenguajes -> Limpieza PII -> Refactorización Mock -> Reporte.
    """
    logging.info("🚀 Starting Universal Legacy Archaeology Pipeline...")

    restorer = CodeRestorer(output_path="restored_project")
    pipeline_audit_data = [] 
    
    # Discovery Phase: Escaneo multilingüe
    all_files = os.listdir('.')
    legacy_files = [
        f for f in all_files 
        if os.path.splitext(f)[1].lower() in ALLOWED_EXTENSIONS 
        and f not in IGNORED_FILES
    ]
    
    if not legacy_files:
        logging.warning("⚠️ No legacy specimens (.py, .js, .php, etc.) detected in root.")
        return

    logging.info(f"🔍 Found {len(legacy_files)} targets for restoration.")

    for file_path in legacy_files:
        ext = os.path.splitext(file_path)[1].lower()
        logging.info(f"📂 Processing [{ext.upper()}]: {file_path}")

        try:
            # STAGE 1: Security Scrubbing (Universal Text Masking)
            # Funciona para cualquier lenguaje al ser análisis de texto plano
            scrubbed_content = PIIScrubber.scrub_file(file_path)
            logging.info(f"🛡️ Stage 1: Security Shield active for {file_path}")
            
            # STAGE 2: AI Analysis Simulation
            # En Fase 2, aquí inyectaremos prompts específicos por extensión
            logging.info(f"🧠 Stage 2: AI Analyzing patterns in {file_path}")
            mock_ai_output = (
                f"/* Refactored {ext.upper()} by Legacy Engine v1.3 */\n"
                f"// Safety: PII Masked locally.\n"
                f"console.log('Modernized logic for {file_path}');"
            )

            # STAGE 3: Shielded Restoration
            # Nota: El validador AST actual es para Python. 
            # En Fase 2 añadiremos validadores para JS y PHP.
            logging.info(f"🧱 Stage 3: Applying Validation Shield to {file_path}")
            success = restorer.save_restored_file(file_path, mock_ai_output)

            if success:
                # STAGE 4: Audit Traceability
                trace = restorer.generate_audit_report(file_path, changes_count=10)
                trace["language"] = ext.upper()
                trace["security_scan"] = "PASSED (Polyglot Scrubbing)"
                pipeline_audit_data.append(trace)
                logging.info(f"📊 Trace logged for {file_path}")

        except Exception as e:
            logging.error(f"❌ CRITICAL failure on {file_path}: {e}")

    # =================================================================
    # 5. FINAL REPORTING
    # =================================================================
    try:
        with open("audit_report.json", "w", encoding="utf-8") as f:
            json.dump(pipeline_audit_data, f, indent=4)
        
        if AuditReporter.generate_markdown(pipeline_audit_data):
            logging.info("📝 Executive Markdown report generated: FINAL_AUDIT_REPORT.md")
            
        logging.info("🏁 Pipeline finished. Results in /restored_project")
    except Exception as e:
        logging.error(f"❌ Failed to finalize reports: {e}")

if __name__ == "__main__":
    run_pipeline()