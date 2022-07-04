import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands
from responders.ResponderModel import ResponderModel
from coc.players import Player
from database.PlayerStrike import PlayerStrike
from database.UserStrike import UserStrike
from responders import (
    DiscordResponder as discord_responder,
    ClashResponder as clash_responder,
    RazBotDB_Responder as db_responder,
    PlayerStrikeResponder as player_strike_responder,
    UserStrikeResponder as user_strike_responder,
    AuthResponder as auth_responder)
from utils import discord_utils
from disnake.utils import get
from errors.errors_db import (
    NotFoundError,
    ConflictError)


class UserStrike(commands.Cog):
    def __init__(self, bot, coc_client, client_data):
        self.bot = bot
        self.coc_client = coc_client
        self.client_data = client_data

    # user strike
    @commands.slash_command()
    async def userstrike(self, inter):
        """
            parent for user strike commands
        """

        # defer for every user strike command
        await inter.response.defer()

    @userstrike.sub_command()
    async def show(
        self,
        inter: ApplicationCommandInteraction,
        option: str = discord_utils.command_param_dict['userstrike_show'],
        user: disnake.User = discord_utils.command_param_dict['required_user']
    ):
        """
            user strike show command

            Parameters
            ----------
            option (optional): options for user strike show command
            user (User): user to show strikes for
        """

        # user not supplied
        if user is None:
            embed_description = f"user must be supplied"

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        db_user = db_responder.read_user(discord_user_id=user.id)

        if db_user is None:
            embed_description = (
                f"could not find user with id {user.id} "
                f"in the database")

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                description=embed_description,
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        # Summary player count, total Active strike count, total active strike weight
        # User Strike active user strike count, active user strike weight
        # Player Strike active player strike count, active player strike weight
        if option == "active":
            embed_list = (
                await user_strike_responder.get_user_strike_message_active(
                    user=user,
                    inter=inter,
                    coc_client=self.coc_client))

        elif option == "all":
            embed_list = (
                await user_strike_responder.get_user_strike_message_all(
                    user=user,
                    inter=inter,
                    coc_client=self.coc_client))

        else:
            response = ResponderModel(
                field_dict_list=[{
                    'name': "incorrect option selected",
                    'value': "please select a different option"
                }])

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                title=response.title,
                description=response.description,
                bot_user_name=inter.me.display_name,
                field_list=response.field_dict_list,
                author=inter.author)

        await discord_responder.send_embed_list(inter, embed_list)

    @userstrike.sub_command()
    async def add(
        self,
        inter: ApplicationCommandInteraction,
        user: disnake.User = discord_utils.command_param_dict['required_user'],
        strike_name: str = commands.Param(
            name=discord_utils.command_param_dict['required_strike_model_name'].name,
            description=discord_utils.command_param_dict['required_strike_model_name'].description,
            default=discord_utils.command_param_dict['required_strike_model_name'].default,
            autocomplete=discord_utils.autocomp_strike_model_name_all),
        rollover_days: int = discord_utils.command_param_dict['rollover_days'],
        persistent: bool = discord_utils.command_param_dict['persistent']
    ):
        """
            user strike add command

            Parameters
            ----------
            `user` (User): user to add User Strike
            `rollover_days` (int, optional): amount of rollover days by default
                defaults None
        """

        response = user_strike_responder.add_user_strike(
            user=user,
            strike_name=strike_name,
            persistent=persistent,
            rollover_days=rollover_days,
            striker_user_id=inter.author.id)

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=response.title,
            description=response.description,
            bot_user_name=inter.me.display_name,
            field_list=response.field_dict_list,
            author=inter.author)

        await discord_responder.send_embed_list(inter, embed_list)

    @userstrike.sub_command()
    async def edit(
        self,
        inter: ApplicationCommandInteraction,
        user: disnake.User = discord_utils.command_param_dict['required_user'],
        user_strike_id: int = discord_utils.command_param_dict['user_strike_id']
    ):
        """
            user strike edit command

            Parameters
            ----------
            `user` (User): user to edit User Strike
            `user_strike_id` (int): ID of the User Strike to edit
        """

        response = (
            user_strike_responder.edit_user_strike_toggle_persistent(
                user=user,
                strike_id=user_strike_id))

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=response.title,
            description=response.description,
            bot_user_name=inter.me.display_name,
            field_list=response.field_dict_list,
            author=inter.author)

        await discord_responder.send_embed_list(inter, embed_list)

    @userstrike.sub_command()
    async def remove(
        self,
        inter: ApplicationCommandInteraction,
        user: disnake.User = discord_utils.command_param_dict['required_user'],
        user_strike_id: int = discord_utils.command_param_dict['user_strike_id'],
        removal_reason_name: str = commands.Param(
            name=discord_utils.command_param_dict['required_removal_reason_model_name'].name,
            description=discord_utils.command_param_dict['required_removal_reason_model_name'].description,
            default=discord_utils.command_param_dict['required_removal_reason_model_name'].default,
            autocomplete=discord_utils.autocomp_strike_model_name_all)
    ):
        """
            user strike remove command

            Parameters
            ----------
            `user` (User): user to remove User Strike
            `user_strike_id` (int): ID of the User Strike to remove
        """

        response = user_strike_responder.remove_user_strike(
            user=user,
            strike_id=user_strike_id,
            removal_reason_name=removal_reason_name)

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=response.title,
            description=response.description,
            bot_user_name=inter.me.display_name,
            field_list=response.field_dict_list,
            author=inter.author)

        await discord_responder.send_embed_list(inter, embed_list)
