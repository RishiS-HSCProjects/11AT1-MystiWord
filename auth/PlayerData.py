from colorama import Fore, Style

from lib.libData.DataManager import *
from lib.libData.DataManager import DataFields
import GlobalAssets as assets

class PlayerDataFields (DataFields):
    USERNAME = 'username'
    PASSWORD = 'password'
    XP = 'xp'
    COINS = 'coins'
    WINS = 'wins'
    LOSSES = 'losses'
    EASY_PB = 'easy_pb'
    MEDIUM_PB = 'medium_pb'
    HARD_PB = 'hard_pb'
    pass

class PlayerDataErrors (DataManagerErrors):
    class UnknownPlayer(Exception):
        """
            This exception is raised when the game tries accessing an unknown player.
        """
        
        def __init__(self, identifier: str = None):
            super().__init__("Tried manipulating an unknown player" + (f": {str(identifier)}" if identifier else ""))

class PlayerDataManager (DataManager):
    def __init__(self):
        super().__init__(os.path.join(os.path.dirname(__file__), "players"), self.DatabaseType.DICT) # Define database properties

    def getDefaultValues(self) -> dict:
        return {
            PlayerDataFields.XP: 0, # Sets XP to 0 on new account creation
            PlayerDataFields.COINS: 0, # Sets coins to 0 on new account creation
            PlayerDataFields.WINS: 0, # Sets wins to 0 on new account creation
            PlayerDataFields.LOSSES: 0, # Sets losses to 0 on new account creation 
            PlayerDataFields.EASY_PB: None, # Sets personal best to None on new account creation
            PlayerDataFields.MEDIUM_PB: None, # Sets personal best to None on new account creation
            PlayerDataFields.HARD_PB: None # Sets personal best to None on new account creation
        }
    
    def addXP(self, player: str, xp: int) -> None:
        """ Adds XP for a player. Negative XP values subtract them. """
        self.setData( # Replace the XP field with the final XP.
            player, # Sets identifier to player
            PlayerDataFields.XP, # Edits player data
            int(self.getData(player, PlayerDataFields.XP) + xp) # Add current player xp and inherited XP
        )

    def addWin(self, player: str) -> None:
        """ Adds win for a player. """
        self.setData( # Replace the wins field with the new number
            player, # Sets identifier to player
            PlayerDataFields.WINS, # Edits wins data
            int(self.getData(player, PlayerDataFields.WINS) + 1) # Add one to wins
        )

    def addLoss(self, player: str) -> None:
        """ Adds loss for a player. """
        self.setData( # Replace the losses field with the new number
            player, # Sets identifier to player
            PlayerDataFields.LOSSES, # Edits losses data
            int(self.getData(player, PlayerDataFields.LOSSES) + 1) # Add one to wins
        )

    def getGamesPlayed(self, player: str) -> int:
        """ Returns the sum of wins and losses """
        return  int(self.getData(player, PlayerDataFields.WINS)) + int(self.getData(player, PlayerDataFields.LOSSES))
    
    def getPB(self, player: str, difficulty: str) -> int:
        """ Returns the personal best for a given difficulty 
        
            Returns null if no personal best is set.
        """
        
        difficulty_field = f"{difficulty.lower()}_pb" # Define difficulty field by difficulty name
        if difficulty_field not in PlayerDataFields.__dict__.values():
            raise ValueError(f"Invalid difficulty level: {difficulty}") # Raise error if name is incorrect
        return self.getData(player, difficulty_field) # Return the personal best

    def setPB(self, player: str, difficulty: str, lives: int) -> None:
        """ Sets the personal best for a given difficulty """
        difficulty_field = f"{difficulty.lower()}_pb" # Define difficulty field by difficulty name
        if difficulty_field not in PlayerDataFields.__dict__.values():
            raise ValueError(f"Invalid difficulty level: {difficulty}") # Raise error if name is incorrect
        self.setData(player, difficulty_field, lives) # Set the personal best

    def getWLR(self, player: str) -> float:
        """ Returns the win-loss ratio """

        losses = int(self.getData(player, PlayerDataFields.LOSSES))

        if losses <= 0:
            losses = 1

        return  round(self.getData(player, PlayerDataFields.WINS) / losses, 2) # Returns to two decimal places
    
    def getData(self, identifier: str, key: DataFields = None):
        try:
            return super().getData(identifier, key)
        except Exception as e:
            print(Fore.RED + f"An error occured while trying to fetch data of {identifier}: {e}. Signing out..." + Style.RESET_ALL) # Send error message
            assets.pause() # Pause interface
            assets.logged_in_player = None # Logs out player
            try:
                self.deleteDatafile(identifier) # Attempt to delete corrupted file
            except DataManagerErrors.PathNotExists: # If path does not exist
                pass # Igore

            import Main
            Main.sendHomePage() # Open login form.

    def renameDatafile(self, old_identifier: str, new_identifier: str) -> None:
        # Construct the full path to the old and new filenames
        old_filename = os.path.join(self.datapath, f"{old_identifier}.json")
        new_filename = os.path.join(self.datapath, f"{new_identifier}.json")

        if os.path.exists(old_filename):
            os.rename(old_filename, new_filename)
        else:
            raise DataManagerErrors.PathNotExists(f"Error: The file with identifier {old_identifier} does not exist.")