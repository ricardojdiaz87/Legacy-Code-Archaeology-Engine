import os
import google.generativeai as genai
from dotenv import load_dotenv
from rich.console import Console

# Initialize professional console for styled terminal output
console = Console()

class CodeArchaeologist:
    """
    Main analysis engine for the Legacy Code Archaeology Engine.
    Handles secure AI connectivity, system instructions, and technical debt mapping.
    """
    
    def __init__(self):
        """Initialize environment variables and model configuration."""
        load_dotenv()
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.model_name = "gemini-1.5-pro"  # Selected for its massive context window
        self._setup_connection()

    def _setup_connection(self):
        """
        Private: Configures authentication with Google AI Studio (Vertex AI compatible).
        Raises:
            ValueError: If GOOGLE_API_KEY is not found in the environment.
        """
        if not self.api_key:
            console.print("[bold red]❌ Error:[/bold red] GOOGLE_API_KEY not detected in .env file")
            raise ValueError("Missing API Key. Please check your .env configuration.")
        
        # Authenticate the SDK
        genai.configure(api_key=self.api_key)
        
        # Define the System Instruction to lock the AI into a Professional Architect persona
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=(
                "You are a Senior Software Archaeologist and Architect. "
                "Your mission is to perform deep static analysis on legacy systems. "
                "Identify technical debt, security vulnerabilities (PII/Secrets), "
                "and obsolete architectural patterns. Always prioritize remediation "
                "steps and provide a Complexity Score (1-10)."
            )
        )

    def test_connection(self):
        """
        Verifies if the engine can successfully communicate with the LLM.
        Returns:
            bool: True if connection is established, False otherwise.
        """
        try:
            # Low-token pulse to verify heartbeat
            response = self.model.generate_content("Archaeology Engine: Heartbeat check.")
            console.print(f"[bold green]✔ Engine Online:[/bold green] {self.model_name} responded successfully.")
            return True
        except Exception as e:
            console.print(f"[bold red]❌ Connection Failed:[/bold red] {str(e)}")
            return False

if __name__ == "__main__":
    # Local execution for connectivity testing
    engine = CodeArchaeologist()
    engine.test_connection()