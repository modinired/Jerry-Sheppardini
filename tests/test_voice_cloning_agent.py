"""Unit tests for the VoiceCloningAgent."""

import asyncio
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from agent_terminal.agents.voice_cloning_agent import VoiceCloningAgent


@pytest.fixture
def mock_dependencies():
    """Mocks all external dependencies for the VoiceCloningAgent."""
    with patch(
        "agent_terminal.agents.voice_cloning_agent.OpenAIAgent", autospec=True
    ) as mock_openai_agent, patch(
        "chatterbox.tts.ChatterboxTTS", autospec=True
    ) as mock_chatterbox, patch(
        "agent_terminal.agents.voice_cloning_agent.sf", autospec=True
    ) as mock_soundfile, patch(
        "agent_terminal.agents.voice_cloning_agent.sd", autospec=True
    ) as mock_sounddevice, patch(
        "agent_terminal.agents.voice_cloning_agent.Path.is_file", return_value=True
    ), patch(
        "agent_terminal.agents.voice_cloning_agent.Path.unlink"
    ) as mock_unlink:
        # Configure the ChatterboxTTS mock
        mock_tts_instance = MagicMock()
        mock_tts_instance.generate.return_value = MagicMock()  # Mock waveform
        mock_chatterbox.from_pretrained.return_value = mock_tts_instance

        # Configure the OpenAIAgent mock
        mock_openai_instance = MagicMock()
        mock_openai_instance.get_response = AsyncMock(
            return_value="This is a test response."
        )
        mock_openai_agent.return_value = mock_openai_instance

        # Configure the soundfile mock to return dummy data
        mock_soundfile.read.return_value = (MagicMock(), 44100)

        yield {
            "openai_agent": mock_openai_agent,
            "chatterbox": mock_chatterbox,
            "soundfile": mock_soundfile,
            "sounddevice": mock_sounddevice,
            "unlink": mock_unlink,
            "tts_instance": mock_tts_instance,
            "openai_instance": mock_openai_instance,
        }


def test_initialization_success(mock_dependencies):
    """Test that the VoiceCloningAgent initializes successfully without loading the model."""
    agent = VoiceCloningAgent(model="gpt-4o", audio_path="/fake/path/voice.wav")
    assert agent.model == "gpt-4o"
    assert agent.audio_path == "/fake/path/voice.wav"
    assert agent.tts_model is None
    mock_dependencies["chatterbox"].from_pretrained.assert_not_called()
    mock_dependencies["openai_agent"].assert_called_once_with(model="gpt-4o")


def test_initialization_file_not_found():
    """Test that initialization raises FileNotFoundError if the audio path is invalid."""
    with patch("agent_terminal.agents.voice_cloning_agent.Path.is_file", return_value=False):
        with pytest.raises(FileNotFoundError, match="Audio file not found at: /invalid/path.wav"):
            VoiceCloningAgent(model="gpt-4o", audio_path="/invalid/path.wav")


@pytest.mark.asyncio
async def test_get_response(mock_dependencies):
    """Test the complete get_response flow, including lazy model loading."""
    agent = VoiceCloningAgent(model="gpt-4o", audio_path="/fake/path/voice.wav")
    assert agent.tts_model is None

    prompt = "Tell me a story."
    response = await agent.get_response(prompt)

    # Verify the agent returns the correct status message
    assert response == f"Playing audio response for: '{prompt}'"

    # Verify the TTS model was lazy-loaded
    mock_dependencies["chatterbox"].from_pretrained.assert_called_once()
    assert agent.tts_model is not None

    # Verify the text agent was called correctly
    mock_dependencies["openai_instance"].get_response.assert_awaited_once_with(prompt)

    # Verify the TTS model was used correctly
    mock_dependencies["tts_instance"].generate.assert_called_once_with(
        "This is a test response.",
        audio_prompt_path="/fake/path/voice.wav",
    )

    # Verify the audio was saved
    mock_dependencies["soundfile"].write.assert_called_once()

    # Allow the async _play_audio task to run
    await asyncio.sleep(0.01)

    # Verify audio playback and cleanup
    mock_dependencies["sounddevice"].play.assert_called_once()
    mock_dependencies["sounddevice"].wait.assert_called_once()
    mock_dependencies["unlink"].assert_called_once()