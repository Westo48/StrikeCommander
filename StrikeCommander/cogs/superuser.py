import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands
from responders.ResponderModel import ResponderModel
from responders import (
    DiscordResponder as discord_responder,
    RazBotDB_Responder as db_responder,
    StrikeModelResponder as strike_model_responder,
    RemovalReasonModelResponder as removal_reason_model_responder,
    UserStrikeResponder as user_strike_responder,
    PlayerStrikeResponder as player_strike_responder
)
from utils import discord_utils


class SuperUser(commands.Cog):
    def __init__(self, bot, coc_client, client_data):
        self.bot = bot
        self.coc_client = coc_client
        self.client_data = client_data

    # super user administration
    @commands.slash_command()
    async def superuser(self, inter):
        """
            parent for client super user commands
        """

        pass

    @superuser.sub_command()
    async def strikemodel(
        self,
        inter: ApplicationCommandInteraction,
        option: str = discord_utils.command_param_dict['superuser_strike_model'],
        strike_model_name: str = commands.Param(
            name=discord_utils.command_param_dict['strike_model_name'].name,
            description=discord_utils.command_param_dict['strike_model_name'].description,
            default=discord_utils.command_param_dict['strike_model_name'].default,
            autocomplete=discord_utils.autocomp_strike_model_name_all
        ),
        new_strike_name: str = discord_utils.command_param_dict['strike_model_new_strike_name'],
        description: str = discord_utils.command_param_dict['strike_model_description'],
        strike_weight: int = discord_utils.command_param_dict['strike_weight'],
        persistent: bool = discord_utils.command_param_dict['persistent'],
        rollover_days: int = discord_utils.command_param_dict['rollover_days']
    ):
        """
            *superuser strike model* 
            superuser strike model commands

            Parameters
            ----------
            option (optional): options for superuser strike model commands
        """

        # defer for every superuser player command
        await inter.response.defer()

        db_author = db_responder.read_user(inter.author.id)

        # author is not claimed
        if not db_author:
            embed_description = f"{inter.author.mention} is not claimed"

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        # author is not super user
        if not db_author.super_user:
            embed_description = f"{inter.author.mention} is not super user"

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        # initializing embed default values
        response = ResponderModel()

        # show all active strike models
        if option == "show active":
            response = (
                strike_model_responder.get_strike_model_active())

        elif option == "show all":
            response = (
                strike_model_responder.get_strike_model_all())

        elif option == "toggle active":
            response = (
                strike_model_responder.update_strike_model_toggle(
                    name=strike_model_name
                ))

        elif option == "edit":
            response = (
                strike_model_responder.update_strike_model(
                    name=strike_model_name,
                    description=description,
                    strike_weight=strike_weight,
                    persistent=persistent,
                    rollover_days=rollover_days
                ))

        elif option == "rename":
            response = (
                strike_model_responder.update_strike_model_name(
                    current_name=strike_model_name, new_name=new_strike_name
                ))

        elif option == "add":
            response = (
                strike_model_responder.add_strike_model(
                    name=new_strike_name,
                    description=description,
                    strike_weight=strike_weight,
                    persistent=persistent,
                    rollover_days=rollover_days
                ))

        elif option == "delete":
            response = (
                strike_model_responder.remove_strike_model(
                    name=strike_model_name
                ))

        else:
            response.field_dict_list = [{
                'name': "incorrect option selected",
                'value': "please select a different option"
            }]

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=response.title,
            description=response.description,
            bot_user_name=inter.me.display_name,
            field_list=response.field_dict_list,
            author=inter.author)

        await discord_responder.send_embed_list(inter, embed_list)

    @superuser.sub_command()
    async def removalreasonmodel(
        self,
        inter: ApplicationCommandInteraction,
        option: str = (
            discord_utils.command_param_dict['superuser_removal_reason_model']),
        removal_reason_model_name: str = commands.Param(
            name=discord_utils.command_param_dict['removal_reason_model_name'].name,
            description=discord_utils.command_param_dict[
                'removal_reason_model_name'].description,
            default=discord_utils.command_param_dict[
                'removal_reason_model_name'].default,
            autocomplete=discord_utils.autocomp_removal_reason_model_name_all
        ),
        new_removal_reason_name: str = (
            discord_utils.command_param_dict['removal_reason_model_new_removal_reason_name']),
        description: str = (
            discord_utils.command_param_dict['removal_reason_model_description'])
    ):
        """
            *superuser removal reason model* 
            superuser removal reason model commands

            Parameters
            ----------
            option (optional): options for superuser removal reason model commands
        """

        # defer for every superuser player command
        await inter.response.defer()

        db_author = db_responder.read_user(inter.author.id)

        # author is not claimed
        if not db_author:
            embed_description = f"{inter.author.mention} is not claimed"

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        # author is not super user
        if not db_author.super_user:
            embed_description = f"{inter.author.mention} is not super user"

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        # initializing embed default values
        response = ResponderModel()

        # show all active removal reason models
        if option == "show active":
            response = (
                removal_reason_model_responder.get_removal_reason_model_active())

        elif option == "show all":
            response = (
                removal_reason_model_responder.get_removal_reason_model_all())

        elif option == "toggle active":
            response = (
                removal_reason_model_responder.update_removal_reason_model_toggle(
                    name=removal_reason_model_name
                ))

        elif option == "edit":
            response = (
                removal_reason_model_responder.update_removal_reason_model(
                    name=removal_reason_model_name,
                    description=description
                ))

        elif option == "rename":
            response = (
                removal_reason_model_responder.update_removal_reason_model_name(
                    current_name=removal_reason_model_name,
                    new_name=new_removal_reason_name
                ))

        elif option == "add":
            response = (
                removal_reason_model_responder.add_removal_reason_model(
                    name=new_removal_reason_name,
                    description=description
                ))

        elif option == "delete":
            response = (
                removal_reason_model_responder.remove_removal_reason_model(
                    name=removal_reason_model_name
                ))

        else:
            response.field_dict_list = [{
                'name': "incorrect option selected",
                'value': "please select a different option"
            }]

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=response.title,
            description=response.description,
            bot_user_name=inter.me.display_name,
            field_list=response.field_dict_list,
            author=inter.author)

        await discord_responder.send_embed_list(inter, embed_list)

    @superuser.sub_command()
    async def userstrike(
        self,
        inter: ApplicationCommandInteraction,
        option: str = (
            discord_utils.command_param_dict['superuser_strike']),
        strike_id: int = discord_utils.command_param_dict['user_strike_id']
    ):
        """
            *superuser User Strike* 
            superuser User Strike commands

            Parameters
            ----------
            option (optional): options for superuser User Strike commands
        """

        # defer for every superuser player command
        await inter.response.defer()

        db_author = db_responder.read_user(inter.author.id)

        # author is not claimed
        if not db_author:
            embed_description = f"{inter.author.mention} is not claimed"

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        # author is not super user
        if not db_author.super_user:
            embed_description = f"{inter.author.mention} is not super user"

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        # initializing embed default values
        response = ResponderModel()

        if option == "delete":
            response = (
                user_strike_responder.delete_user_strike_from_id(
                    strike_id=strike_id))

        else:
            response.field_dict_list = [{
                'name': "incorrect option selected",
                'value': "please select a different option"
            }]

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=response.title,
            description=response.description,
            bot_user_name=inter.me.display_name,
            field_list=response.field_dict_list,
            author=inter.author)

        await discord_responder.send_embed_list(inter, embed_list)

    @superuser.sub_command()
    async def playerstrike(
        self,
        inter: ApplicationCommandInteraction,
        option: str = (
            discord_utils.command_param_dict['superuser_strike']),
        strike_id: int = discord_utils.command_param_dict['player_strike_id']
    ):
        """
            *superuser User Strike* 
            superuser User Strike commands

            Parameters
            ----------
            option (optional): options for superuser User Strike commands
        """

        # defer for every superuser player command
        await inter.response.defer()

        db_author = db_responder.read_user(inter.author.id)

        # author is not claimed
        if not db_author:
            embed_description = f"{inter.author.mention} is not claimed"

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        # author is not super user
        if not db_author.super_user:
            embed_description = f"{inter.author.mention} is not super user"

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        # initializing embed default values
        response = ResponderModel()

        if option == "delete":
            response = (
                player_strike_responder.delete_player_strike_from_id(
                    strike_id=strike_id))

        else:
            response.field_dict_list = [{
                'name': "incorrect option selected",
                'value': "please select a different option"
            }]

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=response.title,
            description=response.description,
            bot_user_name=inter.me.display_name,
            field_list=response.field_dict_list,
            author=inter.author)

        await discord_responder.send_embed_list(inter, embed_list)
