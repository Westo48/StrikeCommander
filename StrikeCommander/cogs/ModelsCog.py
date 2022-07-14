import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands
from responders import (
    DiscordResponder as discord_responder,
    StrikeModelResponder as strike_model_responder,
    RemovalReasonModelResponder as removal_reason_model_responder)
from utils import discord_utils


class Models(commands.Cog):
    def __init__(self, bot, coc_client, client_data):
        self.bot = bot
        self.coc_client = coc_client
        self.client_data = client_data

    # models
    @commands.slash_command()
    async def models(self, inter):
        """
            parent for models commands
        """

        # defer for every models command
        await inter.response.defer()

    @models.sub_command()
    async def strikemodel(
        self,
        inter: ApplicationCommandInteraction
    ):
        """
            strike model commands
            
            Parameters
            ----------
        """

        response = (
            strike_model_responder.get_strike_model_active())

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=response.title,
            description=response.description,
            bot_user_name=inter.me.display_name,
            field_list=response.field_dict_list,
            author=inter.author)

        await discord_responder.send_embed_list(inter, embed_list)

    @models.sub_command()
    async def removalreasonmodel(
        self,
        inter: ApplicationCommandInteraction
    ):
        """
            removal reason model commands
            
            Parameters
            ----------
        """

        response = (
            removal_reason_model_responder.get_removal_reason_model_active())

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=response.title,
            description=response.description,
            bot_user_name=inter.me.display_name,
            field_list=response.field_dict_list,
            author=inter.author)

        await discord_responder.send_embed_list(inter, embed_list)
