from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("✅ Ping cog loaded")   # Debug print saat class diinisialisasi

    @commands.command(name="ping")
    async def ping(self, ctx):
        await ctx.send(f"🏓 Pong! Latency: {round(self.bot.latency * 1000)}ms")

async def setup(bot):
    print("⚡ setup() in ping.py called")  # Debug print saat setup() dipanggil
    await bot.add_cog(Ping(bot))