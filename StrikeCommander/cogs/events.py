import disnake
from disnake.ext import commands


class Events(commands.Cog):
    def __init__(self, bot, coc_client, client_data):
        self.bot = bot
        self.coc_client = coc_client
        self.client_data = client_data

    # client events
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Strike Commander is ready")

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter, exception):
        if isinstance(exception, commands.CommandNotFound):
            await inter.send(
                content=f"command '{inter.invoked_with}' could not be found")

        elif isinstance(exception, commands.MissingRequiredArgument):
            if hasattr(inter, "invoked_with"):
                await inter.send(
                    content=(f"command '{inter.invoked_with}' "
                             f"requires more information"))

            else:
                await inter.send(
                    content=f"command requires more information")

        elif hasattr(exception.original, "text"):
            await inter.send(
                content=(f"there was an error that I have not accounted for, "
                         f"please let {self.client_data.author} know.\n\n"
                         f"error text: `{exception.original.text}`"))

        elif hasattr(exception.original, "args"):
            await inter.send(
                content=(f"there was an error that I have not accounted for, "
                         f"please let {self.client_data.author} know.\n\n"
                         f"error text: `{exception.original.args[0]}`"))

        else:
            await inter.send(
                content=(f"there was an error that I have not accounted for, "
                         f"please let {self.client_data.author} know"))
