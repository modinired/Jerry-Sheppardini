import os
from textual.widgets import Static
from textual.app import log

# Path to the mascot image, resolved relative to this file's location.
MASCOT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "assets", "mascot.png")
)

# A cache to store the generated ASCII art so we only do the conversion once.
MASCOT_ASCII = None


class Mascot(Static):
    """A widget to display the project's mascot as ASCII art."""

    def on_mount(self) -> None:
        """Called when the widget is mounted.

        This method will generate the ASCII art from the image file.
        It's done here to avoid slowing down the application's startup time.
        """
        global MASCOT_ASCII
        if MASCOT_ASCII is None:
            if not os.path.exists(MASCOT_PATH):
                log.error(f"Mascot image not found at {MASCOT_PATH}")
                self.update("[Mascot image not found]")
                return

            try:
                # We lazy-import ascii_magic here to keep it as an optional dependency
                # and to avoid a long import time at the module level.
                from ascii_magic import AsciiArt

                art = AsciiArt.from_image(MASCOT_PATH)
                # We'll render the mascot at a fixed width to fit the UI.
                MASCOT_ASCII = art.to_ascii(columns=30)
                log.info("Mascot ASCII art generated successfully.")

            except ImportError:
                log.error("The 'ascii_magic' library is not installed.")
                MASCOT_ASCII = "[Mascot requires 'ascii_magic']"
            except Exception as e:
                log.error(f"Failed to generate mascot ASCII art: {e}")
                MASCOT_ASCII = f"[Mascot Error: {e}]"

        self.update(MASCOT_ASCII)