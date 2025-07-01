import os
import csv
import json
import google.generativeai as genai
import questionary
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax

# --- Configuration ---
PATTERNS_FILE = 'patterns.csv'
PATTERN_PACKS_DIR = 'pattern_packs'
GLOBAL_GEMINI_MD_PATH = os.path.expanduser("~/.gemini/GEMINI.md")
console = Console()

# --- AI Model Setup ---
try:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        console.print("[bold red]Error: GOOGLE_API_KEY environment variable not set.[/bold red]")
        exit()
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
except Exception as e:
    console.print(f"[bold red]Error initializing Google AI: {e}[/bold red]")
    exit()

# --- Core Functions ---

def load_patterns(filepath=PATTERNS_FILE):
    """Loads patterns from a given CSV file path, cleaning up malformed rows."""
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            patterns = []
            for row in reader:
                # THE FIX: If a row has more columns than the header, DictReader
                # adds them under a 'None' key. We must remove it.
                if None in row:
                    del row[None]
                patterns.append(row)
            return patterns
    except (IOError, csv.Error) as e:
        console.print(f"[bold red]Error reading {filepath}: {e}[/bold red]")
        return []

def save_patterns(patterns):
    """Saves the active patterns to the main patterns.csv file."""
    try:
        with open(PATTERNS_FILE, 'w', newline='', encoding='utf-8') as f:
            if not patterns:
                f.write("option,description,syntax\n")
                return
            writer = csv.DictWriter(f, fieldnames=['option', 'description', 'syntax'])
            writer.writeheader()
            writer.writerows(patterns)
    except IOError as e:
        console.print(f"[bold red]Error writing to {PATTERNS_FILE}: {e}[/bold red]")

# --- Pattern Pack Management ---

def discover_pattern_packs():
    """Finds all .csv files in the pattern_packs directory."""
    if not os.path.isdir(PATTERN_PACKS_DIR):
        console.print(f"[yellow]Pattern pack directory '{PATTERN_PACKS_DIR}/' not found. Creating it.[/yellow]")
        os.makedirs(PATTERN_PACKS_DIR)
        return []
    
    packs = [f for f in os.listdir(PATTERN_PACKS_DIR) if f.endswith('.csv')]
    return packs

def manage_pattern_packs(active_patterns):
    """UI for loading patterns from available packs into the active set."""
    console.print(Panel("Load patterns from shareable packs into your active configuration.", 
                        title="[bold]Manage Pattern Packs[/bold]", border_style="cyan"))
    
    packs = discover_pattern_packs()
    if not packs:
        console.print(f"[yellow]No pattern packs found in '{PATTERN_PACKS_DIR}/'.[/yellow]")
        console.print("Add themed CSV files like 'terraform.csv' to that directory to get started.")
        return

    selected_packs = questionary.checkbox(
        "Select pattern packs to load (space to select, enter to confirm):",
        choices=packs
    ).ask()

    if not selected_packs:
        console.print("[yellow]No packs selected. Operation cancelled.[/yellow]")
        return

    loaded_count = 0
    active_patterns_dict = {p['option']: p for p in active_patterns}

    for pack_name in selected_packs:
        pack_path = os.path.join(PATTERN_PACKS_DIR, pack_name)
        new_patterns = load_patterns(pack_path)
        for pattern in new_patterns:
            active_patterns_dict[pattern['option']] = pattern
            loaded_count += 1
        console.print(f"  [green]•[/green] Merged [bold]{len(new_patterns)}[/bold] patterns from [cyan]{pack_name}[/cyan]")
    
    updated_patterns = list(active_patterns_dict.values())
    
    save_patterns(updated_patterns)
    console.print(f"\n[bold green]✅ Success![/bold green] Your active configuration has been updated. You now have {len(updated_patterns)} total patterns.")
    
    return updated_patterns

# --- Main Application Loop ---

