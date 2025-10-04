"""Abstract base class for all AI agents."""

from abc import ABC, abstractmethod


class Agent(ABC):
    """
    An abstract base class for an AI agent.

    All agents must implement the get_response method, which takes a user's
    prompt and returns the agent's response as a string.
    """

    @abstractmethod
    async def get_response(self, prompt: str) -> str:
        """
        Generates a response to a given prompt.

        Args:
            prompt: The user's input prompt.

        Returns:
            The agent's response as a string.
        """
        raise NotImplementedError