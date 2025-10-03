"""An agent that uses the OpenAI API to generate responses."""

import os
from openai import AsyncOpenAI, OpenAIError
from .base import Agent


class OpenAIAgent(Agent):
    """An agent that uses the OpenAI API to generate responses."""

    def __init__(self, model: str = "gpt-4o"):
        """
        Initializes the OpenAIAgent.

        Args:
            model: The OpenAI model to use (e.g., "gpt-4o", "gpt-3.5-turbo").

        Raises:
            ValueError: If the OPENAI_API_KEY environment variable is not set.
        """
        self.model = model
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            # This error will be caught during agent creation to provide a
            # graceful message to the user in the UI.
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        self.client = AsyncOpenAI(api_key=api_key)

    async def get_response(self, prompt: str) -> str:
        """
        Fetches a response from the specified OpenAI model.

        Args:
            prompt: The user's input prompt.

        Returns:
            The AI's response as a string, or an error message if the API
            call fails.
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=1500,
            )
            if response.choices:
                return response.choices[0].message.content or "No response from AI."
            return "The AI returned an empty response."
        except OpenAIError as e:
            return f"[bold red]An OpenAI API error occurred: {e}[/bold red]"
        except Exception as e:
            return f"[bold red]An unexpected error occurred: {e}[/bold red]"