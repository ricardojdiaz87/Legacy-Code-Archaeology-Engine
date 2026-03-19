import os
from src.utils.security import SecurityScrubber
from src.core.analyzer import CodeArchaeologist
from rich.console import Console
from rich.panel import Panel

# Initialize the professional terminal console
console = Console()

def run_archaeology_session(file_path: str):
    """
    Orchestrates the complete analysis workflow:
    1. Input Handling -> 2. Local Security Scrubbing -> 3. AI Analysis -> 4. Reporting
    """
    
    # Initialize professional modules
    scrubber = SecurityScrubber()
    archaeologist = CodeArchaeologist()

    console.print(Panel.fit(
        "🏛️  [bold gold1]Legacy Code Archaeology Engine[/bold gold1]\n"
        "[italic]Starting automated excavation...[/italic]",
        border_style="blue"
    ))

    # Phase 1: File Ingestion
    if not os.path.exists(file_path):
        console.print(f"[bold red]Error:[/bold red] Target file '{file_path}' not found.")
        return

    console.print(f"[bold blue]Step 1:[/bold blue] Reading source file: [underscore]{file_path}[/underscore]")
    with open(file_path, "r", encoding="utf-8") as f:
        raw_code = f.read()

    # Phase 2: Local Security (The Shield)
    # We never send raw code to the cloud without local scrubbing first.
    console.print("[bold blue]Step 2:[/bold blue] Executing local Security Scrubber...")
    sanitized_code = scrubber.scrub_content(raw_code)

    # Phase 3: AI Analysis (The Brain)
    console.print("[bold blue]Step 3:[/bold blue] Sending sanitized code to Gemini 1.5 Pro...")
    
    # Define the specific analysis request
    analysis_query = (
        "Perform a deep archaeological analysis on this code. "
        "Identify technical debt, legacy patterns, and provide a refactoring roadmap.\n\n"
        f"CODE TO ANALYZE:\n{sanitized_code}"
    )
    
    try:
        response = archaeologist.model.generate_content(analysis_query)
        
        # Phase 4: Professional Reporting
        console.print("\n[bold green]📊 ARCHAEOLOGY ANALYSIS REPORT[/bold green]")
        console.print("-" * 40)
        console.print(response.text)
        console.print("-" * 40)
        console.print("[bold gold1]Excavation process completed successfully.[/bold gold1]")

    except Exception as e:
        console.print(f"[bold red]Analysis Failed:[/bold red] {str(e)}")

if __name__ == "__main__":
    # Point this to the file you want to analyze
    #target = "src/core/analyzer.py" 
    target = "legacy_sample.py" 
    run_archaeology_session(target)