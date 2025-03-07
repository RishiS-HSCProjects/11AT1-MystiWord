import os
import random
from enum import Enum
from colorama import Fore, Back, init
init() # initialies the colorma class

from lib.libData.DataManager import DataFields, DataManager
from lib.libForms.Form import *

class Game:
    """ Creates a new game instance and holds all of the data attributed to a running game. """

    def __init__(self) -> None:
        self.form = OptionForm("Choose Difficulty")

        for difficulty in list(WordManager.Difficulties): # Cycles through difficulties and adds an option for them.
            self.form.addOption(difficulty.formatDifficulty(), lambda _: self.createWordManager(difficulty))
        self.form.addOption(Back.RED + Fore.WHITE + "Random" + Fore.RESET + Back.RESET, lambda _: self.createWordManager()) # WordData will handle cases where the difficulty is not set.

        self.form.settings.editSetting(FormSettings.Setting.HEADER, "/...........\\") # Creates a pretty header
        self.form.settings.editSetting(FormSettings.Setting.CLEAR_FORM_AFTER_FORM, True) # Clears the console after an option has been selected.

        self.form.send()

        self.foundLetterPositions = [] # Initialises the array with all of the correct letters. This will be the index to wher the correct letter is.
        self.incorrectLetters = [] # Initialises the array with all of the incorrect letters. This is an array of strings.

    def createWordManager(self, difficulty: 'WordManager.Difficulties'):
        self.wordManager = WordManager(difficulty)
        pass

    def playGame(self):
        os.system("cls" if os.name == "nt" else "clear")

        self.sendGameBoard()

        def letterValidation(letter: str) -> bool:
            if not isinstance(letter, str):
                return False # Failsafe + makes the while loop start.
            return len(letter) == 1 and letter.lower().isalpha() # Returns true if the input is a valid letter

        letter = None
        firstIteration = True # Checks if the while loop has ran more than once.
        while not letterValidation(letter): # While the inputted letter is invalid.
            if firstIteration:
                firstIteration = False # Sets first iteration to false after the first iteration
            else:
                print("Error: Invalid letter.") # Notifies the player something went wrong.
            letter = input("Guess a letter: ") # Input for the letter

        word = self.wordManager.wordData.word # Stores the word in this easier variable 

        self.foundLetterPositions.extend([i for i in range(len(word)) if word.startswith(letter, i)]) # Finds positions where the letters in self.word is equal to the letter. Extends the found positions to the total found positions variable.

        if len(self.foundLetterPositions) == len(word): # Win validation
            pass
        else:
            self.playGame()

    def sendGameBoard(self):
        """
        Sends the top part of the gameboard.
        """
        wordData = self.wordManager.wordData # Saves wordData in a shorter variable
        word = wordData.word # Saves word in a shorter variable

        print("Guess the word: " + wordData.difficulty.formatDifficulty().upper() + " MODE") # Displays the mode

        # [PLACEHOLDER] Theme and game needs to go here

        gameLines = ["_ "] * len(word) # Creates a gameLines list comprised of one underscore for each letter of the word

        for i in self.foundLetterPositions:
            gameLines[i] = word[i]

        print()

        print("".join(gameLines)) # Converts array to a string.

        print()

        if len(self.incorrectLetters) > 0: # Only show incorrect letters if there are any.
            print(Fore.RED + "Incorrect letters: " + ", ".join(self.incorrectLetters)) # Format incorrect letters.

class WordManager:
    """ Does everything word-related. All functions relating to the individual words of the game are located here. """
    
    def __init__(self, difficulty: 'WordManager.Difficulties' = None) -> None:
        self.wordData = self.WordData(difficulty)

    class Difficulties (Enum):
        """ Enum class storing the difficulty """
        EASY = "Easy"
        MEDIUM = "Medium"
        HARD = "Hard"

        def getColour(self) -> str:
            """
            Returns the assigned colour for a difficulty
            """
            if self == self.EASY:
                return Fore.GREEN
            elif self == self.MEDIUM:
                return Fore.YELLOW
            elif self == self.HARD:
                return Fore.RED
            
        def formatDifficulty(self, resetColour: str = None) -> str:
            """
            Returns a formatted string of the difficulty name.
            
            If you want names to be forced into upper or lower, please use the .upper()/.lower() functions respectively.
                Example:
                ```python
                    Difficulties.formatDifficulty(Difficulties.EASY, Fore.BLUE).upper()
                ```

            Attributes:
                resetColour:
                    - Fore.XYZ -> Use the colorma class to set what colour you want the string to reset to
                    - False -> Keeps the colour of the difficulty
                    - None (default) -> Resets to the default console colour.
            """
            return self.getColour() + self.value + (resetColour if isinstance(resetColour, str) else "" if resetColour == False else Fore.RESET) # Returns the colour, difficulty name and reset colours joined together.
        pass

    class WordData (DataManager):
        def __init__(self, difficulty: 'WordManager.Difficulties' = None):
            super().__init__(os.path.join(os.path.dirname(__file__), "wordsLibrary")) # Argument 0 sets the database's datapath to "...\\GTWAssets\wordsLibrary"


            if isinstance(difficulty, WordManager.Difficulties): # If the difficulty is of a valid type
                self.difficulty = difficulty # Make difficulty globally accessible
            else: # If difficulty was set to None (for randomisation) or an invalid type, randomise difficulty to avoid an error.
                self.difficulty = random.choice(list(WordManager.Difficulties))  # Randomly select a difficulty

            database = self.getData(difficulty.value) # Converts .json script to a dictionary
            self.word = random.choice(list(database.items())) # Returns a random word
            self.wordList = list(self.word)

        def createDatafile(self, identifier: str):
            # We don't want the software creating difficulties into this program. Overriding this function will stop the software from accidentally doing that.
            raise NotImplementedError("Creating new difficulties is not allowed in this database.")
        
        def setData(self, identifier: str, field: DataFields, newVal) -> None:
            # We also don't want the software editing any words in the database. Overriding this function will stop the software from accidentally doing that.
            raise NotImplementedError("Editing and creating words are not allowed in this database.")

if __name__ == "__main__":
    game = Game()
    game.playGame()