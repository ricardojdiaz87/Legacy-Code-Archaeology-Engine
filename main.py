import os
import time
import sys
from dotenv import load_dotenv
from src.utils.security import SecurityScrubber
from src.core.analyzer import CodeArchaeologist
from src.services.restorer import CodeRestorer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# --- CONFIGURACIÓN DE ENTORNO ---
load_dotenv()
console = Console()

def estimate_token_cost(files):
    """Calcula el costo proyectado de la operación (FinOps)"""
    input_price = float(os.getenv("INPUT_TOKEN_PRICE", 0.10))
    total_chars = 0
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            total_chars += len(f.read())
    
    est_tokens = total_chars / 4
    est_cost = (est_tokens / 1000000) * input_price
    
    table = Table(title="💰 FinOps: Token & Cost Intelligence")
    table.add_column("Métrica", style="cyan")
    table.add_column("Valor", style="magenta")
    table.add_row("Archivos Encontrados", str(len(files)))
    table.add_row("Tokens Estimados", f"{int(est_tokens):,}")
    table.add_row("Costo Est. Proveedor", f"${est_cost:.6f} USD")
    table.add_row("Estado de Cuota", "[bold green]FREE TIER ELIGIBLE[/bold green]")
    
    console.print(table)
    return est_tokens

def get_all_python_files(root_dir):
    """Escaneo recursivo omitiendo carpetas de sistema y entorno"""
    py_files = []
    excluded = {'venv', '.venv', '__pycache__', '.git', 'restored_project', 'build', 'dist'}
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in excluded]
        for file in files:
            if file.endswith(".py") and file != "main.py":
                py_files.append(os.path.join(root, file))
    return py_files

def run_project_archaeology():
    """Flujo principal con manejo de resiliencia (Circuit Breaker)"""
    scrubber = SecurityScrubber()
    engine = CodeArchaeologist()
    restorer = CodeRestorer(engine)
    output_dir = "restored_project"
    
    # ESTADO DEL CIRCUITO
    is_circuit_open = False 

    console.print(Panel.fit(
        "🏛️  [bold gold1]Resilient Architecture: Circuit Breaker Enabled[/bold gold1]\n"
        "[dim]Monitoring API Health & Quota Limits[/dim]"
    ))
    
    all_files = get_all_python_files(".")
    if not all_files:
        console.print("[bold red]No se encontraron archivos Python para procesar.[/bold red]")
        return
    
    estimate_token_cost(all_files)

    # --- FASE 1: LIMPIEZA DE SEGURIDAD (LOCAL) ---
    console.print(f"\n[bold blue]Step 1:[/bold blue] Scrubbing PII & Data Masking...")
    full_context = ""
    for file in all_files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
                sanitized = scrubber.scrub_content(content)
                full_context += f"\n\n--- FILE: {file} ---\n{sanitized}"
        except Exception as e:
            console.print(f"[yellow]⚠️ Error leyendo {file}: {e}[/yellow]")

    # --- FASE 2: ANÁLISIS GLOBAL (Punto de Control del Circuito) ---
    console.print("[bold blue]Step 2:[/bold blue] Generating Global Archaeology Intelligence...")
    project_prompt = f"Analyze this project context and define core business rules:\n{full_context}"
    
    try:
        report = engine.model.generate_content(project_prompt)
        with open("ARCHAEOLOGY_REPORT.md", "w", encoding="utf-8") as f:
            f.write(report.text)
    except Exception as e:
        # Si la API falla por cuota (429), abrimos el circuito para proteger el sistema
        if "429" in str(e) or "ResourceExhausted" in str(e):
            is_circuit_open = True
            console.print(Panel(
                f"[bold red]🚨 CIRCUIT BREAKER TRIPPED![/bold red]\n"
                f"API Quota Exhausted. Aborting Step 3 to prevent system stress.\n"
                f"Error: {e}", title="Safety Protocol"
            ))
        else:
            console.print(f"[bold red]Critical Error:[/bold red] {e}")
            return

    # --- FASE 3: RESTAURACIÓN (Solo si el circuito está CERRADO) ---
    if is_circuit_open:
        console.print("\n[bold yellow]⏭️  Skipping Step 3:[/bold yellow] Circuit is OPEN. Manual reset required after quota reset.")
        sys.exit(1)

    console.print(f"\n[bold blue]Step 3:[/bold blue] Restoring code to [yellow]'{output_dir}/'[/yellow]...")
    for file in all_files:
        relative_path = os.path.relpath(file, ".")
        save_path = os.path.join(output_dir, relative_path)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            restored = restorer.restore_file(file, content)
            
            if restored:
                # Limpiar posibles artefactos de Markdown de la IA
                clean_code = restored.replace("```python", "").replace("```", "").strip()
                with open(save_path, "w", encoding="utf-8") as out_f:
                    out_f.write(clean_code)
                console.print(f"  ✨ [green]Restored:[/green] {relative_path}")
        
        # Throttling preventivo para no saturar la cuenta gratuita
        time.sleep(1.5)

    console.print(f"\n[bold green]🏁 ARCHAEOLOGY PROCESS COMPLETE![/bold green]")

if __name__ == "__main__":
    run_project_archaeology()