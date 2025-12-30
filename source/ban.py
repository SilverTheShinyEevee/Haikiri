import discord
from discord.ext import commands

from logger import create_logger


BAN_BOMB_ROLE_NAME = "Ban Bomb"


class BanBomb(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = create_logger(self.__class__.__name__)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Ignore DMs
        if message.guild is None:
            return

        # Ignore bots (including ourselves)
        if message.author.bot:
            return

        member: discord.Member = message.author

        # Optional safety: ignore admins/mods
        if member.guild_permissions.administrator:
            return

        # Find the ban-bomb role
        ban_role = discord.utils.get(
            message.guild.roles,
            name=BAN_BOMB_ROLE_NAME
        )

        if ban_role is None:
            # Misconfiguration — log once and stop
            self.logger.error(
                f"Ban bomb role '{BAN_BOMB_ROLE_NAME}' not found in guild {message.guild.name}"
            )
            return

        # Check if member has the role
        if ban_role in member.roles:
            try:
                # Optional: delete the triggering message
                await message.delete()

                # Ban the member
                await member.ban(
                    reason="Failed onboarding verification (ban bomb role)"
                )

                self.logger.warning(
                    f"Banned {member} ({member.id}) for ban bomb role"
                )

            except discord.Forbidden:
                self.logger.error(
                    f"Missing permissions to ban {member} ({member.id})"
                )

            except discord.HTTPException as e:
                self.logger.error(
                    f"Failed to ban {member} ({member.id}): {e}"
                )


async def setup(bot: commands.Bot):
    await bot.add_cog(BanBomb(bot))
