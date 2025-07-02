# GEMINI.md Assistant

**Your AI-Powered Assistant for the Gemini CLI**

This tool solves a critical problem for users of the Gemini CLI and other agentic tools: **keeping them context-aware.** An AI agent is only as powerful as the context you provide. This script makes building and sharing that context simple, collaborative, and fast.

## The Problem

Out of the box, the Gemini CLI has no knowledge of your specific projects, commands, or file structures. You make it smart by populating a `GEMINI.md` file with **patterns**.

However, manually creating and managing this file is:
*   **Tedious:** The syntax is simple but requires constant lookups and typing.
*   **Error-Prone:** A small typo can break a pattern.
*   **Not Shareable:** Every team member has to reinvent the wheel, creating their own patterns for the same shared tools (Terraform, GCP, Kubernetes, etc.). This "tribal knowledge" never gets centralized.

## The Solution: Pattern Packs

The GEMINI.md Assistant treats your CLI context as a **shareable knowledge base**.

The core concept is the **Pattern Pack**: a simple `.csv` file containing a collection of patterns for a specific tool or workflow (e.g., `terraform.csv`, `github.csv`).

This tool provides an interactive interface to:
1.  **Discover & Load** these shared Pattern Packs.
2.  **Create** your own custom patterns using natural language.
3.  **Safely Sync** your curated set of patterns to the global `~/.gemini/GEMINI.md` file that the Gemini CLI uses.

### Workflow at a Glance

```
           [ Shareable Pattern Packs ]
 ┌───────────────────────────────────────────────┐
 │  pattern_packs/                               │
 │   ├── terraform.csv  >─────────┐              │
 │   ├── gcp.csv        >─────┐   │              │
 │   └── github.csv     >──┐  │   │              │
 └─────────────────────────┘  │   │              │
                              ▼   ▼              │
                   ┌────────────────────┐        │
                   │ gemini_cli_config.py        │  <── You Are Here
                   └──────────┬─────────┘        │
                              |                  │ (Manage/Load Packs)
                              ▼                  │
                      [ Your Active Set ]        │
                   ┌────────────────────┐        │
                   │    patterns.csv    │────────┘
                   └────────────────────┘
                             |
                             | (Sync to Global)
                             ▼
              [ Gemini CLI's Brain ]
           ┌──────────────────────────┐
           │ ~/.gemini/GEMINI.md      │
           └──────────────────────────┘
```

## Key Features

*   **AI-Powered Creation:** Describe a new pattern in plain English ("a command to run terraform plan"), and the AI assistant will generate the correct syntax for you.
*   **Shareable & Modular:** Organize patterns into thematic "Pattern Packs" (`.csv` files) that can be version-controlled and shared across a team.
*   **Safe Global Sync:** The tool intelligently merges your active patterns with your existing `~/.gemini/GEMINI.md`, preserving any manual additions you've made.
*   **Interactive UI:** A clean, terminal-based interface makes managing patterns fast and intuitive.

## Setup

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/one-thd/reliability-engineering-prompts.git
    cd reliability-engineering-prompts/gemini_cli_config
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set Your API Key:**
    The script requires a Google AI API key.
    ```bash
    # For macOS / Linux
    export GOOGLE_API_KEY="your_api_key_here"

    # For Windows
    set GOOGLE_API_KEY="your_api_key_here"
    ```

## Usage

Simply run the script from the project directory:

```bash
python gemini_cli_config.py
```

You will be presented with a menu. The typical workflow is:

1.  **`Manage/Load Pattern Packs`**: Start here. Select the packs relevant to your work (e.g., `terraform.csv`, `gcp.csv`) to build your active configuration.
2.  **`Add a Custom Pattern`**: Use the AI assistant to create any personal or project-specific patterns not found in a shared pack.
3.  **`List All Active Patterns`**: Check your currently loaded set of patterns.
4.  **`Sync Active Patterns to Global...`**: This is the final step. It takes all your active patterns and intelligently updates the `GEMINI.md` file that the Gemini CLI reads from.

## Contributing

Contributions are what make open-source projects thrive! Whether it's a new Pattern Pack, a bug fix, or a feature suggestion, your help is welcome. Please read our **[CONTRIBUTING.md](CONTRIBUTING.md)** to get started.

## License

This project is licensed under the MIT License.
