# GEMINI.md Context Assistant

This script helps you manage your Gemini CLI context file (`GEMINI.md`) by translating natural language descriptions into the correct syntax. It now supports a modular system of "Pattern Packs" to easily share and load context for different technologies.

## New Feature: Pattern Packs

Instead of a single configuration file, the assistant now uses a `pattern_packs/` directory. Each `.csv` file in this directory is a "pack" of patterns for a specific tool or language (e.g., `terraform.csv`, `gcp.csv`).

-   **Load Packs:** Use the "Manage/Load Pattern Packs" option to select and merge packs into your active configuration.
-   **Customize:** Use "Add a Custom Pattern" to create your own patterns.
-   **Share:** Add new `.csv` files to the `pattern_packs/` directory to create and share new packs with your team.

Your personal, active configuration is stored in `patterns.csv`.

## Setup

1.  **Create Directory:**
    ```bash
    mkdir pattern_packs
    ```
    *(Populate this directory with your own `.csv` pack files. See the repository for examples.)*

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set API Key:**
    ```bash
    export GOOGLE_API_KEY="your_api_key_here"
    ```

## Usage

Run the script from your terminal:
```bash
python gemini_cli_config.py
