import unittest
from unittest.mock import patch
import sys
import os

# Add the parent directory to the Python path to allow for importing the main module.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sopranos_cli import main

class TestMain(unittest.TestCase):

    @patch('builtins.input', side_effect=['quit'])
    def test_game_runs_and_quits(self, mock_input):
        """Test that the game runs and exits cleanly."""
        try:
            main.main()
        except SystemExit:
            # The game should exit cleanly.
            pass
        except Exception as e:
            self.fail(f"Game exited with an unexpected exception: {e}")

if __name__ == '__main__':
    unittest.main()