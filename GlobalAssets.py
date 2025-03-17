"""
This file is full of static functions in avoidance of writing repeat code.
"""

import os
import sys
from colorama import Fore, Style

def clear_console() -> None:
    """ Clears the console. """
    # print("\n" * 20) # Spams enter for an animation
    os.system("cls" if os.name == "nt" else "clear") # Clear system logs

def pause(colour: str = None) -> None:
    """ Pauses console """
    print(colour if colour else "") # Set text colour styles
    os.system("pause") # Pause console
    print(Style.RESET_ALL) # Removes styles

def set_title(title: str = None) -> None:
    """ Sets the title of the app. Add  a title parameter to give extra info. """

    os.system(f"title MystiWord{f': {title}' if title else ''}") # Runs the title command in the app to set the title

from auth import PlayerData
def getPlayerManager() -> PlayerData.PlayerDataManager:
    return PlayerData.PlayerDataManager()   

# Player Data
logged_in_player = None # Stores logged in player (starts at None)

@property
def logged_in_player(): # Get logged_in_player
    return logged_in_player

def get_guest_identifier() -> str:
    return "GUEST"

@logged_in_player.setter
def logged_in_player(value: str) -> None:
    from auth import Auth
    if not Auth.doesUserExist(value): # If statement is true if the user does not exist. 
        raise PlayerData.PlayerDataErrors.UnknownPlayer(value)
    logged_in_player = value # Sets logged in player to value.
    

# Titles
def getTitle() -> str:
    from colorama import Fore, Style # Import colour styling
    return Style.RESET_ALL + Fore.MAGENTA + """
███╗   ███╗██╗   ██╗███████╗████████╗██╗██╗    ██╗ ██████╗ ██████╗ ██████╗ 
████╗ ████║╚██╗ ██╔╝██╔════╝╚══██╔══╝██║██║    ██║██╔═══██╗██╔══██╗██╔══██╗
██╔████╔██║ ╚████╔╝ ███████╗   ██║   ██║██║ █╗ ██║██║   ██║██████╔╝██║  ██║
██║╚██╔╝██║  ╚██╔╝  ╚════██║   ██║   ██║██║███╗██║██║   ██║██╔══██╗██║  ██║
██║ ╚═╝ ██║   ██║   ███████║   ██║   ██║╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝
╚═╝     ╚═╝   ╚═╝   ╚══════╝   ╚═╝   ╚═╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝ 
""" + Style.RESET_ALL