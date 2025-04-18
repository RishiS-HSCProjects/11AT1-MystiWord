"""
This file is full of static functions in avoidance of writing repeat code.
"""

import os
from colorama import Fore, Style
from auth import PlayerData, LocalData

def clear_console() -> None:
    """ Clears the console. """
    os.system("cls" if os.name == "nt" else "clear") # Clear system logs

def pause(colour: str = None) -> None:
    """ Pauses console. """
    print(colour if colour else "") # Set text colour styles
    os.system("pause") # Pause console
    print(Style.RESET_ALL) # Removes styles

def set_title(title: str = None) -> None:
    """ Sets the title of the app. Add a title parameter to give extra info. """
    os.system(f"title MystiWord{f': {title}' if title else ''}") # Runs the title command in the app to set the title

def getPlayerManager() -> PlayerData.PlayerDataManager:
    """ Returns new instance of PlayerDataManager. """
    return PlayerData.PlayerDataManager()

def getLocalData() -> LocalData.LocalDataManager:
    """ Returns new instance of LocalDataManager. """
    return LocalData.LocalDataManager()

def doesUserExist(username: str) -> bool:
    """ Returns if a user exists. """
    return getPlayerManager().datafileExists(username)

# Player Data
logged_in_player = None # Initialises the temporary storage of the logged in player. 

@property
def logged_in_player(): # Get logged_in_player
    return logged_in_player

@logged_in_player.setter
def logged_in_player(value: str) -> None: # Set logged_in_player
    if not doesUserExist(value): # If statement is true if the user does not exist. 
        raise PlayerData.PlayerDataErrors.UnknownPlayer(value) # Throw error if player does not exist.
    logged_in_player = value # Sets logged in player to value.

def get_guest_identifier() -> str:
    """ Return constant guest identifier. """
    return "GUEST" # All caps labeled guest so players can replicate it in game. (All player names must be in lowercase)
    

# Titles
def getTitle() -> str:
    """ Returns formatted ASCII title as a string. """
    return Style.RESET_ALL + Fore.MAGENTA + """
███╗   ███╗██╗   ██╗███████╗████████╗██╗██╗    ██╗ ██████╗ ██████╗ ██████╗ 
████╗ ████║╚██╗ ██╔╝██╔════╝╚══██╔══╝██║██║    ██║██╔═══██╗██╔══██╗██╔══██╗
██╔████╔██║ ╚████╔╝ ███████╗   ██║   ██║██║ █╗ ██║██║   ██║██████╔╝██║  ██║
██║╚██╔╝██║  ╚██╔╝  ╚════██║   ██║   ██║██║███╗██║██║   ██║██╔══██╗██║  ██║
██║ ╚═╝ ██║   ██║   ███████║   ██║   ██║╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝
╚═╝     ╚═╝   ╚═╝   ╚══════╝   ╚═╝   ╚═╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝ 
""" + Style.RESET_ALL