from pathlib import Path
import discord
from discord.ext import commands


class OnMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bad_words = self.load_bad_words()

    def load_bad_words(self):
        """Load daftar kata terlarang dari config/bad_words.txt"""
        path = Path(__file__).resolve().parent.parent / "config" / "bad_words.txt"
        if path.exists():
            return [
                line.strip().lower()
                for line in path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
        return []

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        content = message.content.lower()

        if any(word in content for word in self.bad_words):
            try:
                await message.delete()
                await message.channel.send(
                    f"⚠️ {message.author.mention}, pesanmu mengandung kata terlarang dan telah dihapus.",
                    delete_after=30
                )
            except discord.Forbidden:
                print("⚠️ Bot tidak punya izin hapus pesan.")
            return


async def setup(bot):
    await bot.add_cog(OnMessage(bot))