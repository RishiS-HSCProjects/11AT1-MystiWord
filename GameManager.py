import sys
import random
from enum import Enum
from colorama import Fore, Back, Style, init
init() # initialies the colorma class
import time

from lib.libData.DataManager import *
from lib.libForms.Form import *
import GlobalAssets as assets
from auth.LocalData import LocalDataFields
from auth import PlayerData

class Game:
    """ Holds all data and functions attributed to a running game. """

    def __init__(self) -> None:
        """ Initialise game """
        difficulty_form = OptionForm("Play Guess the Word!", "Guess letters to spell out a word!\n\nYou get more XP the less incorrect guesses you make. XP can get you ranked high on the leaderboards!\n\nYou lose a life for every incorrect letter you guess. You have 10 lives, so choose wisely!.") # Create a choose difficulty form
        difficulty_form.settings.editSetting(FormSettings.Setting.OPTIONS_TEXT, "Choose Difficulty") # Sets options text to Choose Difficulty


        difficulty_form.addOption(WordManager.Difficulties.EASY.formatDifficulty(upperCase=True), lambda _: self.createWordManager(WordManager.Difficulties.EASY)) # Create option for difficulty
        difficulty_form.addOption(WordManager.Difficulties.MEDIUM.formatDifficulty(upperCase=True), lambda _: self.createWordManager(WordManager.Difficulties.MEDIUM)) # Create option for difficulty
        difficulty_form.addOption(WordManager.Difficulties.HARD.formatDifficulty(upperCase=True), lambda _: self.createWordManager(WordManager.Difficulties.HARD)) # Create option for difficulty
        difficulty_form.addOption(Back.RED + Fore.WHITE + "Random", lambda _: self.createWordManager()) # WordData will handle cases where the difficulty is not set.
        
        from Main import sendHomePage # Import home page
        difficulty_form.addOption(
            name=Fore.LIGHTBLACK_EX + "Back", # Create back option
            callback=lambda: sendHomePage(), # Send to homepage on click
            isDefault=True # If no option selected, go back
        )

        difficulty_form.settings.editSetting(FormSettings.Setting.HEADER, assets.getTitle()) # Creates a pretty header using the ANSI SHADOW ASCII art
        difficulty_form.settings.editSetting(FormSettings.Setting.CLEAR_FORM_AFTER_FORM, True) # Clears the console after an option has been selected.
        difficulty_form.settings.editSetting(FormSettings.Setting.CLEAN_FAILED_RESPONSES, 3) # Clears form and failed responses after three incorrect attempts

        difficulty_form.send() # Sends the form to the user

        self.foundLetterPositions = [] # Initialises the array with all of the correct letters. This will be the index to wher the correct letter is.
        self.correctLetters = [] # Initialises the array with all of the correct letters. This is an array of strings.
        self.incorrectLetters = [] # Initialises the array with all of the incorrect letters. This is an array of strings.

        self.lives = 10 # Starts life count at ten.

        self.xp = self.lives * 10 # starts XP at ten time the amount of lives (100). 

        self.theme = None # Initialise self.theme
        equipped = assets.getPlayerManager().getData(assets.logged_in_player, PlayerData.PlayerDataFields.EQUIPPED_THEME) # get equipted theme
        if equipped: # If theme equipted
            while not self.theme: # Repeat until theme is set
                for theme in Themes.Themes: # Find theme
                    if equipped == theme.getName():
                        self.theme = theme # Set theme

    def createWordManager(self, difficulty: 'WordManager.Difficulties' = None):
        """ Sets the wordmanager based on difficulty. """
        self.wordManager = WordManager(difficulty)
        pass

    def playGame(self):
        """ Runs gameplay processes """

        assets.set_title(f"Playing {self.wordManager.difficulty.name} MODE")

        self.sendGameBoard() # Displays gameboard.

        def letterValidation(letter: str) -> bool:
            """ Function to check if a letter is a valid guess (not guessed before, a valid letter). """
            if not isinstance(letter, str):
                return False # Failsafe + makes the while loop start.

            isLetter = len(letter) == 1 and letter.lower().isalpha() # Returns true if the input is a valid letter
            notGuessed = letter.upper() not in self.incorrectLetters and letter.upper() not in self.correctLetters # Returns true if the letter has not previously been guessed.

            return isLetter and notGuessed # Returns if letter is a valid letter and has not previously been guessed.

        letter = None # Sets letter to none to enter the while loop
        iteration = 0 # Checks if the while loop has ran more than once.
        while not letterValidation(letter): # While the inputted letter is invalid.
            if iteration > 0: # Not the first iteration

                if iteration > 3:
                    iteration = 1 # Reset the iteration counter
                    self.sendGameBoard() # Resend the gameboard to clear failed attempts.

                print(Fore.RED + "Error: Invalid letter." + Fore.RESET) # Notifies the player something went wrong.

            iteration += 1 # Increment the iteration counter

            letter = input("Guess a letter: ") # Input for the letter

        word = self.wordManager.word # Stores the word in this easier variable 

        foundLetters = [i for i in range(len(word)) if word.startswith(letter, i)] # Finds positions where the letters in self.word is equal to the letter.
        
        def finishGame(win) -> None:
            """ Actions ran on game end. """
            self.sendGameBoard(win) # Show winning board.
            time.sleep(1) # Sleep to not let the user exit too fast. 

            assets.pause() # Holder for user to observe the board.

            runGame() # Rerun game

        if len(foundLetters) > 0: # If the player found a correct letter.
            self.foundLetterPositions.extend(foundLetters) # Extends the found positions to the total found positions variable.
            self.correctLetters.append(letter.upper()) # Add letter to correct letters
        else:
            self.incorrectLetters.append(letter.upper()) # Add letter to incorrect letters
            if self.lives >= 1:
                self.lives -= 1 # Reduce one life.
                self.xp -= 10 # Reduce XP by 10
            if self.lives == 0:
                finishGame(False) # Stop game (loss).


        if len(self.foundLetterPositions) == len(word): # Win validation
            finishGame(True) # Stop game (win)
        else:
            self.playGame() # Rerun this script to play the next tern.

    def sendGameBoard(self, win: bool = None):
        """ Sends the gameboard. """

        assets.clear_console() # Clears the console

        word = self.wordManager.word # Saves word in a shorter variable

        print(assets.getTitle()) # Prints the title banner

        pb = assets.getPlayerManager().getPB(assets.logged_in_player, self.wordManager.difficulty.value) or 0 # Gets the personal best. If it does not exist, set it to 0.
        hearts = (Fore.RED + '♥️' * min(self.lives, pb if pb != 10 else pb - 1) + Fore.YELLOW + '♥️' * max(1 if self.lives == 10 else 0, self.lives - pb) + Style.RESET_ALL) if assets.getLocalData().getDataField(LocalDataFields.Settings.SHOW_HEARTS) else None # Displays the hearts (gold for personal best, red for current lives, last heart always yellow if lives are 10)
        print("Guess the word: " + f"{self.wordManager.difficulty.formatDifficulty(upperCase=True)} MODE" + (f"               {hearts}" if hearts else "")) # Displays the mode

        if self.theme: # Check if theme is valid
            print(self.theme.getStage((10 - (self.lives if self.lives > 0 else 1)))) # Print the theme

        gameLines = ["_ "] * len(word) # Creates a gameLines list comprised of one underscore for each letter of the word

        for themes in self.foundLetterPositions:
            gameLines[themes] = word[themes].upper() + " "

        print() # Whitespace

        print("".join(gameLines)) # Converts array to a string.

        print() # Whitespace

        if len(self.incorrectLetters) > 0: # Only show incorrect letters if there are any.
            print(Fore.RED + "Incorrect letters: " + ", ".join(self.incorrectLetters) + Fore.RESET) # Format incorrect letters.

        print() # Whitespace

        if win != None: # Handle victory/loss logic
            if win: # Handle victory
                if self.lives == 10:
                    print(Fore.LIGHTGREEN_EX + "Perfect game!" + Fore.RESET) # Perfect game message
                elif self.lives == 1:
                    print(Fore.LIGHTBLACK_EX + "Phew! That was close!" + Fore.RESET) # Close call message
                print(Fore.GREEN + Style.BRIGHT + "YOU WIN!" + Fore.RESET) # Victory text
                print() # Whitespace

                winXP = self.xp # Assign the base xp to winXP.
                coins = self.wordManager.difficulty.getCoins() # Get the amount of coins awarded for a win

                # Add multipliers here
                winXP *= 1 + self.lives/20 # Add a 5% bonus for each life remaining
                winXP *= self.wordManager.difficulty.getXPMultiplier() # Multiply the XP by the difficulty multiplier

                newPB = self.lives > (pb or 0) # Set if player has a new personal best
                if newPB or self.lives == 10: # If the player has a new personal best or they have a perfect game
                    if newPB: # If the player has a new personal best
                        assets.getPlayerManager().setPB(assets.logged_in_player, self.wordManager.difficulty.value, self.lives) # Set new personal best
                        print(Fore.LIGHTGREEN_EX + f"New personal best: {self.lives} lives" + Style.RESET_ALL) # Display the new personal best message\

                    winXP *= 1.2 # Add a 20% bonus to XP for setting a new personal best (or having a personal best of 10)

                winXP = round(winXP)
                print(Fore.LIGHTGREEN_EX + f"+ {winXP} XP" + Style.RESET_ALL) # Display the addition of XP
                print(Fore.YELLOW + f"+ {coins} coins" + Style.RESET_ALL) # Display the addition of coins
                assets.getPlayerManager().addXP(assets.logged_in_player, winXP) # Add XP to account
                assets.getPlayerManager().addCoins(assets.logged_in_player, coins) # Add XP to account
                assets.getPlayerManager().addWin(assets.logged_in_player) # Register win
            else:
                print(Fore.RED + "YOU LOSE!" + Fore.RESET) # Loss text
                print(Fore.YELLOW + f"Word: {word.upper()}" + Fore.RESET) # Display the word
                assets.getPlayerManager().addLoss(assets.logged_in_player) # Register loss

                

            if assets.getLocalData().getDataField(LocalDataFields.Settings.AFTER_GAME_STATS): # Show player stats if enabled
                playerManager = assets.getPlayerManager() # Get player manager
                getData = lambda field: playerManager.getData(assets.logged_in_player, field) # Get player data
                time.sleep(1) # Pause for 1 second
                print(f"""
New Stats:
  {Fore.LIGHTGREEN_EX}XP: {getData(PlayerData.PlayerDataFields.XP)}{Style.RESET_ALL}
  Games Played: {playerManager.getGamesPlayed(assets.logged_in_player)}
  Wins: {str(getData(PlayerData.PlayerDataFields.WINS) - 1) + " + 1" if win else getData(PlayerData.PlayerDataFields.WINS)}
  Losses: {str(getData(PlayerData.PlayerDataFields.LOSSES) - 1) + " + 1" if not win else getData(PlayerData.PlayerDataFields.LOSSES)}
  WLR: {playerManager.getWLR(assets.logged_in_player)}
  Points per Win Average: {round(int(getData(PlayerData.PlayerDataFields.XP)) / int(getData(PlayerData.PlayerDataFields.WINS)), 2) if int(getData(PlayerData.PlayerDataFields.WINS)) > 0 else "N/A"}
  {self.wordManager.difficulty.value} PB: {playerManager.getPB(assets.logged_in_player, self.wordManager.difficulty.value) or "N/A"}
            """) # Print stats

