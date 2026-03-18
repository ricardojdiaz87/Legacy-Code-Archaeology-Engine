import re
from rich.console import Console

console = Console()

class SecurityScrubber:
    """
    Local Security Layer to sanitize legacy code before cloud analysis.
    Identifies and masks sensitive data like API Keys, Emails, and Credentials.
    """

    def __init__(self):
        # Patterns for common sensitive data (RegEx)
        self.patterns = {
            "api_key": r"(?i)(api_key|secret|token|password|auth|pwd)[\s]*[:=>]+[\s]*['\"]([^'\"]+)['\"]",
            "email": r"[\w\.-]+@[\w\.-]+\.\w+",
            "ipv4": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
        }

    def scrub_content(self, raw_code: str) -> str:
        """
        Scans and replaces sensitive patterns with high-visibility placeholders.
        Returns:
            str: The sanitized code ready for AI Ingestion.
        """
        sanitized_code = raw_code
        
        for label, pattern in self.patterns.items():
            matches = re.findall(pattern, sanitized_code)
            if matches:
                console.print(f"[bold yellow]⚠ Security Alert:[/bold yellow] Found {len(matches)} potential {label}(s). Masking...")
                sanitized_code = re.sub(pattern, f"[REDACTED_{label.upper()}]", sanitized_code)
        
        return sanitized_code

if __name__ == "__main__":
    # Local Test: Verifying that the scrubber works before committing
    test_code = 'db_pass = "super-secret-123"; admin_email = "ricardo@example.com";'
    scrubber = SecurityScrubber()
    clean_code = scrubber.scrub_content(test_code)
    
    print("\n--- Original Code ---")
    print(test_code)
    print("\n--- Sanitized Code ---")
    print(clean_code)