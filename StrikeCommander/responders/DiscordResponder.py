from disnake import (
    ApplicationCommandInteraction,
    TextChannel,
    Member,
    Embed,
    Color,
    User
)
from coc import (
    Client as CocClient,
    WarRound,
    NotFound,
    Maintenance,
    PrivateWarLog,
    GatewayError,
    Clan,
    ClanWar,
    ClanWarLeagueGroup
)

from responders import (
    RazBotDB_Responder as db_responder,
    ClashResponder as clash_responder
)
import data.StrikeCommander_Client_Data as StrikeCommander_Client_Data
from data.th_urls import get_th_url
from disnake.utils import get


# DISCORD

def embed_message(
    discord_embed=Embed,
    color=Color(StrikeCommander_Client_Data.StrikeCommander_Data().embed_color),
    icon_url=None,
    title=None,
    description=None,
    bot_user_name=None,
    thumbnail=None,
    field_list=[],
    image_url=None,
    author: Member = None
):
    embed_list = []

    # no fields given
    if len(field_list) == 0:
        embed = initialize_embed(
            discord_embed=discord_embed,
            color=color,
            icon_url=icon_url,
            title=title,
            description=description,
            bot_user_name=bot_user_name,
            thumbnail=thumbnail,
            image_url=image_url,
            author=author
        )
        embed_list.append(embed)
        return embed_list

    while len(field_list) > 0:
        # initialize the current embed
        embed = initialize_embed(
            discord_embed=discord_embed,
            color=color,
            icon_url=icon_url,
            title=title,
            description=description,
            bot_user_name=bot_user_name,
            thumbnail=thumbnail,
            image_url=image_url,
            author=author
        )

        embed_str = ""
        # embed is be the disnake.Embed instance
        fields = [embed.title, embed.description,
                  embed.footer.text, embed.author.name]

        for item in fields:
            # if we str(disnake.Embed.Empty) we get 'Embed.Empty', when
            # we just want an empty string...
            embed_str += str(item) if str(item) != 'Embed.Empty' else ''

        while len(field_list) > 0:
            # use first field item since they will get deleted
            field = field_list[0]

            field_str = ""

            if str(field['name']) != 'Embed.Empty':
                field_str += str(field['name'])
            if str(field['value']) != 'Embed.Empty':
                field_str += str(field['value'])

            # embed data is greater than 6000
            if len(embed_str) + len(field_str) > 6000:
                # add the current embed to the list
                embed_list.append(embed)

                # get rid of the embed so it won't be added a second time
                embed = None

                # break the for and restart the while
                break

            if 'inline' in field:
                embed.add_field(
                    name=field['name'],
                    value=field['value'],
                    inline=field['inline']
                )
            else:
                embed.add_field(
                    name=field['name'],
                    value=field['value']
                )

            if str(field['name']) != 'Embed.Empty':
                embed_str += str(field['name'])
            if str(field['value']) != 'Embed.Empty':
                embed_str += str(field['value'])

            del field_list[0]

            # embed fields are greater than 25
            # discord doesn't allow more than 25 fields per embed
            if len(embed.fields) == 25:
                # add the current embed to the list
                embed_list.append(embed)

                # get rid of the embed so it won't be added a second time
                embed = None

                # break the for and restart the while
                break

        # dont add if exactly 25, already added
        # add the last embed to the list
        if embed is not None:
            if len(embed.fields) != 25 and len(embed.fields) > 0:
                embed_list.append(embed)

    return embed_list


def initialize_embed(
    discord_embed: Embed,
    color: Color,
    icon_url,
    title,
    description,
    bot_user_name,
    thumbnail,
    image_url,
    author: Member
):
    if title and description:
        embed = discord_embed(
            colour=color,
            title=title,
            description=description
        )
    elif title and not description:
        embed = discord_embed(
            colour=color,
            title=title,
        )
    elif not title and description:
        embed = discord_embed(
            colour=color,
            description=description
        )
    else:
        embed = discord_embed(
            colour=color
        )

    # icon url and bot username is not null
    if icon_url is not None and bot_user_name is not None:
        embed.set_author(
            icon_url=icon_url,
            name=f"{bot_user_name}"
        )

    # thumbnail is not null
    if thumbnail is not None:
        embed.set_thumbnail(
            url=thumbnail)

    # image url is not null
    if image_url is not None:
        embed.set_image(
            url=image_url)

    # author is not None
    if author is not None:
        # author avatar is None
        if author.avatar is None:
            embed.set_footer(
                text=author.display_name
            )
        # author avatar is not None
        else:
            embed.set_footer(
                text=author.display_name,
                icon_url=author.avatar.url
            )

    return embed


