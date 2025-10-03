# Agent Terminal

Agent Terminal is a local, terminal-based application designed for interacting with multiple AI agents simultaneously. It provides a sleek, tabbed interface reminiscent of modern terminals, allowing users to manage different agent sessions in one window.

## Features

*   **Tabbed Interface**: Each agent session lives in its own tab.
*   **Add/Remove Tabs**: Dynamically add new agent tabs (`Ctrl+T`) and remove the active one (`Ctrl+W`).
*   **Sleek UX**: Styled with a modern, dark theme for a comfortable user experience.
*   **Extensible Architecture**: Built with `textual`, making it easy to add new features and integrate real LLMs.

## Prerequisites

*   Python 3.9+

## Installation

1.  **Clone the repository (or create the files as provided).**

2.  **Create a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -e .
    ```
    The `-e` flag installs the package in "editable" mode, which is useful for development.

## Local LLM Setup (Optional)

This application supports local language models via Ollama. To use this feature, you must first install and run the Ollama service on your machine.

1.  **Install Ollama**: Follow the official instructions at [https://ollama.com](https://ollama.com).
2.  **Pull a Model**: Before using a model in the app, you must pull it from the Ollama registry. For example, to use Llama 3, run:
    ```bash
    ollama pull llama3
    ```

The Ollama application must be running in the background for the local agent to work.

## OpenAI API Configuration (Optional)

This application uses the OpenAI API to provide AI responses. Before running, you must set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

## Usage

To run the application, execute the following command from the root of the project:

```bash
python3 agent_terminal/app.py
```

### Key Bindings

*   `Ctrl+T`: Add a new agent tab.
*   `Ctrl+W`: Close the active agent tab.
*   `q`: Quit the application.

## Testing

To run the test suite, you first need to install the development dependencies:

```bash
pip install -e '.[dev]'
```

Then, run Pytest:

```bash
pytest
```

## Validation

*   **Linting & Formatting**: This project uses `ruff` for linting and formatting.
*   **Type Safety**: The codebase includes type hints and is checked for correctness.
*   **Tests**: The initial test suite ensures the application can be instantiated and mounted without runtime errors.

## Risks & Mitigations

*   **Initial Version**: This is the first version and currently uses a simple "Echo Agent." The core focus has been on building a robust and production-ready UI foundation.
*   **Mitigation**: The architecture is designed for extension. Future work will involve creating an agent protocol and integrating local and remote LLMs.

## Backward Compatibility

This is the first release, so there are no backward compatibility concerns. Future breaking changes will be documented in release notes.