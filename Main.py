from colorama import Fore, Style

from lib.libForms.Form import *
from lib.libData.DataManager import *
import GlobalAssets as assets
from GameManager import runGame, WordManager, Themes
from auth import PlayerData, LocalData, Auth

def sendHomePage() -> None:
    """ Send homepage. Sends login form if no player is logged in. """
    assets.clear_console() # Clears the console
    settings = FormSettings() # Initialises common form settings
    settings.editSetting(FormSettings.Setting.HEADER, assets.getTitle()) # Sets header to title.
    settings.editSetting(FormSettings.Setting.CLEAR_FORM_AFTER_FORM, True) # Sets form to clear after interaction
    settings.editSetting(FormSettings.Setting.CLEAR_FORM_AFTER_ACTION, True) # Sets form to clear after every action (input forms)

    if (assets.logged_in_player): # Returns true if logged_in_player is not None (therefore, logged in)
        form = OptionForm(f"Hello, {assets.logged_in_player}", settings=settings) # Greats logged in player
        form.addOption(Fore.GREEN + "Play", runGame) # Opens game menu.

        def sendStatsMenu() -> None:
            """ Function to send the stats menu """
            assets.clear_console() # Clear console

            print(assets.getTitle()) # Print title

            playerManager = assets.getPlayerManager() # Get player manager
            getData = lambda field: playerManager.getData(assets.logged_in_player, field) # Get player data

            # Print stats menu
            print(f"""
Stats:
  {Fore.LIGHTGREEN_EX}XP: {getData(PlayerData.PlayerDataFields.XP)}{Style.RESET_ALL}
  Games Played: {playerManager.getGamesPlayed(assets.logged_in_player)}
  Wins: {getData(PlayerData.PlayerDataFields.WINS)}
  Losses: {getData(PlayerData.PlayerDataFields.LOSSES)}
  WLR: {playerManager.getWLR(assets.logged_in_player)}
  Points per Win Average: {round(int(getData(PlayerData.PlayerDataFields.XP)) / int(getData(PlayerData.PlayerDataFields.WINS)), 2) if int(getData(PlayerData.PlayerDataFields.WINS)) > 0 else "N/A"}
  Easy PB: {playerManager.getPB(assets.logged_in_player, WordManager.Difficulties.EASY.value) or "N/A"}
  Medium PB: {playerManager.getPB(assets.logged_in_player, WordManager.Difficulties.MEDIUM.value) or "N/A"}
  Hard PB: {playerManager.getPB(assets.logged_in_player, WordManager.Difficulties.HARD.value) or "N/A"}
            """)

            assets.pause(Style.DIM) # Pause console to observe stats.

            sendHomePage() # Send home page after stats are observed.
        form.addOption(Fore.LIGHTMAGENTA_EX + "Stats", sendStatsMenu) # Add stats option to form

    
        def sendShop() -> None:
            """ Function to send the shop UI. """
            form = OptionForm("Shop", "Spend your coins on cool items!", settings=settings) # Create shop form

            coins = assets.getPlayerManager().getData(assets.logged_in_player, PlayerData.PlayerDataFields.COINS) # Get number of coins the player has in their bank.
            form.addSeparator(Fore.YELLOW + f"Coins: {coins}") # Display number of coins

            for theme in Themes.Themes: # Loop through all themes
                cost = theme.getCost() # Get the cost of the theme
                form.addOption( # Add an option for each theme to the form for interaction.
                    theme.getName(), # Set option name to theme name
                    lambda self=None, theme=theme: theme.handlePurchase(), # Call handlePurchase() on selection
                    Fore.LIGHTGREEN_EX + "Equipped" if (theme.getName() == assets.getPlayerManager().getData(assets.logged_in_player, PlayerData.PlayerDataFields.EQUIPPED_THEME)) # Set text to Equipped if equipped
                    else (Fore.YELLOW + "Unequipped" # Set text to Unequipped otherwise if purchased
                        if (theme.getName() in assets.getPlayerManager().getData(assets.logged_in_player, PlayerData.PlayerDataFields.THEMES)) # Check if theme is purchased.
                        else f"Cost: {Fore.RED if cost > coins else Fore.GREEN}{cost} coins") # Display cost if not already purchased
                )

            form.addOption(Fore.RED + "🔴 Back", sendHomePage) # Adds option to go back to the homepage

            form.send() # Send the form

            sendShop() # Sends the shop on every interaction (except back) to update the coin and theme displays.
            pass
        form.addOption(Fore.YELLOW + "Shop", sendShop) # Add shop option to the form

        def sendSettingsMenu() -> None:
            """ Sends settings menu to user to edit game and profile settings. """

            from copy import deepcopy

            form = OptionForm("Settings", "Enter a setting option to toggle it.", settings) # Create settings form
            form.settings.editSetting(FormSettings.Setting.HEADER, f"{assets.getTitle()}\n\n<--------------⚙️-------------->") # Set header for form

            local = assets.getLocalData() # Get local data

            def toggleSetting(setting: LocalData.LocalDataFields.Settings) -> None:
                """ Toggle setting within data """
                local.setDataField(setting, not local.getDataField(setting)) # Toggle the setting
                sendSettingsMenu() # Refresh the settings menu

            form.settings.editSetting(FormSettings.Setting.OPTIONS_TEXT, Fore.LIGHTBLUE_EX + "Settings:")

            form.addSeparator(Fore.YELLOW + f"\nGame Settings{Fore.RESET}:")
            for setting in LocalData.LocalDataFields.Settings: # Loop through all settings
                form.addOption(Fore.YELLOW + setting.value, lambda self=None, setting=setting: toggleSetting(setting), local.getDataField(setting) and Fore.GREEN + "✅" or Fore.RED + "❌") # Add option to toggle the setting

            playerManager = assets.getPlayerManager()

            form.addSeparator(Fore.LIGHTCYAN_EX + f"\nAccount Settings{Fore.RESET}:") # Add account settings heading separator
            if (assets.logged_in_player == assets.get_guest_identifier()): # If the player is a guest
                def portStats() -> None:
                    """ Function to display the UI for porting GUEST stats to a new player. """
                    portStatsSettings = deepcopy(settings) # Copy instance of settings
                    portStatsSettings.editSetting(FormSettings.Setting.HEADER, f"{assets.getTitle()}\n\n<--------------🔁-------------->") # Set header for form
                    form = InputForm("Port Stats", settings=portStatsSettings) # Create input form with the new portStatsSettings

                    form.registerTextInput( # Register username field, including field validation
                        "Username", # Title text input
                        validation=lambda input: # Pass through the input as a parameter of the verification function.
                            ("Username already exists" if playerManager.datafileExists(input) else False) or # Return error if user already exists
                            ("Invalid Username: Please only use letters (a-z) in your username. Do not use spaces or other special characters." if not input.isalnum() else # Return error if the username is not alphanumerical
                            False # Return false to show verification passed
                    ))
                    username = form.send()["Username"][InputForm.DataEntryConsts.RESPONSE].lower() # Set username variable to a lowercase version of the above response
                    
                    form = InputForm("Port Stats", settings=portStatsSettings) # Create a new input form with portStatsSettings
                    form.addSeparator(f"Username: {username}") # Display username.
                    form.registerTextInput("Password") # Registers a text input for the password
                    password = form.send()["Password"][InputForm.DataEntryConsts.RESPONSE] # Set password variable

                    form = OptionForm("Confirm New Account", f"Please confirm the below details:\n  - Username: {username}\n  - Password: {password if password else Fore.RED + 'NOT SET' + Style.RESET_ALL}", settings=settings) # Create confirmation form displaying the username and password.
                    form.addOption(Fore.GREEN + "✅ CONFIRM" + Style.RESET_ALL, lambda: None) # Adds option to confirm the new account. Callback does nothing.
                    form.addOption(Fore.RED + "❌ Cancel" + Style.RESET_ALL, sendSettingsMenu) # Adds option to retry or cancel port. Callback sends the settings form.
                    form.send() # Sends form to player

                    # The following is executed if the user confirmed the action.
                    playerManager.renameDatafile(assets.get_guest_identifier(), username) # Rename the guest datafile to the new username
                    playerManager.setData(username, PlayerData.PlayerDataFields.IDENTIFIER, username) # Set the username for the new account
                    playerManager.setData(username, PlayerData.PlayerDataFields.PASSWORD, password) # Set the password for the new account
                    assets.logged_in_player = username # Set the logged in player to the newly created player.
                    sendHomePage() # Return to the home page

                form.addOption(Fore.LIGHTCYAN_EX + "Port Guest Stats", lambda: portStats(), "Port guest stats to a new player.") # Add option to port guest stats calling the portStats function if selected.
            else: # If a player is logged in
                # Logic for changing username/password.
                def changeUsername() -> None:
                    """ Prompts the user to change their username """
                    form = InputForm("Change Username", settings=settings) # Creates a new input form
                    form.registerTextInput("New Username", tooltip="Leave empty to go back", validation=lambda input: "Username already exists" if Auth.doesUserExist(input.lower()) and input != "" else False) # Register a new text input for the username
                    new_username = form.send()["New Username"][InputForm.DataEntryConsts.RESPONSE].lower() # Store the new username

                    if new_username == "":
                        sendSettingsMenu() # If operation is aborted, go back to the Settings Form.

                    form = OptionForm("Confirm Username Change", f"Are you sure you want to change your username to '{new_username}'?", settings=settings) # Create name change confirmation from

                    def handleUsernameChange():
                        """ Handle the username change """

                        playerManager.renameDatafile(assets.logged_in_player, new_username) # Rename datafile of the currently logged in player to the new player
                        playerManager.setData(new_username, PlayerData.PlayerDataFields.IDENTIFIER, new_username) # Update identifier to the new username
                        assets.logged_in_player = new_username # Set the logged-in player to the new username

                        assets.getLocalData().setDataField(LocalData.LocalDataFields.LAST_LOGGED_IN, new_username) # Update the last logged-in player to the new username

                        sendHomePage() # After the change, return to the homepage

                    form.addOption(Fore.GREEN + "✅  CONFIRM" + Style.RESET_ALL, handleUsernameChange) # Add confirm option. Handle name change on confirmation.
                    form.addOption(Fore.RED + "❌  CANCEL" + Style.RESET_ALL, sendSettingsMenu) # Add cancel option. Goes back to the settings menu.

                    form.send() # Send username change form to the player

                def changePassword() -> None:
                    """ Prompts the user to change their password """
                    form = InputForm("Change Password", settings=settings) # Creates new input form for password change 
                    form.registerTextInput("New Password", tooltip="Enter a new password. Leave empty to unset")
                    new_password = form.send()["New Password"][InputForm.DataEntryConsts.RESPONSE]

                    if new_password == "": # If user prompts to unset password
                        new_password = None # Set new_password to none to unset.

                    form = OptionForm("Confirm Password Change", f"Are you sure you want to {'change' if new_password else 'unset'} your password{' to ' + Fore.CYAN + new_password + Fore.RESET if new_password else ''}?", settings=settings) # Create password change confirmation form.

                    def handlePasswordChange():
                        """ Handle the password change """
                        playerManager.setData(assets.logged_in_player, PlayerData.PlayerDataFields.PASSWORD, new_password) # Set the new password

                        sendHomePage() # After the change, return to the homepage

                    form.addOption(Fore.GREEN + "✅ CONFIRM" + Style.RESET_ALL, handlePasswordChange) # Add confirm option. Handle password change on confirmation.
                    form.addOption(Fore.RED + "❌ CANCEL" + Style.RESET_ALL, sendSettingsMenu) # Add cancel option. Goes back to the settings menu.

                    form.send() # Show the form to confirm the password change

                def deleteAccount() -> None:
                    """ Confirms with the user to delete their account. """

                    deleteAccountSettings = deepcopy(settings) # Copies settings
                    deleteAccountSettings.editSetting(FormSettings.Setting.HEADER, f"{assets.getTitle()}\n\n{Fore.RED}<--------------🛑-------------->")
                    deleteAccountSettings.editSetting(FormSettings.Setting.SEPARATOR, f"{Fore.RED}<--------------🛑-------------->")
                    deleteAccountSettings.editSetting(FormSettings.Setting.CLEAR_FORM_AFTER_ACTION, False)

                    form = OptionForm(Fore.RED + "Confirm Account Deletion", f"Are you sure you want to delete your account, {Fore.CYAN + assets.logged_in_player + Fore.RESET}?\n\nThis is an irreversible action.\n", settings=deleteAccountSettings)

                    def handleAccountDeletion():
                        """ Ask for the user's username and password to confirm. """
                        form = InputForm("Confirm Account Details", settings=deleteAccountSettings) # Create form

                        def handleEmptyField(username: bool) -> None:
                            """ Exits out of account deletion menu if a field is empty. 

                                Pass through username=true for username and username=false for password
                            """
                            
                            if form.inputs['Username' if username else 'Password'][InputForm.DataEntryConsts.RESPONSE] == "": # If field is empty
                                assets.clear_console() # Clear console
                                sendSettingsMenu() # Go back to settings menu

                        form.registerTextInput(
                            name="Username",
                            tooltip="Enter your username to confirm. Leave blank to cancel",
                            validation=lambda input: "Incorrect username" if input != assets.logged_in_player and input != "" else False,
                            callback = lambda: handleEmptyField(True)
                        )

                        password = playerManager.getData(assets.logged_in_player, PlayerData.PlayerDataFields.PASSWORD)
                        if password:
                            form.registerTextInput(
                                name="Password",
                                tooltip="Enter your password to confirm. Leave blank to cancel",
                                validation=lambda input: "Incorrect password" if input != password and input != "" else False,
                                callback = lambda: handleEmptyField(False)
                            )

                        form.send()

                        # Proceed with deletion if username and password are correct
                        playerManager.deleteDatafile(assets.logged_in_player) # Deletes the player's data file
                        assets.logged_in_player = None  # Logout the player
                        assets.getLocalData().setDataField(LocalData.LocalDataFields.LAST_LOGGED_IN, None)

                        sendHomePage()  # Redirect to the homepage (i.e. login page)

                    form.addOption(Fore.GREEN + "✅ CONFIRM DELETE" + Style.RESET_ALL, handleAccountDeletion)  # Confirm delete
                    form.addOption(Fore.RED + "❌ CANCEL" + Style.RESET_ALL, sendSettingsMenu)  # Cancel action and return to settings

                    form.send()  # Show confirmation form

                form.addOption(Fore.LIGHTCYAN_EX + "Change Username", changeUsername) # Option to change username
                form.addOption(Fore.LIGHTCYAN_EX + "Change Password", changePassword) # Option to change password
                form.addOption(Fore.LIGHTRED_EX + "Delete Account", deleteAccount) # Option to change password
            form.addSeparator() # Add separator

            form.addOption(Fore.RED + "🔴 Back", sendHomePage) # Adds option to go back to the home page

            form.send() # Send form to player.
        form.addOption(Fore.LIGHTBLUE_EX + "Settings", sendSettingsMenu) # Add option to open the settings menu of an account.

        def logout() -> None:
            """ Sends a menu confirming a logout action. """
            form = OptionForm(f"Hey, {assets.logged_in_player}!", Fore.LIGHTRED_EX + "Are you sure you want to log out?", settings=settings) # Create confirmation form for the logout
            def handleLogout() -> None:
                """ Function to handle the logout (at this point, only deleting the temporary logged_in_player field.) """
                assets.logged_in_player = None # Properly log out the user
            form.addOption(Fore.GREEN + "✅ CONFIRM" + Style.RESET_ALL, handleLogout) # Adds option to confirm the new account. 
            form.addOption(Fore.RED + "❌ Back" + Style.RESET_ALL, lambda: None) # Adds option cancel logout.
            form.send() # Sends form

            sendHomePage() # Return to the homepage (or login page if user logged out.)
        form.addOption(Fore.RED + "Log Out", logout) # Add option to log out of an account.
        
        form.send() # Send homepage form to player.
    else:
        sendLoginFrom() # Send login form to player if no player is signed in

