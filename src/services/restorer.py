import time
import os
from rich.console import Console

# Initialize console for high-quality terminal output
console = Console()

class CodeRestorer:
    """
    Service responsible for transforming legacy code into production-grade 
    code following Clean Code, SOLID principles, and PEP8 standards.
    """
    
    def __init__(self, engine):
        """
        Injected AI Engine (CodeArchaeologist) to perform generation requests.
        """
        self.engine = engine 

    def restore_file(self, file_path, original_content, max_retries=3):
        """
        Sends code to AI for professional restoration.
        Implements aggressive Exponential Backoff to handle Google's Free Tier limits.
        """
        prompt = (
            "TASK: Professional Code Restoration.\n"
            "1. Remove all redundant/nonsense comments.\n"
            "2. Use professional naming conventions (PEP8).\n"
            "3. Add Type Hinting to all functions and classes.\n"
            "4. Fix inefficient logic while maintaining business rules.\n"
            "5. Ensure NO secrets or PII are hardcoded.\n\n"
            f"ORIGINAL CODE ({file_path}):\n{original_content}"
        )
        
        for attempt in range(max_retries):
            try:
                # Attempt content generation
                response = self.engine.model.generate_content(prompt)
                return response.text
                
            except Exception as e:
                error_msg = str(e)
                
                # Handle Rate Limit (429) or Quota Exhausted
                if "429" in error_msg or "quota" in error_msg.lower():
                    # Cooling strategy: 
                    # 65 seconds ensures the 'Requests Per Minute' counter resets.
                    wait_time = 65 if attempt == 0 else 120 
                    
                    console.print(f"[yellow]⚠️  Quota limit hit in {file_path}. Cooling down for {wait_time}s (Attempt {attempt + 1}/{max_retries})...[/yellow]")
                    time.sleep(wait_time)
                    continue # Retry the same file after waiting
                
                # Handle other potential errors (network, auth, etc.)
                console.print(f"[bold red]❌ Restoration Error in {file_path}:[/bold red] {e}")
                return None
        
        # Final failure after all retries
        console.print(f"[bold red]🚫 Failed to restore {file_path} after multiple cooling attempts.[/bold red]")
        return None