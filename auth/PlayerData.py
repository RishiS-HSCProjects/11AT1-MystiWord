from colorama import Fore, Style

from lib.libData.DataManager import *
from lib.libData.DataManager import DataFields
import GlobalAssets as assets

class PlayerDataFields (DataFields):
    USERNAME = 'username'
    PASSWORD = 'password'
    XP = 'xp'
    WINS = 'wins'
    LOSSES = 'losses'
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
            PlayerDataFields.WINS: 0, # Sets wins to 0 on new account creation
            PlayerDataFields.LOSSES: 0 # Sets losses to 0 on new account creation 
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