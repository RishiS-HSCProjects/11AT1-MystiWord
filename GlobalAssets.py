"""
This file is full of static functions in avoidance of writing repeat code.
"""

import os

def clear_console() -> None:
    """ Clears the console. """
    print("\n" * 20) # Spams enter for an animation
    os.system("cls" if os.name == "nt" else "clear") # Clear system logs