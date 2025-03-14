"""
This file is full of static functions in avoidance of writing repeat code.
"""

import os

def clear_console() -> None:
    """ Clears the console. """
    print("\n" * 20) # Spams enter for an animation
    os.system("cls" if os.name == "nt" else "clear") # Clear system logs

def set_title(title: str = None) -> None:
    """ Sets the title of the app. Add  a title parameter to give extra info. """

    os.system(f"title MystiWord{f': {title}' if title else ''}") # Runs the title command in the app to set the title