class WordManager:
    """ Does everything word-related. All functions relating to the individual words of the game are located here. """
    
    def __init__(self, difficulty: 'WordManager.Difficulties' = None) -> None:
        """ Initialise word manager. """
        if not isinstance(difficulty, WordManager.Difficulties):
            # If difficulty was set to None (for randomisation) or an invalid type, randomise difficulty to avoid an error.
            difficulty = random.choice(list(WordManager.Difficulties))  # Randomly select a difficulty
        
        self.difficulty = difficulty # Sets difficulty

        class LoadingBarStatus (Enum):
            """ Statuses to tell the systems which messages to display for the loading screen. """
            DOWNLOADING_WORDS = 0
            FILTERING_WORDS = 1
            RANDOMISING_WORDS = 2
            CHOOSING_WORD = 3
            pass

        class CorpusType (Enum):
            """ Defines corpus names for easy access """
            WORDS = 'words' # Type storing a large repository of words in English
            COMMON = 'brown' # Type storing (smaller) repository of common words in English
            pass

        def sendLoadingBar(status: "LoadingBarStatus") -> None:
            """ Prints a progress bar to show progress of game creation """
            assets.clear_console()  # Clears the console

            print("Game starting soon...\n")  # Loading message

            # Calculate the percentage of the progress bar filled based on the current status
            total_steps = len(LoadingBarStatus) - 1 # Subtract 1 because we want a range from 0 to the last status
            percentage = status.value / total_steps if total_steps > 0 else 1 # Calculate the progress as a percentage (between 0 and 1)

            bar_length = 50 # Horizontal length of the progress bar

            filled_length = int(bar_length * percentage) # Calculate the number of filled blocks based on the percentage

            # Create the progress bar string
            bar = Style.BRIGHT + '[' + Fore.GREEN + '=' * filled_length + Fore.RED + ' ' * (bar_length - filled_length) + Style.RESET_ALL + ']'  # Progress bar

            print(f"\n{bar} {int(percentage * 100)}%\n") # Print the progress bar with percentage

            # Print the corresponding status message
            if status.value == LoadingBarStatus.DOWNLOADING_WORDS.value:
                print("\nDownloading words...")
                print(Fore.RED + "\nWARNING: " + Fore.RESET + "If this step takes too long, please restart the game and try again.")
            if status.value == LoadingBarStatus.FILTERING_WORDS.value:
                print("\nFiltering words...")
            if status.value == LoadingBarStatus.RANDOMISING_WORDS.value:
                print("\nRandomising words...")
            if status.value == LoadingBarStatus.CHOOSING_WORD.value:
                print("\nChoosing word...")
    
        sendLoadingBar(LoadingBarStatus.DOWNLOADING_WORDS) # Send loading screen

        import nltk # Import the Natural Language Toolkit

        corpusType = None
        if difficulty == WordManager.Difficulties.EASY: # Settings to configure if difficulty is easy
            min_len, max_len = 4, 5 # Define word length range based on difficulty
            corpusType = CorpusType.COMMON
        elif difficulty == WordManager.Difficulties.MEDIUM: # Settings to configure if difficulty is Medium
            min_len, max_len = 6, 7 # Define word length range based on difficulty
            corpusType = CorpusType.COMMON
        elif difficulty == WordManager.Difficulties.HARD: # Settings to configure if difficulty is Hard
            min_len, max_len = 8, 15 # Define word length range based on difficulty
            corpusType = CorpusType.WORDS
        else: 
            raise ValueError("Unknown difficulty") # Raise error if the diffculty does not exist.

        word_list = [] # Initialise word_list

        # Download word repo
        from nltk.corpus import words, brown
        # Download the necessary corpora if not already downloaded. Do not output logs here.
        nltk.download(corpusType.value, quiet=True)

        sendLoadingBar(LoadingBarStatus.FILTERING_WORDS) # Send loading screen

        # Select the correct corpus based on corpusType
        # Creates array with all applicable words by cycling through all words in a repository. 
        if corpusType == CorpusType.COMMON:
            word_list = [word.lower() for word in brown.words() if min_len <= len(word) <= max_len]
        elif corpusType == CorpusType.WORDS:
            word_list = [word.lower() for word in words.words() if min_len <= len(word) <= max_len]

        sendLoadingBar(LoadingBarStatus.RANDOMISING_WORDS) # Send loading screen
        random.shuffle(word_list) # Shuffle the word list
        while True: # Loop to keep finding a word till it is valid
            self.word = random.choice(word_list) # Choose a random word
            if self.word.isalpha(): # Ensure the word only has letters (Brown words had this issue where numbers would sometimes be outputted instead of words.)
                break

        sendLoadingBar(LoadingBarStatus.CHOOSING_WORD) # Send loading screen

    class Difficulties (Enum):
        """ Stores difficulty information and functions. """
        EASY = "Easy"
        MEDIUM = "Medium"
        HARD = "Hard"

        def getColour(self) -> str:
            """ Return the appropriate color for each difficulty. """
            if self == WordManager.Difficulties.EASY:
                return Fore.GREEN
            elif self == WordManager.Difficulties.MEDIUM:
                return Fore.YELLOW
            elif self == WordManager.Difficulties.HARD:
                return Fore.RED
            return Fore.RESET
        
        def formatDifficulty(self, resetColour: str = None, upperCase: bool = None) -> str:
            """
            Returns a formatted string of the difficulty name with color and case formatting.

            Parameters:
                resetColour (str): Optionally, color to reset to after formatting.
                upperCase (bool):
                    - None (default): No case changes (sentence case)
                    - False: Force lower case
                    - True: Force upper case 

            Returns:
                str: The formatted difficulty string with color and desired case formatting.
            """
            # Apply case formatting based on the passed formatCase argument
            name = self.value
            if upperCase:
                name = name.upper()
            elif upperCase != None: # While True != None, True case is handled above.
                name = name.lower()

            # Apply color formatting and return formatted name
            return self.getColour() + name + (resetColour if isinstance(resetColour, str) else Fore.RESET)
            
        def getXPMultiplier(self) -> float:
            """ Returns the XP multipler that will be applied. """
            if self == WordManager.Difficulties.EASY:
                return 0.8
            elif self == WordManager.Difficulties.MEDIUM:
                return 1.1
            elif self == WordManager.Difficulties.HARD:
                return 1.3
            raise ValueError("Unknown difficulty") # Raise error if the diffculty does not exist.
            
        def getCoins(self) -> int:
            """ Returns the constant amount of coins awarded for a win. """
            if self == WordManager.Difficulties.EASY: return 5
            elif self == WordManager.Difficulties.MEDIUM: return 7
            elif self == WordManager.Difficulties.HARD: return 10
            raise ValueError("Unknown difficulty") # Raise error if the diffculty does not exist.

