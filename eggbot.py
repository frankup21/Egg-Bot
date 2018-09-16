import discord
import asyncio
import platform
import requests
import json
from datetime import datetime
from discord.ext.commands import Bot
from discord.ext import commands

async def run():
    bot = Bot()
    try:
        await bot.start("")
    except KeyboardInterrupt:
        await bot.logout()

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="e!")
        self.remove_command("help")
        self.add_command(self.top)
        self.add_command(self.help)
        self.add_command(self.addcolor)
        self.add_command(self.removecolor)
        self.add_command(self.colors)
        self.add_command(self.verify)
        self.add_command(self.fullyverify)
        self.add_command(self.ask)

        self.role_ids = [
            "476625775718694922", #Red
            "479391249170956309", #Mint
            "476914831744827392", #Blue
            "475637467370881027", #Pink
            "480098398461231104", #Orchid
            "480099403416469525", #Purple
            "480100032373325824", #Yellow
            "480100441162645525", #White
            "480101544981692442", #Orange
            "480102271133417504", #Lime Green
            "480103088145825793", #Green
            "480103452408807424", #Black
            "480104711748583455", #Cyan
            "480105715877543936", #Beige
            "480106440460337155", #Sky Blue
            "480106946427355136", #Coral
            "480107033203441675", #Teal
            "480107825050288131", #Violet
            "480108741186813952", #Magenta
            "480108169977266178", #Gold
            "480109574813253683", #Turquoise
            "480108741019172864", #Silver
            "480126003704889349", #Crimson
            "480127634961858570", #Eggshell
            "480189683842809865", #Royal Blue
            "480100032427589632", #Navy
            "479889427074908161", #Salmon
            "480106945911586818", #Sea Green
            "480238460523773953", #Dark Red
            "480239814768197643", #Slate
            "480124829085859840" #Dark Green
        ]
        self.role_names = [
            "Red", "Mint", "Blue", "Pink", "Orchid", "Purple", "Yellow", "White", "Orange", "Lime Green",
            "Green", "Black", "Cyan", "Beige", "Sky Blue", "Coral", "Teal", "Violet", "Magenta", "Gold",
            "Turquoise", "Silver", "Crimson", "Eggshell", "Royal Blue", "Navy", "Salmon", "Sea Green", "Dark Red", "Slate",
            "Dark Green"]

        self.verified_ids = ["473649456043261953", "473649831328481282"]

    async def on_command_error(self, error, ctx):
        if isinstance(error, commands.CommandOnCooldown):
            await self.send_message(ctx.message.channel, ":no_entry_sign: Please wait an hour between posting new questions.")
        elif isinstance(error, commands.BadArgument):
            ctx.command.reset_cooldown(ctx)

    async def on_ready(self):
        await self.change_presence(game=discord.Game(name=("e!help")))

        print('Logged in as '+self.user.name+' (ID:'+self.user.id+') | Connected to '+str(len(self.servers))+' servers | Connected to '+str(len(set(self.get_all_members())))+' users')
        print('--------')
        print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
        print('--------')
        print('Use this link to invite {}:'.format(self.user.name))
        print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(self.user.id))
        print('--------')

    @commands.cooldown(1, 3600, commands.BucketType.user)
    @commands.command(pass_context=True)
    async def ask(self, ctx, *, input: str):
        if ',' not in input:
            await self.say(":no_entry_sign: Your command is not in proper format. Make sure your options are comma separated: `e!ask option 1, option 2`")
            raise commands.BadArgument()

        tokens = input.split(",")
        if len(tokens) > 2:
            await self.say(":no_entry_sign: This command only allows two options.")
            raise commands.BadArgument()

        option1 = tokens[0]
        option2 = tokens[1]

        if option1 is None or option2 is None or bool(option1.strip()) is False or bool(option2.strip()) is False:
            await self.say(":no_entry_sign: You must supply two options!")
            raise commands.BadArgument()

        msg = "🥚 " + option1 + "\n" + "or \n🍆 " + option2
        embed = discord.Embed(title="Would you rather...", description=msg, colour=0xf7dece)
        embed.set_author(icon_url=ctx.message.author.avatar_url, name=ctx.message.author.display_name + " asks,")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/372188609425702915/489585830009110549/476089787569405967.png")
        message = await self.say(embed=embed)
        await self.add_reaction(message, "🥚")
        await self.add_reaction(message, "🍆")

    @commands.command(pass_context=True)
    async def verify(self, ctx, member: discord.Member=None):
        mod_role = discord.utils.get(ctx.message.server.roles, name="Mod")
        if mod_role not in ctx.message.author.roles:
            await self.send_message(ctx.message.channel, ":no_entry_sign: You do not have permission to use this command.")
            return
        elif member is None:
            await self.send_message(ctx.message.channel, ":no_entry_sign: Please tag the user you want to verify.")
            return
        else:
            for r in member.roles:
                if r.id in self.verified_ids:
                    await self.send_message(ctx.message.channel, ":no_entry_sign: That user is already verified!")
                    return
            role = discord.utils.get(ctx.message.server.roles, name="Verified Nerd🤓")
            await self.add_roles(member, role)
            await self.send_message(ctx.message.channel, ":white_check_mark: User verified!")

    @commands.command(pass_context=True)
    async def fullyverify(self, ctx, member: discord.Member=None):
        mod_role = discord.utils.get(ctx.message.server.roles, name="Mod")
        if mod_role not in ctx.message.author.roles:
            await self.send_message(ctx.message.channel, ":no_entry_sign: You do not have permission to use this command.")
            return
        elif member is None:
            await self.send_message(ctx.message.channel, ":no_entry_sign: Please tag the user you want to verify.")
            return
        else:
            for r in member.roles:
                if r.id == "473649831328481282":
                    await self.send_message(ctx.message.channel, ":no_entry_sign: That user is already fully verified!")
                    return
            try:
                role = discord.utils.get(ctx.message.server.roles, name="Verified Nerd🤓")
                member.roles.remove(role)
            except:
                pass
            role = discord.utils.get(ctx.message.server.roles, name="Fully Verified Nerd🤓")
            member.roles.append(role)
            await self.replace_roles(member, *member.roles)
            await self.send_message(ctx.message.channel, ":white_check_mark: User fully verified!")

    @commands.command(pass_context=True)
    async def colors(self, ctx):
        with open('colors.png', 'rb') as f:
            await self.send_file(ctx.message.channel, f)

    @commands.command(pass_context=True)
    async def addcolor(self, ctx, *, color: str=None):
        if color is None:
            await self.send_message(ctx.message.channel, ":no_entry_sign: Try supplying a color.")
            with open('colors.png', 'rb') as f:
                await self.send_file(ctx.message.channel, f)
            return
        entered_color = color.title()
        role = discord.utils.get(ctx.message.server.roles, name=entered_color)

        for r in ctx.message.author.roles:
            if r.id in self.role_ids:
                await self.send_message(ctx.message.channel, ":no_entry_sign: Use `e!removecolor` before changing your color!")
                return
        if role is None or role.name not in self.role_names:
            await self.send_message(ctx.message.channel, ":no_entry_sign: That color was not found. Please refer to the color listing below.")
            with open('colors.png', 'rb') as f:
                await self.send_file(ctx.message.channel, f)
            return
        elif role in ctx.message.author.roles:
            await self.send_message(ctx.message.channel, ":no_entry_sign: You already have that color.")
            return
        else:
            try:
                await self.add_roles(ctx.message.author, role)
                await self.send_message(ctx.message.channel, ":white_check_mark: Color added!")
            except discord.Forbidden:
                await self.send_message(ctx.message.channel, "I don't have perms to add roles.")

    @commands.command(pass_context=True)
    async def removecolor(self, ctx):
        for r in ctx.message.author.roles:
            if r.id in self.role_ids:
                try:
                    await self.remove_roles(ctx.message.author, r)
                    await self.send_message(ctx.message.channel, ":white_check_mark: Color removed!")
                except discord.Forbidden:
                    await self.send_message(ctx.message.channel, "I don't have perms to add roles.")
                return

    def find_longest_name(self, data):
        longest = 0
        for player in data:
            if len(player['username']) > longest:
                longest = len(player['username'])
        return longest + 2

    @commands.command(pass_context=True)
    async def top(self, ctx, param: int=0):
        if param < 0:
            await self.send_message(ctx.message.channel, ":no_entry_sign: That page does not exist!")
            return

        apipage = "0"
        if param != 0:
            apipage = str(param - 1)

        session_requests = requests.session()
        url = "https://mee6.xyz/api/plugins/levels/leaderboard/455399951258746900?limit=10&page={}".format(apipage)
        page = session_requests.get(url)
        data = page.json()

        if len(data['players']) == 0:
            await self.send_message(ctx.message.channel, ":no_entry_sign: That page does not exist!")
            return

        longest_name = self.find_longest_name(data['players'])
        message = "Server Leaderboard: Page {}\n\n{:<6}{:<{namelength}}{:<7}{:<6}\n".format(int(apipage) + 1, "Rank", "Name", "Level", "XP", namelength=longest_name) + ("-" * (19 + longest_name)) + "\n"
        count = 1 + (10 * int(apipage))
        for player in data['players']:
            message = message + "{:<6}{:<{namelength}}{:<7}{:<6}\n".format(count, player['username'], player['level'], player['xp'], namelength=longest_name) + ("-" * (19 + longest_name)) + "\n"
            count += 1
        nextpage = int(apipage) + 2
        message = message + "\nType e!top {} to see the next page.".format(nextpage)
        await self.send_message(ctx.message.channel, "```python\n"+message+"```")

    @commands.command(pass_context=True)
    async def help(self, ctx):
        message = """Hello! I am Egg Bot. I am a custom bot written specifically for the Lonely Nerds server!

        Prefix: **e!**
        Example: **e!top**

        Commands:
        `e!top`
        Displays the MEE6 server leaderboard.

        `e!addcolor color`
        Assigns a color role. Refer to #information for a list of colors to choose from.

        `e!removecolor`
        Clears your color role.

        `e!colors`
        View a list of availible color roles.

        __Moderator Commands__
        `e!verify @user`
        Verifies a user.

        `e!fullyverify @user`
        Fully verifies a user."""

        embed = discord.Embed(description=message)
        embed.set_footer(text="Written by Frankup")
        embed.set_author(icon_url=ctx.message.author.avatar_url, name=ctx.message.author.display_name + " needs help!")
        embed.colour = ctx.message.author.colour if hasattr(ctx.message.author, "colour") else discord.Colour.default()
        await self.send_message(ctx.message.channel, embed=embed)

    async def on_message(self, message):
        await self.process_commands(message)
        #wordie
        #if message.channel.id == "474581363442319360":
        #    messages = []
        #    async for m in self.logs_from(message.channel, limit=2):
        #        messages.append(m)
        #    last_letter = messages[1].content[-1:].lower()
        #    first_letter = messages[0].content[0].lower()
        #    if last_letter != first_letter:
        #        await self.delete_message(message)

        #10000 numbers
        if message.channel.id == "474581363442319360":
            try:
                int(message.content)
            except ValueError:
                await self.delete_message(message)
                return

            messages = []
            async for m in self.logs_from(message.channel, limit=2):
                messages.append(m)
            previous_number = messages[1].content
            posted_number = messages[0].content
            print(previous_number + " " + posted_number)
            if (int(previous_number) + 1) != int(posted_number):
                await self.delete_message(message)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
