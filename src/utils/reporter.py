import os
import logging

class AuditReporter:
    """
    Business Intelligence Layer: Converts raw JSON audit data into 
    professional Markdown reports for stakeholders.
    """
    
    @staticmethod
    def generate_markdown(audit_data: list, output_file: str = "FINAL_AUDIT_REPORT.md"):
        if not audit_data:
            logging.warning("⚠️ No data available to generate report.")
            return

        header = "# 📜 Legacy Restoration Executive Summary\n\n"
        header += "> **Engine:** Legacy-Code-Archaeology v1.0-hardened\n"
        header += "> **Status:** Phase 1 Infrastructure Verified\n\n"
        
        table_header = "| File Name | Status | Impact Score | Security Scan | Version |\n"
        table_divider = "| :--- | :--- | :--- | :--- | :--- |\n"
        
        rows = ""
        total_impact = 0
        
        for entry in audit_data:
            icon = "✅" if entry.get("security_scan") == "PASSED (Local Scrubbing)" else "🔍"
            rows += f"| {entry['file']} | `{entry['status']}` | {entry['impact_score']} | {icon} PASSED | {entry['engine_version']} |\n"
            total_impact += entry['impact_score']

        footer = f"\n\n### 📊 Project Insights\n"
        footer += f"* **Total Files Processed:** {len(audit_data)}\n"
        footer += f"* **Accumulated Impact Score:** {total_impact} points\n"
        footer += f"\n---\n*Report generated automatically by the Restoration Pipeline.*"

        try:
            full_report = header + table_header + table_divider + rows + footer
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(full_report)
            return True
        except Exception as e:
            logging.error(f"❌ Failed to write Markdown report: {e}")
            return False