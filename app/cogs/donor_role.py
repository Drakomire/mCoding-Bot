from typing import Optional, TYPE_CHECKING

import discord
from discord.ext import commands

if TYPE_CHECKING:
    from app.bot import Bot


class DonorRole(commands.Cog):

    def __init__(self, bot: "Bot"):
        self.bot = bot

        self.donor_role_id = 843135052036702218
        self.patron_role_id = 846834281535504434
        self.mcoding_server_id = 826875707418214451

        self.donor_role: Optional[discord.Role] = None
        self.patron_role: Optional[discord.Role] = None
        self.mcoding_server: Optional[discord.Guild] = None

    async def set_objects_from_ids(self):
        if not self.bot.is_ready():
            await self.bot.wait_until_ready()

        if self.mcoding_server is None:
            self.mcoding_server = self.bot.get_guild(self.mcoding_server_id)

        if self.donor_role is None:
            self.donor_role = self.mcoding_server.get_role(self.donor_role_id)

        if self.patron_role is None:
            self.patron_role = self.mcoding_server.get_role(self.patron_role_id)

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if before.guild.id != self.mcoding_server_id:
            return

        await self.set_objects_from_ids()

        if len(before.roles) > len(after.roles):
            return

        # they received a role
        added_roles = [r for r in after.roles if r not in before.roles]

        if self.patron_role in added_roles:
            await after.add_roles(self.donor_role)


def setup(bot: "Bot"):
    bot.add_cog(DonorRole(bot))