async def send_embed_list(
        inter: ApplicationCommandInteraction,
        embed_list: list = [],
        content: str = None,
        channel: TextChannel = None):
    # embed limit is 10
    # embed char limit is 6000
    # embed field limit is 25

    # prep a list of embeds to send
    # this will be lists of embeds in a list
    total_str = ""
    send_list = []
    add_list = []
    for embed in embed_list:
        embed_str = ""
        # embed is the disnake.Embed instance
        fields = [embed.title, embed.description,
                  embed.footer.text, embed.author.name]

        fields.extend([field.name for field in embed.fields])
        fields.extend([field.value for field in embed.fields])

        for item in fields:
            # if we str(disnake.Embed.Empty) we get 'Embed.Empty', when
            # we just want an empty string...
            embed_str += str(item) if str(item) != 'Embed.Empty' else ''

        # embeds will be higher than 6000 if added
        # embeds will have more than 10 embeds if added
        if len(total_str)+len(embed_str) > 6000 or len(add_list) == 10:
            # add the add_list to the send_list
            if len(add_list) != 0:
                send_list.append(add_list.copy())

                # clear the add_list
                add_list.clear()
            else:
                send_list.append([embed])

            total_str = ""

        add_list.append(embed)
        total_str += embed_str

        # if the embed is the last embed in the list
        # adding one to index for 0 index start
        if (embed_list.index(embed) + 1) == len(embed_list):
            send_list.append(add_list.copy())
            break

    # send all embeds
    for embeds in send_list:
        # respond to interaction if channel is not provided
        if channel is None:
            await inter.send(embeds=embeds)
            continue

        # try to send the embeds to specified channel
        try:
            await channel.send(embeds=embeds)

            # edit original message if the message was sent to channel
            embed_title = "message sent"
            embed_description = f"channel {channel.mention}"

            embed_list = embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                title=embed_title,
                description=embed_description,
                author=inter.author)

            await inter.edit_original_message(embeds=embed_list)
            continue

        # could not send embeds to specified channel
        # possible that bot does not have access for that
        except:
            embed_title = "message could not be sent"
            embed_description = (f"please ensure bot is in "
                                 f"channel {channel.mention}")

            embed_list = embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                title=embed_title,
                description=embed_description,
                author=inter.author)

            await inter.edit_original_message(embeds=embed_list)

            return False

    # end by sending content if provided
    if content is None:
        return True

    # respond to interaction if channel is not provided
    if channel is None:
        if len(content) >= 2000:
            while len(content) >= 2000:
                # send the first 2K characters of the string
                await inter.send(content=content[:2000])

                # remove the first 2K characters of the string
                content = content[2000:]

        await inter.send(content=content)
        return True

    # try to send the content to specified channel
    try:
        if len(content) >= 2000:
            while len(content) >= 2000:
                # send the first 2K characters of the string
                await channel.send(content=content[:2000])

                # remove the first 2K characters of the string
                content = content[2000:]

        await channel.send(content=content)

        # edit original message if the message was sent to channel
        embed_title = "message sent"
        embed_description = f"channel {channel.mention}"

        embed_list = embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            title=embed_title,
            description=embed_description,
            author=inter.author)

        await inter.edit_original_message(embeds=embed_list)
        return True

    # could not send content to specified channel
    # possible that bot does not have access for that
    except:
        embed_title = "message could not be sent"
        embed_description = (f"please ensure bot is in "
                             f"channel {channel.mention}")

        embed_list = embed_message(
            icon_url=inter.bot.user.avatar.url,
            bot_user_name=inter.me.display_name,
            title=embed_title,
            description=embed_description,
            author=inter.author)

        await inter.edit_original_message(embeds=embed_list)

        return False

# town hall urls


def get_town_hall_url(player):
    thumbnail_url = get_th_url(player.town_hall)
    if thumbnail_url is None:
        thumbnail_url = player.league.icon.small
    return thumbnail_url


