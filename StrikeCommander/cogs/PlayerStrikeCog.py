import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands
from responders.ResponderModel import ResponderModel
from coc.players import Player
from coc.clans import Clan
from coc.wars import ClanWar
from database.PlayerStrike import PlayerStrike
from responders import (
    DiscordResponder as discord_responder,
    ClashResponder as clash_responder,
    RazBotDB_Responder as db_responder,
    PlayerStrikeResponder as player_strike_responder,
    AuthResponder as auth_responder)
from utils import discord_utils
from disnake.utils import get
from errors.errors_db import (
    NotFoundError,
    ConflictError)


class PlayerStrike(commands.Cog):
    def __init__(self, bot, coc_client, client_data):
        self.bot = bot
        self.coc_client = coc_client
        self.client_data = client_data

    # player strike
    @commands.slash_command()
    async def playerstrike(self, inter):
        """
            parent for player strike commands
        """

        # defer for every player strike command
        await inter.response.defer()

    @playerstrike.sub_command()
    async def show(
        self,
        inter: ApplicationCommandInteraction,
        option: str = discord_utils.command_param_dict['playerstrike_show'],
        tag: str = discord_utils.command_param_dict['required_player_tag']
    ):
        """
            player strike show command
            Parameters
            ----------
            option (optional): options for player strike show command
            tag (optional): player tag to show strikes
        """

        # player tag not supplied
        if tag is None:
            embed_description = f"player tag must be supplied"

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        player: Player = await clash_responder.get_player(tag, self.coc_client)

        if player is None:
            embed_description = f"could not find player with tag {tag}"

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                description=embed_description,
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        db_player = db_responder.read_player_from_tag(player_tag=player.tag)

        if db_player is None:
            embed_description = (
                f"{player.name} {player.tag} "
                f"not found in database")

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                description=embed_description,
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        db_user = db_responder.read_user_from_tag(player_tag=player.tag)

        if db_user is None:
            embed_description = (
                f"could not find user with tag {player.tag} "
                f"in the database")

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                description=embed_description,
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        user = get(inter.guild.members, id=db_user.discord_id)

        # user not found in server
        if user is None:
            user_string = f"<@{db_user.discord_id}>"

        else:
            user_string = f"{user.mention}"

        embed_thumbnail = discord_responder.get_town_hall_url(player)

        if option == "overview":
            try:
                player_strike_list = (
                    player_strike_responder.find_player_strike_active(
                        player_tag=player.tag))

            except NotFoundError as arg:
                response = ResponderModel(
                    title=f"{player.name} {player.tag} Active Player Strikes",
                    description=(
                        f"Linked User: {user_string}\n"
                        f"Active Player Strike Count: **0**"))

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    title=response.title,
                    description=response.description,
                    bot_user_name=inter.me.display_name,
                    thumbnail=embed_thumbnail,
                    field_list=response.field_dict_list,
                    author=inter.author)

                await discord_responder.send_embed_list(inter, embed_list)

                return

            response = player_strike_responder.get_player_strike_overview(
                player=player,
                user_string=user_string,
                player_strike_list=player_strike_list)

        elif option == "active":
            try:
                player_strike_list = (
                    player_strike_responder.find_player_strike_active(
                        player_tag=player.tag))

            except NotFoundError as arg:
                response = ResponderModel(
                    title=f"{player.name} {player.tag} Active Player Strikes",
                    description=(
                        f"Linked User: {user_string}\n"
                        f"Active Player Strike Count: **0**"))

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    title=response.title,
                    description=response.description,
                    bot_user_name=inter.me.display_name,
                    thumbnail=embed_thumbnail,
                    field_list=response.field_dict_list,
                    author=inter.author)

                await discord_responder.send_embed_list(inter, embed_list)

                return

            response = player_strike_responder.get_player_strike_active(
                player=player,
                user_string=user_string,
                player_strike_list=player_strike_list)

        elif option == "all":
            try:
                player_strike_list = (
                    player_strike_responder.find_player_strike_all(
                        player_tag=player.tag))

            except NotFoundError as arg:
                response = ResponderModel(
                    title=f"{player.name} {player.tag} Player Strikes",
                    description=(
                        f"Linked User: {user_string}\n"
                        f"Player Strike Count: **0**"))

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    title=response.title,
                    description=response.description,
                    bot_user_name=inter.me.display_name,
                    thumbnail=embed_thumbnail,
                    field_list=response.field_dict_list,
                    author=inter.author)

                await discord_responder.send_embed_list(inter, embed_list)

                return

            response = player_strike_responder.get_player_strike_all(
                player=player,
                user_string=user_string,
                player_strike_list=player_strike_list)

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
            thumbnail=embed_thumbnail,
            field_list=response.field_dict_list,
            author=inter.author)

        await discord_responder.send_embed_list(
            inter,
            embed_list,
            content=response.content)

    @playerstrike.sub_command()
    async def clan(
        self,
        inter: ApplicationCommandInteraction,
        option: str = discord_utils.command_param_dict['playerstrike_show'],
        clan_role: disnake.Role = discord_utils.command_param_dict['clan_role'],
        tag: str = discord_utils.command_param_dict['tag']
    ):
        """
            player strike clan command
            Parameters
            ----------
            option (optional): options for player strike clan command
            clan_role (optional): clan role to use linked clan
            tag (optional): clan tag to show strikes for all players in the clan
        """

        # role not mentioned
        if clan_role is None:
            db_player_obj = db_responder.read_player_active(inter.author.id)

            verification_payload = await auth_responder.clan_verification(
                db_player_obj, inter.author, self.coc_client)
        # role has been mentioned
        else:
            verification_payload = await auth_responder.clan_role_verification(
                clan_role, self.coc_client)

        if not verification_payload['verified']:
            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                field_list=verification_payload['field_dict_list'],
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        clan: Clan = verification_payload['clan_obj']

        # clan tag selected
        if tag is not None:
            clan: Clan = await clash_responder.get_clan(tag, self.coc_client)

            if clan is None:
                embed_description = f"could not find clan with tag {tag}"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    bot_user_name=inter.me.display_name,
                    description=embed_description,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)

                return

        db_clan = db_responder.read_clan(
            discord_guild_id=inter.guild.id,
            clan_tag=clan.tag)

        if db_clan is None:
            embed_description = (
                f"{clan.name} {clan.tag} is not claimed in "
                f"{inter.guild.name}")

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                description=embed_description,
                author=inter.author)

            await discord_responder.send_embed_list(inter, embed_list)

            return

        clan_response = ResponderModel(
            title=f"{clan.name} {clan.tag}",
            description=f"Member Count: {clan.member_count}")

        field_dict_list = []
        message_content = ""

        async for player in clan.get_detailed_members():
            db_player = db_responder.read_player_from_tag(
                player_tag=player.tag)

            if db_player is None:
                field_dict_list.append({
                    'name': f"{player.name} {player.tag}",
                    'value': f"not found in database",
                    'inline': False})

                continue

            db_user = db_responder.read_user_from_tag(player_tag=player.tag)

            if db_user is None:
                field_dict_list.append({
                    'name': f"user with tag {player.tag}",
                    'value': f"not found in the database",
                    'inline': False})

                continue

            user = get(inter.guild.members, id=db_user.discord_id)

            # user not found in server
            if user is None:
                user_string = f"<@{db_user.discord_id}>"

            else:
                user_string = f"{user.mention}"

            if option == "overview":
                try:
                    player_strike_list = (
                        player_strike_responder.find_player_strike_active(
                            player_tag=player.tag))

                    response = player_strike_responder.get_player_strike_overview(
                        player=player,
                        user_string=user_string,
                        player_strike_list=player_strike_list)

                    if response.content is not None:
                        message_content += f"{response.content}\n\n"

                except NotFoundError:
                    response = ResponderModel(
                        title=f"{player.name} {player.tag} Active Player Strikes",
                        description=(
                            f"Linked User: {user_string}\n"
                            f"Active Player Strike Count: **0**"))

            elif option == "active":
                try:
                    player_strike_list = (
                        player_strike_responder.find_player_strike_active(
                            player_tag=player.tag))

                    response = player_strike_responder.get_player_strike_active(
                        player=player,
                        user_string=user_string,
                        player_strike_list=player_strike_list)

                    if response.content is not None:
                        message_content += f"{response.content}\n\n"

                except NotFoundError:
                    response = ResponderModel(
                        title=f"{player.name} {player.tag} Active Player Strikes",
                        description=(
                            f"Linked User: {user_string}\n"
                            f"Active Player Strike Count: **0**"))

            elif option == "all":
                try:
                    player_strike_list = (
                        player_strike_responder.find_player_strike_all(
                            player_tag=player.tag))

                    response = player_strike_responder.get_player_strike_all(
                        player=player,
                        user_string=user_string,
                        player_strike_list=player_strike_list)

                    if response.content is not None:
                        message_content += f"{response.content}\n\n"

                except NotFoundError:
                    response = ResponderModel(
                        title=f"{player.name} {player.tag} Player Strikes",
                        description=(
                            f"Linked User: {user_string}\n"
                            f"Player Strike Count: **0**"))

            else:
                response.field_dict_list = [{
                    'name': "incorrect option selected",
                    'value': "please select a different option"
                }]

            # response title or description were not passed
            if (response.title is not None
                    and response.description is not None):
                field_dict_list.append({
                    'name': response.title,
                    'value': response.description,
                    'inline': False
                })

        if message_content == "":
            message_content = None

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=clan_response.title,
            description=clan_response.description,
            bot_user_name=inter.me.display_name,
            thumbnail=clan.badge.small,
            field_list=field_dict_list,
            author=inter.author)

        await discord_responder.send_embed_list(
            inter,
            embed_list,
            content=message_content)

    @playerstrike.sub_command()
    async def add(
            self,
            inter: ApplicationCommandInteraction,
            tag: str = discord_utils.command_param_dict['required_player_tag'],
            strike_name: str = commands.Param(
                name=discord_utils.command_param_dict['required_strike_model_name'].name,
                description=discord_utils.command_param_dict['required_strike_model_name'].description,
                default=discord_utils.command_param_dict['required_strike_model_name'].default,
                autocomplete=discord_utils.autocomp_strike_model_name_active),
            rollover_days: int = discord_utils.command_param_dict['rollover_days'],
            persistent: bool = discord_utils.command_param_dict['persistent']):
        """
            player strike add command
            Parameters
            ----------
            `tag` (str): player tag to add Player Strike
            `rollover_days` (int, optional): amount of rollover days by default
                defaults None
        """

        # player tag not supplied
        if tag is None:
            embed_description = f"player tag must be supplied"

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        player_tag_list = tag.split()

        for tag in player_tag_list:
            player: Player = await clash_responder.get_player(tag, self.coc_client)

            if player is None:
                embed_description = f"could not find player with tag {tag}"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    bot_user_name=inter.me.display_name,
                    description=embed_description,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                continue

            db_player = db_responder.read_player_from_tag(
                player_tag=player.tag)

            if db_player is None:
                embed_description = (
                    f"{player.name} {player.tag} "
                    f"not found in database")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    bot_user_name=inter.me.display_name,
                    description=embed_description,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                continue

            db_user = db_responder.read_user_from_tag(player_tag=player.tag)

            if db_user is None:
                embed_description = (
                    f"could not find user with tag {player.tag} "
                    f"in the database")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    bot_user_name=inter.me.display_name,
                    description=embed_description,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                continue

            user = get(inter.guild.members, id=db_user.discord_id)

            # user not found in server
            if user is None:
                embed_description = (
                    f"could not find user <@{db_user.discord_id}> "
                    f"in the server")

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    bot_user_name=inter.me.display_name,
                    description=embed_description,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)
                continue

            else:
                user_string = f"{user.mention}"

            response = player_strike_responder.add_player_strike(
                player=player,
                user_string=user_string,
                strike_name=strike_name,
                persistent=persistent,
                rollover_days=rollover_days,
                striker_user_id=inter.author.id
            )

            embed_thumbnail = discord_responder.get_town_hall_url(player)

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                title=response.title,
                description=response.description,
                bot_user_name=inter.me.display_name,
                thumbnail=embed_thumbnail,
                field_list=response.field_dict_list,
                author=inter.author)

            await discord_responder.send_embed_list(
                inter, embed_list, content=response.content)

    @playerstrike.sub_command()
    async def war(
            self,
            inter: ApplicationCommandInteraction,
            option: str = discord_utils.command_param_dict['playerstrike_war'],
            clan_role: disnake.Role = discord_utils.command_param_dict['clan_role'],
            tag: str = discord_utils.command_param_dict['tag'],
            rollover_days: int = discord_utils.command_param_dict['rollover_days'],
            persistent: bool = discord_utils.command_param_dict['persistent'],
            war_selection: str = discord_utils.command_param_dict['war_selection']):
        """
            adds Player Strikes to those who missed war attacks 
            to an ended war
            Parameters
            ----------
            option (optional): options for player strike war command
            clan_role (optional): clan role to use linked clan
            tag (optional): clan tag to show strikes for all players in the clan
            war_selection (optional): cwl war selection
        """

        # role not mentioned
        if clan_role is None:
            db_player_obj = db_responder.read_player_active(inter.author.id)

            verification_payload = await auth_responder.war_verification(
                db_player_obj, war_selection, inter.author, self.coc_client)
        # role has been mentioned
        else:
            verification_payload = await auth_responder.clan_role_war_verification(
                clan_role, war_selection, self.coc_client)

        if not verification_payload['verified']:
            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                field_list=verification_payload['field_dict_list'],
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        war: ClanWar = verification_payload['war_obj']

        # clan tag selected
        if tag is not None:
            war: ClanWar = await clash_responder.get_war(tag, self.coc_client)

            if war is None:
                embed_description = f"could not find war with clan tag {tag}"

                embed_list = discord_responder.embed_message(
                    icon_url=inter.bot.user.avatar.url,
                    bot_user_name=inter.me.display_name,
                    description=embed_description,
                    author=inter.author
                )

                await discord_responder.send_embed_list(inter, embed_list)

                return

        db_clan = db_responder.read_clan(
            discord_guild_id=inter.guild.id,
            clan_tag=war.clan.tag)

        if db_clan is None:
            embed_description = (
                f"{war.clan.name} {war.clan.tag} is not claimed in "
                f"{inter.guild.name}")

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                description=embed_description,
                author=inter.author)

            await discord_responder.send_embed_list(inter, embed_list)

            return

        if war.state != "warEnded":
            embed_description = (
                f"{war.clan.name} {war.clan.tag} vs "
                f"{war.opponent.name} {war.opponent.tag} "
                f"has not ended")

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                description=embed_description,
                author=inter.author)

            await discord_responder.send_embed_list(inter, embed_list)

            return

        # setting strike model name to use
        if war.is_cwl:
            strike_model_name = "Missed CWL War Attack"

        else:
            strike_model_name = "Missed War Attack"

        field_dict_list = []
        message_content = "Users:\n\n"

        for player in war.clan.members:
            missing_attack_count = (
                war.attacks_per_member - len(player.attacks))

            # player has no missed attacks
            if missing_attack_count == 0:
                continue

            db_player = db_responder.read_player_from_tag(
                player_tag=player.tag)

            if db_player is None:
                field_dict_list.append({
                    'name': f"{player.name} {player.tag}",
                    'value': f"not found in database",
                    'inline': False})

                continue

            db_user = db_responder.read_user_from_tag(player_tag=player.tag)

            if db_user is None:
                field_dict_list.append({
                    'name': f"user with tag {player.tag}",
                    'value': f"not found in the database",
                    'inline': False})

                continue

            user = get(inter.guild.members, id=db_user.discord_id)

            # user not found in server
            if user is None:
                user_string = f"<@{db_user.discord_id}>"

            else:
                user_string = f"{user.mention}"

            # giving a Missed War Attack or Missed CWL War Attack strike
            # for each missed war attack
            if option == "each":
                for missed_attack in range(missing_attack_count):
                    response = (
                        player_strike_responder.add_player_strike(
                            player=player,
                            user_string=user_string,
                            strike_name=strike_model_name,
                            persistent=persistent,
                            rollover_days=rollover_days,
                            striker_user_id=inter.author.id))

            # giving a Missed War Attack or Missed CWL War Attack strike
            # for any missed war attack
            elif option == "any":
                response = (
                    player_strike_responder.add_player_strike(
                        player=player,
                        user_string=user_string,
                        strike_name=strike_model_name,
                        persistent=persistent,
                        rollover_days=rollover_days,
                        striker_user_id=inter.author.id))

            else:
                response.field_dict_list = [{
                    'name': "incorrect option selected",
                    'value': "please select a different option"
                }]

            # content not passed by responder
            if response.content is None:
                message_content += f"{user_string}\n\n"

            # content passed by responder
            else:
                message_content += f"{response.content}\n\n"

            if (
                response.title is not None
                and response.description is not None
            ):
                field_dict_list.append({
                    'name': response.title,
                    'value': response.description,
                    'inline': False
                })

        war_response = ResponderModel(
            title=f"{war.clan.name} {war.clan.tag}",
            description=f"Players Missing Attacks: {len(field_dict_list)}")

        # no fields meaning nobody missed an attack
        if len(field_dict_list) == 0:
            response = ResponderModel(
                title=f"{war.clan.name} {war.clan.tag}",
                description=(
                    f"all {len(war.clan.members)} {war.clan.name} "
                    f"war members attacked"))

            message_content = None

            field_dict_list.append({
                'name': response.title,
                'value': response.description,
                'inline': False
            })

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=war_response.title,
            description=war_response.description,
            bot_user_name=inter.me.display_name,
            thumbnail=war.clan.badge.small,
            field_list=field_dict_list,
            author=inter.author)

        await discord_responder.send_embed_list(
            inter, embed_list, content=message_content)

    @playerstrike.sub_command()
    async def edit(
            self,
            inter: ApplicationCommandInteraction,
            option: str = discord_utils.command_param_dict['playerstrike_edit'],
            tag: str = discord_utils.command_param_dict['required_player_tag'],
            player_strike_id: int = discord_utils.command_param_dict['player_strike_id'],
            rollover_days: int = discord_utils.command_param_dict['required_rollover_days']):
        """
            player strike edit command
            Parameters
            ----------
            `tag` (str): player tag to edit Player Strike
            `player_strike_id` (int): ID of the Player Strike to edit
            `rollover_days` (int): amount of rollover days
        """

        # player tag not supplied
        if tag is None:
            embed_description = f"player tag must be supplied"

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        player: Player = await clash_responder.get_player(tag, self.coc_client)

        if player is None:
            embed_description = f"could not find player with tag {tag}"

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                description=embed_description,
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        db_player = db_responder.read_player_from_tag(player_tag=player.tag)

        if db_player is None:
            embed_description = (
                f"{player.name} {player.tag} "
                f"not found in database")

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                description=embed_description,
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        db_user = db_responder.read_user_from_tag(player_tag=player.tag)

        if db_user is None:
            embed_description = (
                f"could not find user with tag {player.tag} "
                f"in the database")

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                description=embed_description,
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        user = get(inter.guild.members, id=db_user.discord_id)

        # user not found in server
        if user is None:
            embed_description = (
                f"could not find user with id <@{db_user.discord_id}> "
                f"in the server")

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                description=embed_description,
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        else:
            user_string = f"{user.mention}"

        if option == "toggle persistent":
            response = (
                player_strike_responder.edit_player_strike_toggle_persistent(
                    player=player,
                    strike_id=player_strike_id,
                    user_string=user_string))

        elif option == "rollover days":
            response = (
                player_strike_responder.edit_player_strike_rollover_days(
                    player=player,
                    strike_id=player_strike_id,
                    user_string=user_string,
                    rollover_days=rollover_days))

        else:
            response = ResponderModel(field_dict_list=[{
                'name': "incorrect option selected",
                'value': "please select a different option"
            }])

        embed_thumbnail = discord_responder.get_town_hall_url(player)

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=response.title,
            description=response.description,
            bot_user_name=inter.me.display_name,
            thumbnail=embed_thumbnail,
            field_list=response.field_dict_list,
            author=inter.author)

        await discord_responder.send_embed_list(
            inter, embed_list, content=response.content)

    @playerstrike.sub_command()
    async def remove(
        self,
        inter: ApplicationCommandInteraction,
        tag: str = discord_utils.command_param_dict['required_player_tag'],
        player_strike_id: int = discord_utils.command_param_dict['player_strike_id'],
        removal_reason_name: str = commands.Param(
            name=discord_utils.command_param_dict['required_removal_reason_model_name'].name,
            description=discord_utils.command_param_dict['required_removal_reason_model_name'].description,
            default=discord_utils.command_param_dict['required_removal_reason_model_name'].default,
            autocomplete=discord_utils.autocomp_removal_reason_model_name_active)):
        """
            player strike remove command
            Parameters
            ----------
            `tag` (str): player tag to remove Player Strike
            `player_strike_id` (int): ID of the Player Strike to remove
        """

        # player tag not supplied
        if tag is None:
            embed_description = f"player tag must be supplied"

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                description=embed_description,
                bot_user_name=inter.me.display_name,
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        player: Player = await clash_responder.get_player(tag, self.coc_client)

        if player is None:
            embed_description = f"could not find player with tag {tag}"

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                description=embed_description,
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        db_player = db_responder.read_player_from_tag(player_tag=player.tag)

        if db_player is None:
            embed_description = (
                f"{player.name} {player.tag} "
                f"not found in database")

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                description=embed_description,
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        db_user = db_responder.read_user_from_tag(player_tag=player.tag)

        if db_user is None:
            embed_description = (
                f"could not find user with tag {player.tag} "
                f"in the database")

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                description=embed_description,
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        user = get(inter.guild.members, id=db_user.discord_id)

        # user not found in server
        if user is None:
            embed_description = (
                f"could not find user with id <@{db_user.discord_id}> "
                f"in the server")

            embed_list = discord_responder.embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                description=embed_description,
                author=inter.author
            )

            await discord_responder.send_embed_list(inter, embed_list)
            return

        else:
            user_string = f"{user.mention}"

        response = player_strike_responder.remove_player_strike(
            player=player,
            strike_id=player_strike_id,
            removal_reason_name=removal_reason_name,
            user_string=user_string)

        embed_thumbnail = discord_responder.get_town_hall_url(player)

        embed_list = discord_responder.embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=response.title,
            description=response.description,
            bot_user_name=inter.me.display_name,
            thumbnail=embed_thumbnail,
            field_list=response.field_dict_list,
            author=inter.author)

        await discord_responder.send_embed_list(
            inter, embed_list, content=response.content)
