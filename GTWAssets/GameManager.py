import sys
import random
from enum import Enum
from colorama import Fore, Back, Style, init
init() # initialies the colorma class

from lib.libData.DataManager import *
from lib.libForms.Form import *
import GlobalAssets as assets

class Game:
    """ Creates a new game instance and holds all of the data attributed to a running game. """

    def __init__(self) -> None:
        self.form = OptionForm("Choose Difficulty")

        self.form.addOption(WordManager.Difficulties.EASY.formatDifficulty(upperCase=True), lambda _: self.createWordManager(WordManager.Difficulties.EASY))
        self.form.addOption(WordManager.Difficulties.MEDIUM.formatDifficulty(upperCase=True), lambda _: self.createWordManager(WordManager.Difficulties.MEDIUM))
        self.form.addOption(WordManager.Difficulties.HARD.formatDifficulty(upperCase=True), lambda _: self.createWordManager(WordManager.Difficulties.HARD))
        self.form.addOption(Back.RED + Fore.WHITE + "Random" + Fore.RESET + Back.RESET, lambda _: self.createWordManager()) # WordData will handle cases where the difficulty is not set.

        self.form.settings.editSetting(
            FormSettings.Setting.HEADER,
            """
 ██████╗ ██╗   ██╗███████╗███████╗███████╗    ████████╗██╗  ██╗███████╗    ██╗    ██╗ ██████╗ ██████╗ ██████╗ 
██╔════╝ ██║   ██║██╔════╝██╔════╝██╔════╝    ╚══██╔══╝██║  ██║██╔════╝    ██║    ██║██╔═══██╗██╔══██╗██╔══██╗
██║  ███╗██║   ██║█████╗  ███████╗███████╗       ██║   ███████║█████╗      ██║ █╗ ██║██║   ██║██████╔╝██║  ██║
██║   ██║██║   ██║██╔══╝  ╚════██║╚════██║       ██║   ██╔══██║██╔══╝      ██║███╗██║██║   ██║██╔══██╗██║  ██║
╚██████╔╝╚██████╔╝███████╗███████║███████║       ██║   ██║  ██║███████╗    ╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝
 ╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚══════╝       ╚═╝   ╚═╝  ╚═╝╚══════╝     ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝                                                                                                                                                           
            """) # Creates a pretty header
        self.form.settings.editSetting(FormSettings.Setting.CLEAR_FORM_AFTER_FORM, True) # Clears the console after an option has been selected.

        self.form.send()

        self.foundLetterPositions = [] # Initialises the array with all of the correct letters. This will be the index to wher the correct letter is.
        self.correctLetters = [] # Initialises the array with all of the correct letters. This is an array of strings.
        self.incorrectLetters = [] # Initialises the array with all of the incorrect letters. This is an array of strings.

        self.lives = 10 # Starts life count at ten.

    def createWordManager(self, difficulty: 'WordManager.Difficulties' = None):
        self.wordManager = WordManager(difficulty)
        pass

    def playGame(self):
        self.sendGameBoard()

        def letterValidation(letter: str) -> bool:
            if not isinstance(letter, str):
                return False # Failsafe + makes the while loop start.

            isLetter = len(letter) == 1 and letter.lower().isalpha() # Returns true if the input is a valid letter
            notGuessed = letter.upper() not in self.incorrectLetters and letter.upper() not in self.correctLetters # Returns true if the letter has not previously been guessed.

            return isLetter and notGuessed

        letter = None
        firstIteration = True # Checks if the while loop has ran more than once.
        while not letterValidation(letter): # While the inputted letter is invalid.
            if firstIteration:
                firstIteration = False # Sets first iteration to false after the first iteration
            else:
                print("Error: Invalid letter.") # Notifies the player something went wrong.
            letter = input("Guess a letter: ") # Input for the letter

        word = self.wordManager.word # Stores the word in this easier variable 

        foundLetters = [i for i in range(len(word)) if word.startswith(letter, i)] # Finds positions where the letters in self.word is equal to the letter.
        
        def finishGame(win: bool = True) -> None:
            self.sendGameBoard(win) # Show winning board.
            input("\nPress enter to play again! ") # Holder for user to observe the board.
            runGame()

        if len(foundLetters) > 0: # If the player found a correct letter.
            self.foundLetterPositions.extend(foundLetters) # Extends the found positions to the total found positions variable.
            self.correctLetters.append(letter.upper()) # Add letter to correct letters
        else:
            self.incorrectLetters.append(letter.upper()) # Add letter to incorrect letters
            if self.lives > 1:
                self.lives -= 1 # Reduce one life.
            else:
                finishGame(False) # Stop game.


        if len(self.foundLetterPositions) == len(word): # Win validation
            finishGame()
        else:
            self.playGame() # Rerun this script to play the next tern.

    def sendGameBoard(self, win: bool = None):
        """
        Sends the top part of the gameboard.
        """

        assets.clear_console() # Clears the console

        word = self.wordManager.word # Saves word in a shorter variable

        print("Guess the word: " + self.wordManager.difficulty.formatDifficulty(upperCase=True) + f" MODE               {Fore.RED + self.lives * '♥️' + Style.RESET_ALL}") # Displays the mode

        # [PLACEHOLDER] Theme and game needs to go here

        gameLines = ["_ "] * len(word) # Creates a gameLines list comprised of one underscore for each letter of the word

        for i in self.foundLetterPositions:
            gameLines[i] = word[i].upper() + " "

        print()

        print("".join(gameLines)) # Converts array to a string.

        print()

        if len(self.incorrectLetters) > 0: # Only show incorrect letters if there are any.
            print(Fore.RED + "Incorrect letters: " + ", ".join(self.incorrectLetters) + Fore.RESET) # Format incorrect letters.

        print()

        if win != None:
            if win:
                print(Fore.GREEN + "YOU WIN!" + Fore.RESET)
            else:
                print(Fore.RED + "YOU LOSE!" + Fore.RESET)
                print(Fore.YELLOW + f"Word: {word.upper()}" + Fore.RESET)