class Themes:
    """ Deals with everything related to themes. """
    
    class Themes (Enum):
        BOXES = 'boxes'
        BRIDGE = 'bridge'
        PACMAN = 'pacman'
        HANGMAN = 'hangman'

        def getName(self) -> str:
            """ Returns the name of the theme. """
            theme_data = Themes.Manager().getTheme(self)  # Fetch the theme data

            return theme_data.get('name')  # Fetch the specific theme data

        def getStage(self, stage: int) -> str:
            """ Returns the name of the theme. """
            theme_data = Themes.Manager().getTheme(self)  # Fetch the theme data

            return theme_data.get('stages').get(f'{stage}')  # Fetch the specific theme data
        
        def getCost(self) -> int:
            """ Returns the cost of the theme. """
            theme_data = Themes.Manager().getTheme(self) # Fetch the theme data
            return theme_data.get('cost') # Get the amount of coins required to purchase the theme
        
        def handlePurchase(self) -> None:
            """
                Handles the selection of the theme in the shop. 
                
                Cases:
                    - Player can not afford it: Does nothing.
                    - Player can afford it: Purchases theme and enables theme for display.
                    - Player has item in inventory: Enables theme for display.
            """
            from auth.PlayerData import PlayerDataFields as field
            
            themes = assets.getPlayerManager().getData(assets.logged_in_player, field.THEMES) # Array of purchased themes
            coins = assets.getPlayerManager().getData(assets.logged_in_player, field.COINS) # Number of coins in the player's bank.
            if self.getName() not in themes: # If item is not already purchased...
                if (int(coins) >= self.getCost()): # Checks if player has sufficient funds
                    assets.getPlayerManager().setData(assets.logged_in_player, field.COINS, int(coins) - self.getCost()) # removes cost from bank
                    themes.append(self.getName()) # Append themes array with the newly purchased theme.
                    assets.getPlayerManager().setData(assets.logged_in_player, field.THEMES, themes) # Stores new themes array into player stats.
                else: return # If insufficient funds, exit (do nothing)
            
            assets.getPlayerManager().setData(assets.logged_in_player, field.EQUIPPED_THEME, self.getName()) # Sets the theme to the selected theme

    class Manager (DataManager):
        """ Manages themes data """
        _DATAFILE_NAME = 'themes' # Only one file in this database. Sets the name of the database to 'themes'.
        
        def __init__(self):
            """ Initialise database. """
            super().__init__(os.path.dirname(__file__), DataManager.DatabaseType.DICT) # Define database properties.
        
        def createDatafile(self):
            """
                Raises exception when developer tries to create a new datafile. 

                Seeing as this database only needs one datafile to manage themes,
                this is set to prevent accidental/unnecessary actions.
            """
            raise DataManagerErrors.ActionNotAllowed()
        
        def deleteDatafile(self):
            """
                Raises exception when developer tries to delete a datafile. 

                If the datafile does not exist, themes will stop working.
                Although we have implemented a try-except block to avoid
                this being a fatal error, it would be better if the developer
                could not accidentally delete the file within the code.
            """
            raise DataManagerErrors.ActionNotAllowed()

        def getTheme(self, theme: "Themes.Themes") -> dict:
            """ Retrieve theme data by theme. """
            return self.getData(key=theme) # Returns a dictionary with themes data.

        def getData(self, identifier: str = None, key: "Themes.Themes" = None) -> dict:
            """ Retrieves data from the database for the given identifier and optional key. """
            data = super().getData(self._DATAFILE_NAME)  # Fetch data from parent class. Force search in the (only) datafile.

            # If key is provided, return the specific theme data, otherwise return all data
            if key is not None:
                return data.get(key.value, {}) # Return data for a specific key
            return data # Return all themes data. 

def runGame():
    """ Create new game instance to run the game. """
    assets.clear_console() # Clears the console
    assets.set_title("Play")
    game = Game() # Create new game class
    game.playGame() # Run game