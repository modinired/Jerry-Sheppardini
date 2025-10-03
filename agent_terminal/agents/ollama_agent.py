"""An agent that uses a local Ollama service to generate responses."""

import ollama
from .base import Agent


class OllamaAgent(Agent):
    """An agent that uses a local Ollama service to generate responses."""

    def __init__(self, model: str = "llama3"):
        """
        Initializes the OllamaAgent.

        Args:
            model: The name of the Ollama model to use (e.g., "llama3", "codellama").
                   This model must be pulled via `ollama pull <model_name>` first.
        """
        self.model = model
        # We will check for Ollama service availability in the get_response method
        # to provide a more dynamic error message in the chat window.

    async def get_response(self, prompt: str) -> str:
        """
        Fetches a response from the local Ollama model.

        Args:
            prompt: The user's input prompt.

        Returns:
            The AI's response as a string, or an error message if the service
            is unavailable or the model call fails.
        """
        try:
            # The ollama library's async client needs to be created inside an
            # async function's context.
            client = ollama.AsyncClient()
            response = await client.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
            )
            return response["message"]["content"]
        except ollama.ResponseError as e:
            if "model not found" in e.error:
                return (
                    f"[bold red]Error: Model '{self.model}' not found.[/bold red]\n\n"
                    f"Please pull it first by running: `ollama pull {self.model}`"
                )
            return f"[bold red]An Ollama API error occurred: {e.error}[/bold red]"
        except Exception as e:
            # This broad exception often catches connection errors.
            return (
                "[bold red]Error: Could not connect to Ollama service.[/bold red]\n\n"
                "Please ensure the Ollama application is running on your local machine."
            )