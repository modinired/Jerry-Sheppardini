"""A widget to display agent conversation history."""

from textual.widgets import RichLog


class AgentView(RichLog):
    """A widget to display agent conversation history.

    This widget is a subclass of RichLog, configured for displaying
    chat-like conversations with auto-scrolling and highlighting.
    """

    def __init__(self, **kwargs) -> None:
        """Initialize the AgentView."""
        super().__init__(highlight=True, markup=True, **kwargs)
        self.border_title = "Agent Conversation"

    def add_message(self, sender: str, message: str, sender_style: str = "bold") -> None:
        """Add a message to the conversation view.

        Args:
            sender: The name of the message sender (e.g., "User", "Agent").
            message: The content of the message.
            sender_style: The Rich style to apply to the sender's name.
        """
        self.write(f"[{sender_style}]{sender}:[/{sender_style}] {message}")