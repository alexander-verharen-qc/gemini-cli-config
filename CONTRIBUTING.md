# Contributing to GEMINI.md Assistant

First off, thank you for considering contributing! We're excited to see this tool grow with the help of the community. Every contribution, from a new Pattern Pack to a bug fix, is valuable.

This document provides guidelines for contributing to this project.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior.

## How Can I Contribute?

There are many ways to contribute, and all are welcome:

*   **Creating and improving Pattern Packs:** This is the easiest and one of the most impactful ways to contribute.
*   **Reporting bugs:** Help us make the tool more robust by identifying issues.
*   **Suggesting enhancements:** Have an idea for a new feature? Let's talk about it.
*   **Submitting code changes:** Fix a bug or implement a new feature.

## Your First Contribution: Pattern Packs

The core value of this tool comes from the shared knowledge within `pattern_packs/`. If you have a set of useful patterns for a specific tool, language, or workflow, we encourage you to share it!

### Creating a New Pattern Pack

1.  **Create a New File:** Inside the `pattern_packs/` directory, create a new file with a descriptive, lowercase name (e.g., `kubernetes.csv`, `docker.csv`).
2.  **Add the Header:** The first line of your file **must** be the CSV header:
    ```csv
    option,description,syntax
    ```
3.  **Add Your Patterns:** Add one pattern per row, following the format below.

### Pattern Format Explained

Each row in the CSV represents one pattern and has three columns:

1.  **`option`**: A short, unique, `kebab-case` name for the pattern (e.g., `k8s-get-pods`, `docker-build`). This is what the user will type to invoke the pattern.
2.  **`description`**: A clear, concise explanation of what the pattern does. Explain its purpose and the outcome for the user. This description is shown in the tool's "List" view.
3.  **`syntax`**: The exact `GEMINI.md` syntax.
    *   **Newlines:** Represent all newlines within the syntax with `\n`.
    *   **Quoting:** Enclose the entire syntax string in double quotes (`"`). If your syntax itself contains double quotes, escape them by doubling them up (`""`).

**Example:**

Let's say you want to create a pattern for a Kubernetes deployment:

```
pattern: k8s-get-pods {namespace}
  command: kubectl get pods -n {namespace}
```

The corresponding row in your `.csv` file would look like this:

```csv
k8s-get-pods,"Gets all pods from a specific Kubernetes namespace.","pattern: k8s-get-pods {namespace}\n  command: kubectl get pods -n {namespace}"
```

Once your pack is ready, submit it as a Pull Request!

## Reporting Bugs

*   **Check Existing Issues:** Before creating a new bug report, please check the [Issues](https://github.com/one-thd/reliability-engineering-prompts/issues) to see if the problem has already been reported.
*   **Be Descriptive:** Create an issue and provide a clear and concise description of the bug.
*   **Provide Steps to Reproduce:** Include the exact steps to reproduce the problem.
*   **Include Error Messages:** Paste the full traceback or error message you received.
*   **Mention Your Environment:** Include details about your operating system and Python version.

## Submitting Pull Requests

Ready to contribute code? Excellent!

1.  **Fork the Repository:** Create your own fork of the project.
2.  **Create a Feature Branch:** `git checkout -b feature/my-amazing-feature`
3.  **Set Up Your Environment:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Make Your Changes:** Add your feature or fix your bug.
5.  **Commit Your Changes:** Use clear and descriptive commit messages.
6.  **Push to Your Branch:** `git push origin feature/my-amazing-feature`
7.  **Open a Pull Request:** Submit a PR to the `main` branch of the original repository. Please provide a clear description of the changes, why they are needed, and a reference to any related issues.

Thank you for helping make this tool better for everyone!
