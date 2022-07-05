# Strike Commander

Discord bot for Clash of Clans striking users and players written in Python

# Table of Contents

- [Introduction](#introduction)
- [Setup](#setup)
  - [Setup Summary](#setup-summary)
- [Usage](#usage)
- [Command List](#command-list)
  - [Help](#command-list-help)
  - [Models](#command-list-models)
  - [User](#command-list-user)
  - [User Strike](#command-list-user-strike)
  - [Player Strike](#command-list-player-strike)
- [Contributing](#contributing)
- [Requirements](#requirements)
- [Links and Contact](#links-and-contact)

# <a id="introduction"></a>Introduction

Strike Commander is a discord bot written in Python that is a sister bot to [ClashCommander](https://github.com/Westo48/clash-discord). This bot focuses on striking users and players for various reasons including, but not limited to, missing attacks, being toxic towards other players, and not following directions. If you like ClashCommander and want to take it one step further, then Strike Commander is the bot for you!

# <a id="setup"></a>Setup

Getting Strike Commander set up in your discord server is much simpler than ClashCommander.

1. set up ClashCommander

   - [ClashCommander setup](https://github.com/Westo48/clash-discord/blob/master/README.md)
   
2. invite Strike Commander

   - [invite link]()
   
3. restrict commands in discord

   - **important** this step restricts users from giving and removing strikes
   - go into your discord's server settings *on your desktop (currently does NOT work on mobile)*, select `integrations` and disallow `@everyone` access for the commands `UserStrike` and `PlayerStrike`, then allow access for specific users or roles as desired
   - ClashCommander authenticates based on admin status in the database and leadership status in clans, Strike Commander does **NOT** authenticate for commands, so this must be done on the server's end. That being said this is a step that should take less than 5 minutes and, once set, shouldn't require any additional setup!

4. Use Strike Commander, you are set up!

# <a id="setup-summary"></a>Setup Summary

- set up ClashCommander
- invite Strike Commander
- restrict commands in discord

# <a id="usage"></a>Usage

Strike Commander is largely **command** focused, meaning it doesn't do anything that it is not told to do.

Once setup is complete you will be able to interact with Strike Commander with slash commands as desired.

# <a id="command-list"></a>Command List

- ## <a id="command-list-help"></a>Help

  - help
    - displays relevant help-text regarding what commands can be run
    - react to the help message to parse through command groups

- ## <a id="command-list-models"></a>Models

  - models strikemodel

    - lists all Strike Models

  - models removalreasonmodel

    - lists all Removal Reason Models

- ## <a id="command-list-user"></a>User

  - user show

    - _user show options_
      - options for `user show` command
      - `active` _default_ - shows active user and player strikes
      - `all` - shows all user and player strikes

- ## <a id="command-list-user-strike"></a>User Strike

  - ### _userstrike parameters_

    - parameters for userstrike commands
    - `user` - *required* discord user to specify for the command

  - userstrike show

    - show specified user's User Strikes and Player Strikes
    - _userstrike show options_
      - options for `userstrike show` command
      - `active` _default_ - shows active user and player strikes
      - `all` - shows all user and player strikes

  - userstrike add

    - adds a User Strike to the specified user
	- _userstrike add parameters_
      - `strike_model_name` - *required* name of strike model to give the specified user
      - `rollover_days` -  amount of days strike will rollover
	    - this will override the default rollover days set by the model
		- if no `rollover_days` value is set, then it will default to the rollover days set by the model
      - `persistent` -  whether or not the strike will be persistent (if it is persistent, then it will not automatically rollover)
	    - this will override the default persistent value set by the model
		- if no `persistent` value is set, then it will default to the persistent value set by the model

  - userstrike edit

    - toggles the `persistent` value of the given strike for the given user
	- _userstrike edit parameters_
      - `user_strike_id` - *required* ID of the User Strike

  - userstrike remove

    - removes the given User Strike
	- _userstrike remove parameters_
      - `user_strike_id` - *required* ID of the User Strike
      - `removal_reason_model_name` - *required* name of removal reason model to give to remove the specified User Strike

- ## <a id="command-list-player-strike"></a>Player Strike

  - playerstrike show

    - show specified player's Player Strikes
	- _playerstrike show parameters_
      - `player_tag` - *required* player tag to specify for the command
    - _playerstrike show options_
      - options for `playerstrike show` command
      - `active` _default_ - shows active player strikes
      - `all` - shows all player strikes

  - playerstrike clan

    - show specified clan's Player Strikes for each clan member
	- _playerstrike clan parameters_
      - `clan_role` - mention a role linked to a clan to get that clan's information
        - _if no clan role is specified, then the user's active player's clan will be used_
      - `tag` - specify a clan's tag for that clan's information
        - _if no tag is specified, then the user's active player's clan will be used_
    - _playerstrike clan options_
      - options for `playerstrike clan` command
      - `active` _default_ - shows active player strikes
      - `all` - shows all player strikes

  - playerstrike add

    - adds a Player Strike to the specified player
	- _playerstrike add parameters_
      - `player_tag` - *required* player tag to specify for the command
      - `strike_model_name` - *required* name of strike model to give the specified player
      - `rollover_days` -  amount of days strike will rollover
	    - this will override the default rollover days set by the model
		- if no `rollover_days` value is set, then it will default to the rollover days set by the model
      - `persistent` -  whether or not the strike will be persistent (if it is persistent, then it will not automatically rollover)
	    - this will override the default persistent value set by the model
		- if no `persistent` value is set, then it will default to the persistent value set by the model

  - playerstrike war

    - adds a Player Strike for each missed attack of an ended war
	- _playerstrike war parameters_
      - `clan_role` - mention a role linked to a clan to get that clan's information
        - _if no clan role is specified, then the user's active player's clan will be used_
      - `tag` - specify a clan's tag for that clan's information
        - _if no tag is specified, then the user's active player's clan will be used_
      - `rollover_days` -  amount of days strike will rollover
	    - this will override the default rollover days set by the model
		- if no `rollover_days` value is set, then it will default to the rollover days set by the model
      - `persistent` -  whether or not the strike will be persistent (if it is persistent, then it will not automatically rollover)
	    - this will override the default persistent value set by the model
		- if no `persistent` value is set, then it will default to the persistent value set by the model
    - _playerstrike war options_
      - options for `playerstrike war` command
      - `each` _default_ - gives a Player Strike for each missed attack
      - `any` - gives a Player Strike for any missed attack
	    - _will give one strike regardless of the amount of attacks missed_

  - playerstrike edit

    - toggles the `persistent` value of the given strike for the given player
	- _playerstrike edit parameters_
      - `player_tag` - *required* player tag to specify for the command
      - `player_strike_id` - *required* ID of the Player Strike

  - playerstrike remove

    - removes the given Player Strike
	- _playerstrike remove parameters_
      - `player_tag` - *required* player tag to specify for the command
      - `player_strike_id` - *required* ID of the Player Strike
      - `removal_reason_model_name` - *required* name of removal reason model to give to remove the specified Player Strike

# <a id="contributing"></a>Contributing

If you would _like_ to contribute to this project please message me on discord _or_ email me. I currently do not have any contribution instruction and will figure that out when the time comes if someone would like to.

# <a id="requirements"></a>Requirements

There aren't many required packages, but here are the few that are required and the versions I am using.

- [disnake](https://github.com/DisnakeDev/disnake)
  - 2.5.1
- [coc.py](https://github.com/mathsman5133/coc.py)
  - 2.0.1
- PyMySQL
  - 1.0.2
- requests
  - 2.27.1

# <a id="links-and-contact"></a>Links and Contact

[Official ClashCommander Server](https://discord.gg/3jcfaa5NYk)

Email: ClashCommander218@gmail.com
