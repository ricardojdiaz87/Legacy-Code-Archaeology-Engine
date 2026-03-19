import os
import ast
import logging

class CodeRestorer:
    def __init__(self, output_path: str = "restored_project"):
        self.output_path = output_path
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

    def validate_python_syntax(self, code: str) -> bool:
        try:
            ast.parse(code)
            return True
        except SyntaxError as e:
            logging.error(f"🚨 Syntax Error Detected: {e}")
            return False

    def save_restored_file(self, original_path: str, restored_code: str) -> bool:
        if not self.validate_python_syntax(restored_code):
            return False

        file_name = os.path.basename(original_path)
        target_path = os.path.join(self.output_path, file_name)

        with open(target_path, "w", encoding="utf-8") as f:
            f.write(restored_code)
        return True

    def generate_audit_report(self, original_path: str, changes_count: int) -> dict:
        return {
            "file": original_path,
            "status": "RESTORED",
            "impact_score": round(changes_count * 1.5, 2),
            "engine_version": "1.0.0-hardened"
        }