class WordManager:
    """ Does everything word-related. All functions relating to the individual words of the game are located here. """
    
    def __init__(self, difficulty: 'WordManager.Difficulties' = None) -> None:
        if not isinstance(difficulty, WordManager.Difficulties):
            # If difficulty was set to None (for randomisation) or an invalid type, randomise difficulty to avoid an error.
            difficulty = random.choice(list(WordManager.Difficulties))  # Randomly select a difficulty
        
        self.difficulty = difficulty

        class LoadingBarStatus (Enum):
            """
            Statuses to tell the systems which messages to display.
            """
            DOWNLOADING_WORDS = 0
            FILTERING_WORDS = 1
            RANDOMISING_WORDS = 2
            CHOOSING_WORD = 3
            pass

        class CorpusType (Enum):
            """ Defines corpus names for easy access """
            WORDS = 'words' # Type storing a large repository of words in English
            COMMON = 'brown' # Type storing repository of common words in English
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
            bar = Style.BRIGHT + '[' + Fore.GREEN + '=' * filled_length + Fore.RED + ' ' * (bar_length - filled_length) + ']' + Style.RESET_ALL # Progress bar

            print(f"\n{bar} {int(percentage * 100)}%\n") # Print the progress bar with percentage

            # Print the corresponding status message
            if status.value >= LoadingBarStatus.DOWNLOADING_WORDS.value:
                print("\nDownloading words...")
            if status.value >= LoadingBarStatus.FILTERING_WORDS.value:
                print("\nFiltering words...")
            if status.value >= LoadingBarStatus.RANDOMISING_WORDS.value:
                print("\nRandomising words...")
            if status.value >= LoadingBarStatus.CHOOSING_WORD.value:
                print("\nChoosing word...")
    
        sendLoadingBar(LoadingBarStatus.DOWNLOADING_WORDS)

        import nltk # Import the Natural Language Toolkit

        corpusType = None
        if difficulty == WordManager.Difficulties.EASY: # Settings to configure if difficulty is easy
            min_len, max_len = 4, 5 # Define word length range based on difficulty
            corpusType = CorpusType.COMMON
        elif difficulty == WordManager.Difficulties.MEDIUM: # Settings to configure if difficulty is Medium
            min_len, max_len = 6, 7 # Define word length range based on difficulty
            if random.randint(0, 1) == 0: # Randomly choose word processor
                corpusType = CorpusType.COMMON
            else:
                corpusType = CorpusType.WORDS
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

        sendLoadingBar(LoadingBarStatus.FILTERING_WORDS)
        # Select the correct corpus based on corpusType
        if corpusType == CorpusType.COMMON:
            word_list = [word.lower() for word in brown.words() if min_len <= len(word) <= max_len]
        elif corpusType == CorpusType.WORDS:
            word_list = [word.lower() for word in words.words() if min_len <= len(word) <= max_len]

        sendLoadingBar(LoadingBarStatus.RANDOMISING_WORDS)
        random.shuffle(word_list) # Shuffle the word list
        self.word = random.choice(word_list)

        sendLoadingBar(LoadingBarStatus.CHOOSING_WORD)

    class Difficulties (Enum):
        EASY = "Easy"
        MEDIUM = "Medium"
        HARD = "Hard"

        def getColour(self) -> str:
            """
            Return the appropriate color for each difficulty.
            """
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
                    - None: No case changes
                    - False: Force lower case
                    - True: Force upper case 

            Returns:
                str: The formatted difficulty string with color and desired case formatting.
            """
            # Apply case formatting based on the passed formatCase argument
            name = self.value
            if upperCase:
                name = name.upper()
            elif upperCase != None:
                name = name.lower()

            # Apply color formatting
            return self.getColour() + name + (resetColour if isinstance(resetColour, str) else Fore.RESET)


def runGame():
    assets.clear_console() # Clears the console
    game = Game() # Create new game class
    game.playGame() # Run game

if __name__ == "__main__":
    runGame()