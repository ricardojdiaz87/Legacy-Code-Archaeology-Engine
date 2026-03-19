import os
import google.generativeai as genai
from dotenv import load_dotenv
from rich.console import Console

# Professional terminal output handler
console = Console()

class CodeArchaeologist:
    """
    Main Analysis Engine for the Legacy Code Archaeology Project.
    Uses Google Gemini 2.5 Flash to perform deep static analysis on source code.
    """
    
    def __init__(self):
        """Initializes environment, API configuration, and model selection."""
        load_dotenv()
        self.api_key = os.getenv("GOOGLE_API_KEY")
        
        # Selected from your authorized list: High-speed, high-reasoning model
        self.model_name = "models/gemini-2.5-flash" 
        self._setup_connection()

    def _setup_connection(self):
        """
        Private: Configures the Gemini SDK and initializes the Generative Model.
        Raises:
            ValueError: If the API Key is missing from the .env file.
        """
        if not self.api_key:
            console.print("[bold red]❌ Error:[/bold red] GOOGLE_API_KEY not found in .env")
            raise ValueError("Missing API Key. Ensure your .env file is correctly configured.")
        
        # Authenticate with Google AI Studio
        genai.configure(api_key=self.api_key)
        
        # Initialize model with persistent system instructions
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=(
                "You are a Senior Software Archaeologist and Architect. "
                "Analyze legacy code for technical debt, security risks, and obsolete patterns. "
                "Always provide a 'Refactoring Roadmap' and a Complexity Score (1-10)."
            )
        )

    def list_available_models(self):
        """
        Diagnostic Tool: Scans and lists all models authorized for this API Key.
        Useful for debugging 404/Connectivity issues.
        """
        console.print("\n[bold blue]🔍 Scanning Authorized Models...[/bold blue]")
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    console.print(f"  • [green]Authorized:[/green] {m.name}")
        except Exception as e:
            console.print(f"[bold red]❌ Diagnostic Failed:[/bold red] {e}")

    def analyze_code(self, sanitized_code: str):
        """
        Sends the scrubbed code to the AI engine for expert review.
        Returns:
            str: The AI-generated archaeology report.
        """
        try:
            # We wrap the code in a structured prompt to ensure quality output
            prompt = (
                "Perform a deep archaeological excavation on the following code snippet. "
                "Identify hidden risks and propose modern alternatives.\n\n"
                f"CODE TO ANALYZE:\n{sanitized_code}"
            )
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            console.print(f"[bold red]❌ Analysis Engine Error:[/bold red] {e}")
            return None

if __name__ == "__main__":
    # Local Test & Diagnostic
    engine = CodeArchaeologist()
    console.print(f"[bold green]✔ Engine Initialized:[/bold green] Using {engine.model_name}")
    engine.list_available_models()