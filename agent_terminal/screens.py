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
    ("Voice Cloning (GPT-4o)", "VoiceCloningAgent", "gpt-4o"),
]


class AgentSelectionScreen(ModalScreen[tuple | None]):
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
            Label("Reference Audio Path", id="audio_path_label", classes="hidden"),
            Input(
                placeholder="/path/to/voice.wav",
                id="audio_path_input",
                classes="hidden",
            ),
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

            if agent_class_name == "VoiceCloningAgent":
                audio_path = self.query_one("#audio_path_input", Input).value
                if not audio_path:
                    self.bell()
                    return
                self.dismiss((agent_class_name, model_name, audio_path))
            else:
                self.dismiss((agent_class_name, model_name))
        else:
            self.dismiss(None)

    def on_select_changed(self, event: Select.Changed) -> None:
        """Enable or disable inputs based on agent selection."""
        model_input = self.query_one("#model_name_input", Input)
        audio_path_label = self.query_one("#audio_path_label")
        audio_path_input = self.query_one("#audio_path_input")

        selected_config = next(
            (config for config in AGENT_TYPES if config[0] == event.value), None
        )

        # Default state: hide all optional fields
        model_input.disabled = True
        model_input.clear()
        audio_path_label.add_class("hidden")
        audio_path_input.add_class("hidden")
        audio_path_input.clear()

        if not selected_config:
            return

        _, agent_class_name, _ = selected_config

        # Handle custom Ollama model input
        if event.value == "Ollama: Custom":
            model_input.disabled = False
            model_input.focus()

        # Handle voice cloning audio path input
        if agent_class_name == "VoiceCloningAgent":
            audio_path_label.remove_class("hidden")
            audio_path_input.remove_class("hidden")
            audio_path_input.focus()