def sendLoginFrom() -> None:
    """ Sends a form with all login options to the player. """
    from auth.PlayerData import PlayerDataFields as fields

    def sendSignIn() -> None:
        """ Sends a sign in form to the user. """
        last_logged_in = assets.getLocalData().getDataField(LocalData.LocalDataFields.LAST_LOGGED_IN) # Get the last logged in player

        form = InputForm("Sign In", settings=settings) # Creates a sign-in form
        form.registerTextInput( # Registers a text input with validation ensuring the user exists.
            "Username", # Input name
            tooltip=f"Leave empty to autofil to '{Fore.CYAN + last_logged_in + Fore.RESET}'" if last_logged_in else "Leave empty to go back", # Tooltip for exit/autofill
            validation=lambda input: ( # Validation code
                "Username does not exist" if not Auth.doesUserExist(input.lower()) and input != "" else # Check that username does not exist (or is empty)
                ("Invalid Username: Please only use letters (a-z) in your username. Do not use spaces or other special characters."  if not input.isalnum() and input != "" else # Invalid if username is not alphanumeric 
                False # False means username is valid
                )
            )
        )
        username = form.send()["Username"][InputForm.DataEntryConsts.RESPONSE].lower() # Set username variable to a lowercase version of the above response
        if username == "": # Checks if usernme is empty
            if last_logged_in: # Checks if last_logged_in field is available
                username = last_logged_in # Autofills username to last logged in if no username provided.
            else: # If no last_logged_in player...
                sendLoginFrom() # Operation is aborted, go back to the Login Form.

        password = assets.getPlayerManager().getData(username, fields.PASSWORD) # Get the expected password of the player
        if password: # Check if the player has a password set
            form = InputForm("Sign In", settings=settings) # Re-create sign-in form if username passed validation
            form.addSeparator(f"Username: {username}") # Display username.
            try:
                form.registerTextInput("Password", # Register password input
                    tooltip="Leave empty to go back", # Add back tooltip
                    validation=lambda input: # Assign verification lambda
                        "Password Incorrect" if not input == password and input != "" # Return password incorrect if incorrect password and not empty (for back function)
                        else False # Return False for no validation error (password correct or empty)
                )
                if form.send()["Password"][InputForm.DataEntryConsts.RESPONSE] == "": # Check if password is empty to see if user wants to go back
                    sendLoginFrom() # Send login form on back
            except json.decoder.JSONDecodeError:
                print(Fore.RED + "File corrupted. Please sign up for a new account.\n" + Style.RESET_ALL) # Sends warning
                assets.pause()

                sendSignUp()
                return

        assets.logged_in_player = username # Set the logged in player to this player. Username acts as the player identifier.
        assets.getLocalData().setDataField(LocalData.LocalDataFields.LAST_LOGGED_IN, username) # Set the last logged in player to this player.

    def sendSignUp() -> None:
        """ Sends a sign in form to the user. """
        form = InputForm("Sign Up", settings=settings) # Creates a sign-up forms
        form.registerTextInput("Username", tooltip="Leave empty to go back", validation=lambda input: "Username already exists" if Auth.doesUserExist(input.lower()) else False) # Registers a text input with validation ensuring the user does not already exist.
        username = form.send()["Username"][InputForm.DataEntryConsts.RESPONSE].lower() # Set username variable
        if username == "":
            sendLoginFrom() # If operation is aborted, go back to the Login Form.

        form = InputForm("Sign Up", settings=settings) # Re-creates the sign-up form
        form.addSeparator(f"Username: {username}") # Display username.
        form.registerTextInput("Password") # Registers a text input for the password
        password = form.send()["Password"][InputForm.DataEntryConsts.RESPONSE] # Set password variable

        form = OptionForm("Confirm New User", f"Please confirm the below details:\n  - Username: {username}\n  - Password: {password if password else Fore.RED + 'NOT SET' + Style.RESET_ALL}", settings=settings) # Create confirmation form displaying the username and password

        def createPlayer():
            """ Creates a player datafile """
            playerManager = assets.getPlayerManager() # Get player manager 
            playerManager.createDatafile(username) # Create the datafile. This will automatically add the default values.
            playerManager.setData(username, fields.PASSWORD, password) # Set the password to the datafile.
        form.addOption(Fore.GREEN + "✅ CONFIRM" + Style.RESET_ALL, createPlayer) # Adds option to confirm the new account. 

        form.addOption(Fore.RED + "❌ RETRY" + Style.RESET_ALL, sendSignUp) # Adds option to retry sign-up.

        form.send() # Sends form to player

    def registerGuest() -> None:
        """ Opens terminal for a guest """

        playerManager = assets.getPlayerManager() # Assigns player manager

        guest_exists = playerManager.datafileExists(assets.get_guest_identifier()) # Checks if guest datafile already exists

        def createGuestProfile() -> None:
            """ Create a new guest profile """
            if guest_exists: # If a guest already exists
                playerManager.deleteDatafile(assets.get_guest_identifier()) # Deletes existing datafile
            
            playerManager.createDatafile(assets.get_guest_identifier()) # Creates a stock guest datafile with clean settings and values.
            
        if guest_exists: # If a guest already exists
            form = OptionForm("Create Guest Profile", "A guest profile already exists. Would you like to continue using that?", settings) # Option form to override guest profile
            form.setBody(f"""Stats:
  XP: {playerManager.getData(assets.get_guest_identifier(), PlayerData.PlayerDataFields.XP)}
  Games Played: {playerManager.getGamesPlayed(assets.get_guest_identifier())}""") # Display some guest stats to users can observe whether or not they want to override it.
            form.addOption(Fore.GREEN + "✅  Yes, continue guest account!" + Style.RESET_ALL, lambda: None) # Continues with existing profile
            form.addOption(Fore.RED + "❌  No, reset stats and create a new guest account!" + Style.RESET_ALL, createGuestProfile) # Overrides profile and creates a new guest account
            form.addOption(Fore.LIGHTBLACK_EX + "Back to Login Page", sendLoginFrom) # Return back to login page

            form.send() # Sends form
        else:
            createGuestProfile() # Creates guest profile
    
        assets.logged_in_player = assets.get_guest_identifier() # Sets logged in player to guest
        sendHomePage() # Send the homepage.

    assets.clear_console() # Clears the console
    settings = FormSettings() # Initialises common form settings
    settings.editSetting(FormSettings.Setting.HEADER, f"{assets.getTitle()}\n\n<--------------🔒-------------->")
    settings.editSetting(FormSettings.Setting.CLEAR_FORM_AFTER_FORM, True)
    settings.editSetting(FormSettings.Setting.CLEAR_FORM_AFTER_FORM, True)

    form = OptionForm("Get Started", "Please log in to get started! You can also play as a temporary guest.", settings) # Create Login Options Form
    form.addOption("🔐  Sign In", lambda: sendSignIn(), "Login to an existing account.") # Sign in option
    form.addOption("➕  Sign Up", lambda: sendSignUp(), "Create a new account.") # Sign up option
    form.addOption("👤  Play as Guest", lambda: registerGuest(), "You will be able to port your stats later on.") # Play as guest option
    form.addOption("🔴  Exit", lambda: exit()) # Quit app if this option is selected

    form.send() # Sends the form

    sendHomePage() # Open home page unless any process is aborted.

if __name__ == "__main__":
    assets.logged_in_player = None # Logs out player
    sendHomePage() # Send homepage (usually will be the login page)