import unittest
from unittest.mock import patch, call
import sys
import os
import io

# Add the parent directory to the Python path to allow for importing the main module.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sopranos_cli import main

class TestMain(unittest.TestCase):

    @patch('builtins.input', side_effect=['quit'])
    def test_game_runs_and_quits(self, mock_input):
        """Test that the game runs and exits cleanly with 'quit'."""
        # Redirect stdout to capture print statements
        captured_output = io.StringIO()
        sys.stdout = captured_output

        main.main()

        # Restore stdout
        sys.stdout = sys.__stdout__

        # Check that the exit message is printed
        self.assertIn("Fuggedaboutit! See you next time.", captured_output.getvalue())

    @patch('builtins.input', side_effect=['1'])
    @patch('sopranos_cli.main.get_newspaper')
    def test_get_newspaper_path(self, mock_get_newspaper, mock_input):
        """Test the 'get newspaper' game path."""
        main.main()
        mock_get_newspaper.assert_called_once()

    @patch('builtins.input', side_effect=['2'])
    @patch('sopranos_cli.main.go_to_satrialis')
    def test_go_to_satrialis_path(self, mock_go_to_satrialis, mock_input):
        """Test the 'go to Satriale's' game path."""
        main.main()
        mock_go_to_satrialis.assert_called_once()

    @patch('builtins.input', side_effect=['3', 'quit'])
    @patch('builtins.print')
    def test_invalid_input(self, mock_print, mock_input):
        """Test that the game handles invalid input and allows the user to quit."""
        main.main()
        # Check that the error message for invalid input is printed.
        mock_print.assert_any_call("What, you got gabagool in your ears? Pick 1 or 2.")
        # Check that the exit message is also printed.
        mock_print.assert_any_call("Fuggedaboutit! See you next time.")

if __name__ == '__main__':
    unittest.main()