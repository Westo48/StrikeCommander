import disnake
import coc
from disnake.ext import commands
from cogs import (
    events as events_cog,
    help as help_cog,
    superuser as super_user_cog,
    ModelsCog as models_cog,
    UserCog as user_cog,
    PlayerStrikeCog as player_strike_cog,
    UserStrikeCog as user_strike_cog
)
from data import StrikeCommander_Client_Data
from responders.ClientResponder import (
    get_client_email,
    get_client_password,
    get_client_test_guilds,
    get_client_token
)

client_data = StrikeCommander_Client_Data.StrikeCommander_Data()

coc_client = coc.login(
    email=get_client_email(),
    password=get_client_password()
)

intents = disnake.Intents.default()
intents.members = True

bot = commands.InteractionBot(
    intents=intents,
    test_guilds=get_client_test_guilds())

bot.add_cog(help_cog.Help(
    bot, coc_client, client_data))
bot.add_cog(events_cog.Events(
    bot, coc_client, client_data))
bot.add_cog(super_user_cog.SuperUser(
    bot, coc_client, client_data))
bot.add_cog(models_cog.Models(
    bot, coc_client, client_data))
bot.add_cog(user_cog.User(
    bot, coc_client, client_data))
bot.add_cog(player_strike_cog.PlayerStrike(
    bot, coc_client, client_data))
bot.add_cog(user_strike_cog.UserStrike(
    bot, coc_client, client_data))

if __name__ == "__main__":
    bot.run(get_client_token())
