"""Tests for the AgentTerminal application."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from textual.pilot import Pilot
from textual.widgets import Button, Input, Select, TabbedContent

from agent_terminal.app import AgentTerminal
from agent_terminal.screens import AgentSelectionScreen
from agent_terminal.widgets.agent_view import AgentView

# Mark all tests in this file as asyncio
pytestmark = pytest.mark.asyncio

# --- Mocks for the entire test suite ---

MOCK_RESPONSE = "This is a mocked AI response."

# Mock the agent classes to avoid real API calls and dependencies
mock_openai_agent_instance = MagicMock()
mock_openai_agent_instance.get_response = AsyncMock(return_value=MOCK_RESPONSE)

mock_ollama_agent_instance = MagicMock()
mock_ollama_agent_instance.get_response = AsyncMock(return_value=MOCK_RESPONSE)

MockOpenAIAgent = MagicMock(return_value=mock_openai_agent_instance)
MockOllamaAgent = MagicMock(return_value=mock_ollama_agent_instance)

# Mock the VoiceCloningAgent to prevent model downloads during tests
mock_vc_agent_instance = MagicMock()
mock_vc_agent_instance.get_response = AsyncMock(return_value=MOCK_RESPONSE)
MockVoiceCloningAgent = MagicMock(return_value=mock_vc_agent_instance)


@patch.dict(
    "agent_terminal.app.AgentTerminal.agent_classes",
    {
        "OpenAIAgent": MockOpenAIAgent,
        "OllamaAgent": MockOllamaAgent,
        "VoiceCloningAgent": MockVoiceCloningAgent,
    },
)
class TestAgentTerminal:
    """A test suite for the main application flow."""

    async def test_initial_state_and_add_first_agent(self):
        """Test that the app starts, prompts for an agent, and adds it."""
        app = AgentTerminal()
        async with app.run_test() as pilot:
            # App starts and immediately pushes the selection screen
            assert isinstance(pilot.app.screen, AgentSelectionScreen)
            assert len(pilot.app.query("TabPane")) == 0

            # Simulate selecting an agent
            await pilot.click(Select)
            await pilot.click("Select > .select--option")  # Clicks the first option (GPT-4o)
            await pilot.click(Button, "#create_button")
            await pilot.pause()

            # Verify the screen was dismissed and a tab was added
            assert isinstance(pilot.app.screen, AgentTerminal)
            assert len(pilot.app.query("TabPane")) == 1
            assert pilot.app.query_one(TabbedContent).active == "agent_1"
            assert "OpenAIAgent: gpt-4o" in pilot.app.query_one("TabPane").renderable

            # Verify input is now enabled
            assert pilot.app.query_one("#prompt_input", Input).disabled is False

    async def test_add_and_remove_agents(self):
        """Test adding a second agent and then removing tabs."""
        app = AgentTerminal()
        async with app.run_test() as pilot:
            # Add the first agent
            await pilot.press("ctrl+t")  # First one is added on mount
            await pilot.click(Select)
            await pilot.click("Select > .select--option")
            await pilot.click(Button, "#create_button")
            await pilot.pause()
            assert len(pilot.app.query("TabPane")) == 1

            # Add a second agent
            await pilot.press("ctrl+t")
            await pilot.click(Select)
            # Select the third option (Ollama)
            await pilot.press("down", "down")
            await pilot.press("enter")
            await pilot.click(Button, "#create_button")
            await pilot.pause()

            assert len(pilot.app.query("TabPane")) == 2
            assert pilot.app.query_one(TabbedContent).active == "agent_2"
            assert "OllamaAgent: llama3" in pilot.app.query("TabPane")[1].renderable
            assert "agent_2" in app.agents

            # Remove the second agent
            await pilot.press("ctrl+w")
            await pilot.pause()
            assert len(pilot.app.query("TabPane")) == 1
            assert "agent_2" not in app.agents
            assert pilot.app.query_one(TabbedContent).active == "agent_1"

            # Remove the last agent
            await pilot.press("ctrl+w")
            await pilot.pause()
            assert len(pilot.app.query("TabPane")) == 0
            assert "agent_1" not in app.agents
            assert pilot.app.query_one("#prompt_input", Input).disabled is True

    async def test_prompt_submission_and_mocked_response(self):
        """Test the full flow of submitting a prompt to a mocked agent."""
        app = AgentTerminal()
        async with app.run_test() as pilot:
            # Add an agent
            await pilot.press("ctrl+t")
            await pilot.click(Select)
            await pilot.click("Select > .select--option")
            await pilot.click(Button, "#create_button")
            await pilot.pause()

            # Submit a prompt
            prompt_input = pilot.app.query_one("#prompt_input", Input)
            test_prompt = "Hello, mocked AI!"
            prompt_input.value = test_prompt
            await pilot.press("enter")
            await pilot.pause()

            # Verify the flow
            agent_view = pilot.app.query_one(AgentView)
            log_content = agent_view.to_plain_text()

            assert "User: Hello, mocked AI!" in log_content
            assert "System: Agent is thinking..." in log_content
            assert f"OpenAIAgent: {MOCK_RESPONSE}" in log_content

            # Verify the mock was called
            mock_openai_agent_instance.get_response.assert_awaited_with(test_prompt)

    async def test_agent_creation_error_handling(self):
        """Test that UI shows an error if agent instantiation fails."""
        # Mock the agent's __init__ to raise an error
        MockOpenAIAgent.side_effect = ValueError("Missing API Key")

        app = AgentTerminal()
        async with app.run_test() as pilot:
            # Try to add the failing agent
            await pilot.press("ctrl+t")
            await pilot.click(Select)
            await pilot.click("Select > .select--option")
            await pilot.click(Button, "#create_button")
            await pilot.pause()

            # Verify an error tab was created
            assert len(pilot.app.query("TabPane")) == 1
            agent_view = pilot.app.query_one(AgentView)
            log_content = agent_view.to_plain_text()
            assert "Failed to create agent: Missing API Key" in log_content

            # Input should remain disabled
            assert pilot.app.query_one("#prompt_input", Input).disabled is True

        # Reset the mock for other tests
        MockOpenAIAgent.side_effect = None
        MockOpenAIAgent.return_value = mock_openai_agent_instance