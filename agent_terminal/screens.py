"""UI Screens for the Agent Terminal application."""

from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Select

# A registry of available agent configurations.
# Each tuple contains: (Display Name, AgentClassName, default_model_or_None)
AGENT_TYPES = [
    ("OpenAI: GPT-4o", "OpenAIAgent", "gpt-4o"),
    ("OpenAI: GPT-3.5 Turbo", "OpenAIAgent", "gpt-3.5-turbo"),
    ("Ollama: Llama 3", "OllamaAgent", "llama3"),
    ("Ollama: Custom", "OllamaAgent", None),  # Allows user to specify a model
]


class AgentSelectionScreen(ModalScreen[tuple[str, str] | None]):
    """A modal screen for selecting and configuring a new AI agent."""

    def compose(self) -> ComposeResult:
        """Create the UI elements for the agent selection screen."""
        yield Grid(
            Label("Select Agent Type", id="agent_select_label"),
            Select(
                [(name, name) for name, _, _ in AGENT_TYPES],
                prompt="Choose an agent...",
                id="agent_select",
            ),
            Label("Model Name (if custom)", id="model_name_label"),
            Input(placeholder="e.g., codellama", id="model_name_input", disabled=True),
            Button("Create", variant="primary", id="create_button"),
            Button("Cancel", variant="default", id="cancel_button"),
            id="agent_selection_grid",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events to create or cancel."""
        if event.button.id == "create_button":
            select = self.query_one(Select)
            if not select.value:
                self.bell()
                return

            selected_config = next(
                (config for config in AGENT_TYPES if config[0] == select.value), None
            )
            if not selected_config:
                self.bell()
                return

            _, agent_class_name, default_model = selected_config
            model_name = default_model
            if default_model is None:  # This is the "Ollama: Custom" case
                model_name = self.query_one("#model_name_input", Input).value

            if not model_name:
                self.bell()
                return

            self.dismiss((agent_class_name, model_name))
        else:
            self.dismiss(None)

    def on_select_changed(self, event: Select.Changed) -> None:
        """Enable the model name input only for the 'Ollama: Custom' option."""
        model_input = self.query_one("#model_name_input", Input)
        if event.value == "Ollama: Custom":
            model_input.disabled = False
            model_input.focus()
        else:
            model_input.disabled = True
            model_input.clear()