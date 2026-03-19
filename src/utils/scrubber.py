import re
import logging

class PIIScrubber:
    """
    Local Security Layer: Masks sensitive information (PII) before AI analysis.
    """
    PATTERNS = {
        "api_key": r'(?:key|api|token|secret|password|passwd|pwd)[_-]?(?:[a-zA-Z0-9_\-\.\=\+]{16,})',
        "email": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        "ipv4": r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    }

    @staticmethod
    def mask_content(content: str) -> str:
        masked_content = content
        findings_count = 0
        
        for label, pattern in PIIScrubber.PATTERNS.items():
            matches = re.findall(pattern, masked_content, re.IGNORECASE)
            findings_count += len(matches)
            placeholder = f"[REDACTED_{label.upper()}]"
            masked_content = re.sub(pattern, placeholder, masked_content, flags=re.IGNORECASE)
        
        if findings_count > 0:
            logging.info(f"🛡️ Security Shield: {findings_count} sensitive data points masked locally.")
            
        return masked_content

    @staticmethod
    def scrub_file(file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return PIIScrubber.mask_content(content)
        except Exception as e:
            logging.error(f"❌ Error scrubbing file {file_path}: {e}")
            return ""