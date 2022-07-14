from disnake import (
    ApplicationCommandInteraction as Interaction
)
from disnake.ui.view import View
from views.help_view import (
    HelpMainView as main_view,
)
from buttons.help_categories import (
    HelpSuperUserBtn as superuser_btn,
    HelpModelsBtn as models_btn,
    HelpUserBtn as user_btn,
    HelpUserStrikeBtn as user_strike_btn,
    HelpPlayerStrikeBtn as player_strike_btn)
from data import StrikeCommander_Client_Data as Client_Data
from responders import (
    RazBotDB_Responder as db_responder)


def help_main(
        bot,
        inter: Interaction,
        client_data: Client_Data.StrikeCommander_Data):

    help_dict = {
        'field_dict_list': [],
        'view': View
    }

    button_list = []

    # get the db user
    db_user = db_responder.read_user(inter.author.id)

    # return
    if db_user is None:
        help_dict['field_dict_list'].append({
            'name': f"User not claimed",
            'value': (
                f"{inter.author.mention}, claim a user to use "
                f"{inter.me.display_name} help menu")
        })

        help_dict['view'] = main_view(
            buttons=button_list)

        return help_dict

    # get the db guild
    db_guild = db_responder.read_guild(inter.guild.id)

    for category in client_data.bot_categories:
        # super user check
        if category.brief == "superuser":
            if db_user.super_user:
                help_dict['field_dict_list'].append({
                    'name': f"{category.emoji} {category.name}",
                    'value': category.description
                })

                button_list.append(
                    superuser_btn(bot=bot, client_data=client_data))

            continue

        elif category.brief == "models":
            help_dict['field_dict_list'].append({
                'name': f"{category.emoji} {category.name}",
                'value': category.description
            })

            button_list.append(
                models_btn(bot=bot, client_data=client_data))

            continue

        elif category.brief == "user":
            help_dict['field_dict_list'].append({
                'name': f"{category.emoji} {category.name}",
                'value': category.description
            })

            button_list.append(
                user_btn(bot=bot, client_data=client_data))

            continue

        elif category.brief == "userstrike":
            help_dict['field_dict_list'].append({
                'name': f"{category.emoji} {category.name}",
                'value': category.description
            })

            button_list.append(
                user_strike_btn(bot=bot, client_data=client_data))

            continue

        elif category.brief == "playerstrike":
            help_dict['field_dict_list'].append({
                'name': f"{category.emoji} {category.name}",
                'value': category.description
            })

            button_list.append(
                player_strike_btn(bot=bot, client_data=client_data))

            continue

    help_dict['view'] = main_view(
        buttons=button_list)

    return help_dict
