class StrikeCommander_Category(object):
    """
        StrikeCommander_Category: object for client command categories

            Instance Attributes
                name (str): category name
                brief (str): formatted brief category name
                description (str): category description
                emoji (str): emoji for category
    """

    def __init__(self, name, brief, description, emoji):
        self.name = name
        self.brief = brief
        self.description = description
        self.emoji = emoji


class StrikeCommander_Data(object):
    """
        StrikeCommander_Data: object for Strike Commander client data

            Instance Attributes
                version (str): client version
                author (str): author of Strike Commander
                description (str): description of Strike Commander
                prefix (str): prefix for command calls
                embed_color (int): color integer for embed commands
                bot_categories (list): list of Bot_Category objects
    """

    version = '1.0.0'
    author = "Razgriz#7805"
    description = ("Clash of Clans discord bot for striking "
                   "users and members for missed attack, bad behavior, etc.")
    prefix = '/'
    # purple
    embed_color = 10181046
    bot_categories = [
        StrikeCommander_Category(
            'Super User', 'superuser',
            'Strike Commander commands for super user', '🧠'),
        StrikeCommander_Category(
            'User Strike', 'userstrike',
            'Strike Commander commands for User Strike', '🤖'),
        StrikeCommander_Category(
            'Player Strike', 'playerstrike',
            'Strike Commander commands for Player Strike', '😎'),
    ]