def main():
    """Main function to run the application."""
    console.print(Panel("[bold yellow]GEMINI.md Assistant[/bold yellow] - Your AI-powered context manager", expand=False))
    
    active_patterns = load_patterns()
    
    while True:
        console.print("")
        menu_title = f"What would you like to do? ({len(active_patterns)} active patterns)"
        
        action = questionary.select(
            menu_title,
            choices=[
                "Manage/Load Pattern Packs",
                "Add a Custom Pattern",
                "List All Active Patterns",
                "Sync Active Patterns to Global ~/.gemini/GEMINI.md",
                "Exit"
            ]
        ).ask()

        if action == "Manage/Load Pattern Packs":
            updated_patterns = manage_pattern_packs(active_patterns)
            if updated_patterns is not None:
                active_patterns = updated_patterns
        elif action == "Add a Custom Pattern":
            add_new_pattern(active_patterns)
        elif action == "List All Active Patterns":
            list_all_patterns(active_patterns)
        elif action == "Sync Active Patterns to Global ~/.gemini/GEMINI.md":
            sync_global_gemini_md(active_patterns)
        elif action == "Exit" or action is None:
            save_patterns(active_patterns)
            console.print("[bold]Goodbye![/bold]")
            break
            
# --- All other functions ---

def list_all_patterns(patterns):
    if not patterns:
        console.print("[yellow]No active patterns found. Load a pack or add a custom one![/yellow]")
        return
    table = Table(title="Current Active Patterns")
    table.add_column("Option", style="cyan", no_wrap=True)
    table.add_column("Description", style="magenta")
    table.add_column("Syntax", style="green")
    for p in patterns:
        table.add_row(p['option'], p['description'], p['syntax'].replace('\\n', '\n'))
    console.print(table)

def sync_global_gemini_md(managed_patterns):
    console.print(Panel(f"This will merge your active patterns with the global file at:\n[cyan]{GLOBAL_GEMINI_MD_PATH}[/cyan]", 
                        title="[bold]Sync with Global GEMINI.md[/bold]", border_style="yellow"))
    if not managed_patterns:
        console.print("[yellow]No active patterns to sync. Load some first![/yellow]")
        return
    managed_syntax_set = {p['syntax'].replace('\\n', '\n').strip() for p in managed_patterns}
    unmanaged_blocks = []
    if os.path.exists(GLOBAL_GEMINI_MD_PATH):
        try:
            with open(GLOBAL_GEMINI_MD_PATH, 'r', encoding='utf-8') as f:
                content = f.read()
                existing_blocks = [block.strip() for block in content.split('\n\n') if block.strip()]
                for block in existing_blocks:
                    if block.startswith("#"): continue
                    if block.strip() not in managed_syntax_set:
                        unmanaged_blocks.append(block)
        except IOError as e:
            console.print(f"[bold red]Could not read global GEMINI.md file: {e}[/bold red]")
            return
    console.print("\n[bold]Sync Preview:[/bold]")
    if unmanaged_blocks:
        unmanaged_table = Table(title="[yellow]Unmanaged Patterns (will be preserved)[/yellow]")
        unmanaged_table.add_column("Existing Syntax Found in your GEMINI.md")
        for block in unmanaged_blocks: unmanaged_table.add_row(block)
        console.print(unmanaged_table)
    else:
        console.print("[gray50]No unmanaged patterns found in your global file.[/gray50]")
    managed_table = Table(title="[green]Active Patterns (will be added/synced)[/green]")
    managed_table.add_column("Option", style="cyan")
    managed_table.add_column("Syntax", style="green")
    for p in managed_patterns: managed_table.add_row(p['option'], p['syntax'].replace('\\n', '\n'))
    console.print(managed_table)
    confirm = questionary.confirm(f"Proceed with updating {GLOBAL_GEMINI_MD_PATH}?").ask()
    if not confirm:
        console.print("[yellow]Sync cancelled.[/yellow]")
        return
    header = [
        "#####################################################################",
        "# This file is managed by the GEMINI.md Assistant.                  #",
        "# Unmanaged patterns are preserved, managed patterns are synced.    #",
        "#####################################################################\n",
    ]
    final_content_parts = header + unmanaged_blocks + [p['syntax'].replace('\\n', '\n') for p in managed_patterns]
    final_content = "\n\n".join(final_content_parts)
    try:
        os.makedirs(os.path.dirname(GLOBAL_GEMINI_MD_PATH), exist_ok=True)
        with open(GLOBAL_GEMINI_MD_PATH, 'w', encoding='utf-8') as f:
            f.write(final_content)
        console.print(f"\n[bold green]✅ Success![/bold green] Your global `{os.path.basename(GLOBAL_GEMINI_MD_PATH)}` has been updated.")
    except IOError as e:
        console.print(f"[bold red]Error writing to global GEMINI.md file: {e}[/bold red]")
        
