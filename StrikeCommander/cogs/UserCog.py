import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands
from responders.ResponderModel import ResponderModel
from database.UserStrike import UserStrike
from responders import (
    DiscordResponder as discord_responder,
    RazBotDB_Responder as db_responder,
    UserStrikeResponder as user_strike_responder)
from utils import discord_utils


class User(commands.Cog):
    def __init__(self, bot, coc_client, client_data):
        self.bot = bot
        self.coc_client = coc_client
        self.client_data = client_data

    # user
    @commands.slash_command()
    async def user(self, inter):
        """
            parent for user commands
        """

        # defer for every user command
        await inter.response.defer()

    @user.sub_command()
    async def show(
        self,
        inter: ApplicationCommandInteraction,
        option: str = discord_utils.command_param_dict['userstrike_show']
    ):
        """
            user show command
            
            Parameters
            ----------
            option (optional): options for user show command
        """

        db_user = db_responder.read_user(discord_user_id=inter.author.id)

        if db_user is None:
            embed_description = (
                f"could not find user with id {inter.author.id} "
                f"in the database")

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                description=embed_description,
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        if option == "overview":
            response = (
                await user_strike_responder.get_user_strike_message_overview(
                    user=inter.author,
                    inter=inter,
                    coc_client=self.coc_client))

        elif option == "active":
            response = (
                await user_strike_responder.get_user_strike_message_active(
                    user=inter.author,
                    inter=inter,
                    coc_client=self.coc_client))

        elif option == "all":
            response = (
                await user_strike_responder.get_user_strike_message_all(
                    user=inter.author,
                    inter=inter,
                    coc_client=self.coc_client))

        else:
            response = ResponderModel(
                field_dict_list=[{
                    'name': "incorrect option selected",
                    'value': "please select a different option"
                }])

            response.embed_list.append(discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                title=response.title,
                description=response.description,
                bot_user_name=inter.me.display_name,
                field_list=response.field_dict_list,
                author=inter.author))

        await discord_responder.send_embed_list(
            inter,
            response.embed_list,
            content=response.content)
