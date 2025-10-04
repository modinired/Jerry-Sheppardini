"""The main application for the Agent Terminal."""

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Header, Input, TabbedContent, TabPane

from agent_terminal.agents.base import Agent
from agent_terminal.agents.openai_agent import OpenAIAgent
from agent_terminal.agents.ollama_agent import OllamaAgent
from agent_terminal.screens import AgentSelectionScreen
from agent_terminal.widgets.agent_view import AgentView
from agent_terminal.widgets.mascot import Mascot


class AgentTerminal(App):
    """A multi-agent terminal application."""

    CSS_PATH = "app.css"
    BINDINGS = [
        ("ctrl+t", "add_agent", "Add Agent"),
        ("ctrl+w", "remove_agent", "Remove Agent"),
        ("q", "quit", "Quit"),
    ]

    agent_classes = {"OpenAIAgent": OpenAIAgent, "OllamaAgent": OllamaAgent}

    def __init__(self) -> None:
        """Initialize the app."""
        super().__init__()
        self.agents: dict[str, Agent] = {}
        self.agent_count = 0

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with Vertical():
            with Horizontal():
                yield Mascot()
                yield TabbedContent(id="agents")
            yield Input(placeholder="Enter your prompt here...", id="prompt_input", disabled=True)
        yield Footer()

    def on_mount(self) -> None:
        """Called when the app is first mounted."""
        self.action_add_agent()

    async def on_input_submitted(self, message: Input.Submitted) -> None:
        """Handle user prompt submission."""
        prompt = message.value
        if not prompt:
            return

        tabs = self.query_one(TabbedContent)
        active_pane_id = tabs.active
        input_widget = self.query_one("#prompt_input", Input)

        if active_pane_id and not input_widget.disabled:
            agent = self.agents.get(active_pane_id)
            active_pane = tabs.get_pane(active_pane_id)
            agent_view = active_pane.query_one(AgentView)

            if not agent:
                agent_view.add_message("System", "[bold red]No agent is active for this tab.[/bold red]")
                return

            agent_view.add_message("User", prompt)
            input_widget.clear()
            input_widget.disabled = True
            agent_view.add_message("System", "[italic]Agent is thinking...[/italic]", sender_style="dim")

            response = await agent.get_response(prompt)
            agent_view.add_message(agent.__class__.__name__, response, sender_style="bold blue")

            input_widget.disabled = False
            input_widget.focus()

    def _add_agent_tab(self, agent_class_name: str, model_name: str) -> None:
        """Creates a new agent and its corresponding tab."""
        self.agent_count += 1
        pane_id = f"agent_{self.agent_count}"
        tabs = self.query_one(TabbedContent)

        try:
            agent_class = self.agent_classes[agent_class_name]
            agent = agent_class(model=model_name)
            self.agents[pane_id] = agent

            agent_view = AgentView()
            pane_title = f"{agent_class_name}: {model_name}"
            agent_view.add_message("System", f"Agent '{pane_title}' started.", sender_style="bold green")

            new_pane = TabPane(pane_title, agent_view, id=pane_id)
            tabs.add_pane(new_pane)
            tabs.active = pane_id
            self.query_one("#prompt_input", Input).disabled = False

        except ValueError as e:
            # Handle errors like missing API keys gracefully.
            agent_view = AgentView()
            pane_title = f"Error: {agent_class_name}"
            agent_view.add_message("System", f"[bold red]Failed to create agent: {e}[/bold red]")

            new_pane = TabPane(pane_title, agent_view, id=pane_id)
            tabs.add_pane(new_pane)
            tabs.active = pane_id
        except Exception as e:
            # Catch any other unexpected errors during agent initialization.
            agent_view = AgentView()
            pane_title = "Initialization Error"
            agent_view.add_message("System", f"[bold red]An unexpected error occurred: {e}[/bold red]")

            new_pane = TabPane(pane_title, agent_view, id=pane_id)
            tabs.add_pane(new_pane)
            tabs.active = pane_id

    def action_add_agent(self) -> None:
        """Show the agent selection screen and add a new agent tab."""
        def on_select_closed(result: tuple[str, str] | None) -> None:
            if result:
                agent_class_name, model_name = result
                self._add_agent_tab(agent_class_name, model_name)
            elif not self.agents:
                # If the user cancels the first dialog, quit the app.
                self.exit()

        self.push_screen(AgentSelectionScreen(), on_select_closed)

    def action_remove_agent(self) -> None:
        """Remove the active agent tab."""
        tabs = self.query_one(TabbedContent)
        active_pane_id = tabs.active

        if not active_pane_id:
            return

        if active_pane_id in self.agents:
            del self.agents[active_pane_id]

        tabs.remove_pane(active_pane_id)

        if not self.agents:
            self.query_one("#prompt_input", Input).disabled = True


if __name__ == "__main__":
    app = AgentTerminal()
    app.run()