def add_new_pattern(patterns):
    console.print(Panel("[bold]Add a Custom Pattern[/bold]\nThis will be added to your active patterns list.", title="[cyan]Input[/cyan]", border_style="cyan"))
    description = questionary.text("Your description:").ask()
    if not description: return
    conversation_history = [description]
    while True:
        ai_response_text = get_ai_suggestion("\n".join(conversation_history))
        try:
            suggestion = json.loads(ai_response_text)
            console.print(Panel(f"[bold]Option:[/] {suggestion.get('option', 'N/A')}\n[bold]Description:[/] {suggestion.get('description', 'N/A')}\n\n[bold]Generated Syntax:[/]", title="[green]AI Suggestion[/green]", border_style="green", expand=False))
            console.print(Syntax(suggestion.get('syntax', '').replace('\\n', '\n'), "markdown", theme="monokai", line_numbers=True))
            confirm = questionary.confirm("Do you want to save this custom pattern?").ask()
            if confirm:
                patterns_dict = {p['option']: p for p in patterns}
                patterns_dict[suggestion['option']] = suggestion
                patterns[:] = list(patterns_dict.values())
                save_patterns(patterns)
                console.print("[bold green]👍 Custom pattern saved to your active list![/bold green]")
            else:
                console.print("[yellow]Operation cancelled.[/yellow]")
            break
        except json.JSONDecodeError:
            if "Error: API call failed" in ai_response_text: console.print(f"[bold red]{ai_response_text}[/bold red]"); break
            console.print(Panel(ai_response_text, title="[yellow]AI Clarification[/yellow]", border_style="yellow"))
            more_info = questionary.text("Your response:").ask()
            if not more_info: console.print("[yellow]Operation cancelled.[/yellow]"); break
            conversation_history.append(f"User's clarification: {more_info}")
        except Exception as e:
            console.print(f"[bold red]An unexpected error occurred: {e}[/bold red]"); break

def get_ai_suggestion(user_description: str):
    system_prompt = """
    You are an expert assistant for the Gemini Command Line Interface (CLI). 
    Your goal is to help users create patterns for their GEMINI.md context file by translating their natural language descriptions.
    Your tasks:
    1. Analyze the user's request.
    2. If the request is ambiguous or missing key information (like a name for the 'option'), your response should be a single, concise clarifying question. Do NOT generate JSON if you need to ask a question.
    3. Once the request is clear, generate a JSON object with three keys: "option", "description", and "syntax".
    GEMINI.md Syntax Rules:
    - `pattern:` defines a reusable template with placeholders like {name}.
    - `file:` points to a file path, which can use placeholders.
    - `command:` defines a command to be run.
    - Use `\n` for newlines in the JSON 'syntax' value.
    Example of a good final output (DO NOT ask a question here):
    {
      "option": "python-service",
      "description": "Finds the main file and test file for a Python service.",
      "syntax": "pattern: python-service {name}\\n  file: src/services/{name}.py\\n  file: tests/test_{name}.py"
    }
    Example of a good clarifying question (DO NOT output JSON here):
    "That sounds like a common pattern. What would you like to name the option? For example, 'docker-service' or 'container-run'?"
    IMPORTANT: Respond ONLY with a valid JSON object or ONLY with a clarifying question. Do not add any other text.
    """
    with console.status("[bold cyan]AI is thinking...[/bold cyan]", spinner="dots"):
        try:
            response = model.generate_content([system_prompt, f"User's request: {user_description}"])
            clean_response = response.text.strip()
            if clean_response.startswith("```json"): clean_response = clean_response[7:-3].strip()
            return clean_response
        except Exception as e:
            return f"Error: API call failed: {e}"

if __name__ == "__main__":
    main()