# emojis

def get_emoji(coc_name, discord_emoji_list, client_emoji_list):
    client_emoji = get_base_emoji(
        coc_name, discord_emoji_list, client_emoji_list)

    # base emoji found
    if client_emoji is not None:
        return client_emoji

    client_emoji = get_th_emoji(
        coc_name, discord_emoji_list, client_emoji_list)

    # town hall emoji found
    if client_emoji is not None:
        return client_emoji

    client_emoji = get_war_opted_in_emoji(
        coc_name, discord_emoji_list, client_emoji_list)

    # war opted in emoji found
    if client_emoji is not None:
        return client_emoji

    client_emoji = get_clan_war_league_emoji(
        coc_name, discord_emoji_list, client_emoji_list)

    # clan war league emoji found
    if client_emoji is not None:
        return client_emoji

    return coc_name


def get_base_emoji(coc_name, discord_emoji_list, client_emoji_list):
    client_emoji = get(client_emoji_list, coc_name=coc_name)

    # emoji not found in client list
    if client_emoji is None:
        return None

    discord_emoji = get(
        discord_emoji_list,
        name=client_emoji.discord_name, id=client_emoji.discord_id)

    # emoji not found in discord list
    if discord_emoji is None:
        return None

    return (f"<:{discord_emoji.name}:{discord_emoji.id}>")


def get_th_emoji(coc_name, discord_emoji_list, client_emoji_list):
    client_emoji = get(client_emoji_list, coc_name=f"Town Hall {coc_name}")

    # emoji not found in client list
    if client_emoji is None:
        return None

    discord_emoji = get(
        discord_emoji_list,
        name=client_emoji.discord_name, id=client_emoji.discord_id)

    # emoji not found in discord list
    if discord_emoji is None:
        return None

    return (f"<:{discord_emoji.name}:{discord_emoji.id}>")


def get_war_opted_in_emoji(coc_name, discord_emoji_list, client_emoji_list):
    client_emoji = get(client_emoji_list, coc_name=f"war_opted_in={coc_name}")

    # emoji not found in client list
    if client_emoji is None:
        return None

    discord_emoji = get(
        discord_emoji_list,
        name=client_emoji.discord_name, id=client_emoji.discord_id)

    # emoji not found in discord list
    if discord_emoji is None:
        return None

    return (f"<:{discord_emoji.name}:{discord_emoji.id}>")


def get_clan_war_league_emoji(coc_name, discord_emoji_list, client_emoji_list):
    client_emoji = get(client_emoji_list, coc_name=f"Clan War {coc_name}")

    # emoji not found in client list
    if client_emoji is None:
        return None

    discord_emoji = get(
        discord_emoji_list,
        name=client_emoji.discord_name, id=client_emoji.discord_id)

    # emoji not found in discord list
    if discord_emoji is None:
        return None

    return (f"<:{discord_emoji.name}:{discord_emoji.id}>")


# user

def find_user_from_tag(player_obj, member_list):
    """
        finding a user from a requested player

        Args:
            player_obj (obj): clash player object
            member_list (list): list of members in guild

        Returns:
            list: field_dict_list
    """

    db_user_obj = db_responder.read_user_from_tag(player_obj.tag)
    # user with requested player tag not found
    if not db_user_obj:
        return {
            "name": f"{player_obj.name} {player_obj.tag}",
            "value": (f"linked user not found")
        }

    # find user in guild
    user_obj = get(member_list, id=db_user_obj.discord_id)

    # user not found in guild
    if not user_obj:
        return {
            "name": f"{player_obj.name} {player_obj.tag}",
            "value": (f"linked user not in server")
        }

    return {
        "name": f"{player_obj.name} {player_obj.tag}",
        "value": f"claimed by {user_obj.mention}"
    }


def user_player_ping(player, member_list):
    """
        turning a player into a user ping

        Args:
            player (obj): clash player object
                requires player.name and player.tag
            member_list (list): list of members in guild

        Returns:
            string: returns user ping if possible and player info
    """

    db_user = db_responder.read_user_from_tag(player.tag)

    if db_user is None:
        return f"{player.name} {player.tag}"

    user = get(member_list, id=db_user.discord_id)

    if user is None:
        return f"{player.name} {player.tag}"

    return f"{user.mention} ({player.name} {player.tag})"
