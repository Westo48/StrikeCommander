import data.StrikeCommander_Data as StrikeCommander_Data

from responders.AuthResponder import player_verification

from disnake.utils import get


def get_client_discord_id():
    """
        returns StrikeCommander_Data client discord id
    """

    return StrikeCommander_Data.StrikeCommander_Data().discord_id


def get_client_token():
    """
        returns StrikeCommander_Data client token
    """

    return StrikeCommander_Data.StrikeCommander_Data().token


def get_client_test_guilds():
    """
        returns StrikeCommander_Data client test guilds
    """

    test_guilds = StrikeCommander_Data.StrikeCommander_Data().test_guilds

    if len(test_guilds) > 0:
        return test_guilds

    else:
        return None


def get_client_email():
    """
        returns StrikeCommander_Data client coc email
    """

    return StrikeCommander_Data.StrikeCommander_Data().coc_dev_email


def get_client_password():
    """
        returns StrikeCommander_Data client coc password
    """

    return StrikeCommander_Data.StrikeCommander_Data().coc_dev_password


def client_info(client, client_data):
    field_dict_list = []

    field_dict_list.append({
        'name': "**Client Info**",
        'value': "_ _",
        'inline': False
    })

    field_dict_list.append({
        'name': "author",
        'value': client_data.author
    })

    field_dict_list.append({
        'name': "description",
        'value': client_data.description
    })

    field_dict_list.append({
        'name': "server count",
        'value': f"{len(client.guilds)}"
    })

    field_dict_list.append({
        'name': "version",
        'value': client_data.version
    })

    return field_dict_list


def client_guild_info(guild, db_guild):
    field_dict_list = []

    field_dict_list.append({
        'name': "**Client Server Info**",
        'value': "_ _",
        'inline': False
    })

    field_dict_list.append({
        'name': f"{guild.name} owner",
        'value': f"{guild.owner.mention}"
    })

    field_dict_list.append({
        'name': f"{guild.name} member count",
        'value': f"{len(guild.members)}"
    })

    if db_guild is None:
        field_dict_list.append({
            'name': f"{guild.name} not claimed",
            'value': f"please claim the server using `client guild claim`"
        })
        return field_dict_list

    db_guild_admin = get(guild.members, id=db_guild.admin_user_id)

    if db_guild_admin is None:
        guild_admin_value = f"id: {db_guild.admin_user_id}"
    else:
        guild_admin_value = f"{db_guild_admin.mention}"

    field_dict_list.append({
        'name': "ClashCommander server admin",
        'value': guild_admin_value
    })

    return field_dict_list


async def client_player_info(author, db_players, coc_client):
    field_dict_list = []

    field_dict_list.append({
        'name': "**Client Player Info**",
        'value': "_ _",
        'inline': False
    })

    # linked players count
    field_dict_list.append({
        'name': f"{author.display_name} players",
        'value': f"{len(db_players)}"
    })

    for db_player in db_players:
        player_verification_payload = await player_verification(
            db_player, author, coc_client)

        if not player_verification_payload['verified']:
            field_dict_list.extend(
                player_verification_payload['field_dict_list'])
            continue

        player = player_verification_payload['player_obj']

        field_dict_list.append({
            'name': player.name,
            'value': player.tag
        })

    return field_dict_list
