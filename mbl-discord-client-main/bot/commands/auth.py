import asyncio
import discord
from discord.ext import commands
from bot.services import api


def extract_response(result):
    if not result:
        return None, "Empty response"

    if isinstance(result, dict) and "status" in result:
        if result["status"] != "success":
            return None, result.get("message") or result.get("error") or "Unknown error"
        return result.get("data", {}), None

    if isinstance(result, dict):
        return result, None

    return None, "Unexpected response format"


class Auth(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # key = user_id, value = data akun login
        self.sessions = {}

    @commands.command(name="login")
    async def login(self, ctx):
        """Login via DM, simpan session user"""
        user_id = ctx.author.id

        if user_id in self.sessions:
            await ctx.send("⚠️ Kamu sudah login. Gunakan `!logout` dulu kalau mau ganti akun.")
            return

        try:
            await ctx.author.send("📝 Masukkan username:")
            msg_username = await self.bot.wait_for(
                "message",
                check=lambda m: m.author == ctx.author and isinstance(m.channel, discord.DMChannel),
                timeout=60
            )
            username = msg_username.content.strip()

            await ctx.author.send("🔑 Masukkan password:")
            msg_password = await self.bot.wait_for(
                "message",
                check=lambda m: m.author == ctx.author and isinstance(m.channel, discord.DMChannel),
                timeout=60
            )
            password = msg_password.content.strip()

        except asyncio.TimeoutError:
            await ctx.send("⏰ Login dibatalkan (tidak ada respon).")
            return
        except discord.Forbidden:
            await ctx.send("❌ Tidak bisa kirim DM, pastikan DM dari server ini diizinkan.")
            return
        except Exception as e:
            await ctx.send(f"⚠️ Terjadi error saat login: {e}")
            return

        result = await api.login(username, password)
        data, error = extract_response(result)

        if error:
            await ctx.send(f"❌ Gagal login: {error}")
        else:
            self.sessions[user_id] = data
            await ctx.send(f"✅ Login berhasil! ({ctx.author.mention})")

    @commands.command(name="logout")
    async def logout(self, ctx):
        """Logout dan hapus session user"""
        user_id = ctx.author.id
        if user_id not in self.sessions:
            await ctx.send("⚠️ Kamu belum login.")
            return

        del self.sessions[user_id]
        await ctx.send("✅ Kamu berhasil logout.")

    @commands.command(name="dashboard")
    async def dashboard(self, ctx):
        """Ambil info dashboard dari API"""
        user_id = ctx.author.id
        if user_id not in self.sessions:
            await ctx.send("⚠️ Kamu harus login dulu pakai `!login`")
            return

        result = await api.get_dashboard()
        data, error = extract_response(result)

        if error:
            await ctx.send(f"❌ Gagal ambil dashboard: {error}")
            return

        embed = discord.Embed(
            title="📊 Dashboard",
            description="Informasi akun kamu",
            color=discord.Color.blurple()
        )

        if "nama" in data:
            embed.add_field(name="👤 Nama", value=data["nama"], inline=False)
        if "nim" in data:
            embed.add_field(name="🆔 NIM", value=data["nim"], inline=True)
        if "kelas" in data:
            embed.add_field(name="🏫 Kelas", value=data["kelas"], inline=True)
        if "semester" in data:
            embed.add_field(name="📚 Semester", value=data["semester"], inline=True)

        for k, v in data.items():
            if k not in ["nama", "nim", "kelas", "semester"]:
                embed.add_field(name=k.capitalize(), value=str(v), inline=False)

        await ctx.send(embed=embed)

    @commands.command(name="jadwalujian")
    async def jadwalujian(self, ctx):
        """Ambil jadwal ujian dari API"""
        user_id = ctx.author.id
        if user_id not in self.sessions:
            await ctx.send("⚠️ Kamu harus login dulu pakai `!login`")
            return

        result = await api.get_jadwal_ujian()
        data, error = extract_response(result)

        if error:
            await ctx.send(f"❌ Gagal ambil jadwal: {error}")
            return

        jadwal = data.get("jadwal", []) if isinstance(data, dict) else []
        if not jadwal:
            await ctx.send("📅 Tidak ada jadwal ujian ditemukan.")
            return

        tipe = data.get("meta", {}).get("type", "UJIAN")
        warna = discord.Color.blue() if tipe == "UTS" else discord.Color.red()

        embed = discord.Embed(
            title=f"📅 Jadwal {tipe}",
            description=f"Total: {len(jadwal)}",
            color=warna
        )

        for j in jadwal:
            mata_kuliah = j.get("mata_kuliah") or j.get("matakuliah")
            tanggal = j.get("tanggal") or j.get("waktu", {}).get("tanggal")
            jam_mulai = j.get("waktu", {}).get("jam_mulai")
            jam_selesai = j.get("waktu", {}).get("jam_selesai")
            ruang = j.get("ruangan") or j.get("no_ruang")

            embed.add_field(
                name=mata_kuliah,
                value=f"🗓 {tanggal}\n🕒 {jam_mulai} - {jam_selesai}\n📍 {ruang}",
                inline=False
            )

        await ctx.send(embed=embed)

    @commands.command(name="jadwalpengganti")
    async def jadwalpengganti(self, ctx):
        """Ambil jadwal kuliah pengganti dari API"""
        user_id = ctx.author.id
        if user_id not in self.sessions:
            await ctx.send("⚠️ Kamu harus login dulu pakai `!login`")
            return

        result = await api.get_jadwal_pengganti()
        data, error = extract_response(result)

        if error:
            await ctx.send(f"❌ Gagal ambil jadwal: {error}")
            return

        jadwal = data.get("jadwal", []) if isinstance(data, dict) else []
        if not jadwal:
            await ctx.send("📅 Tidak ada jadwal pengganti ditemukan.")
            return

        embed = discord.Embed(
            title="📅 Jadwal Pengganti",
            description=f"Total: {len(jadwal)}",
            color=discord.Color.green()
        )

        for j in jadwal:
            mata_kuliah = j.get("mata_kuliah")
            tanggal = j.get("tanggal")
            hari = j.get("waktu", {}).get("hari")
            jam_mulai = j.get("waktu", {}).get("jam_mulai")
            jam_selesai = j.get("waktu", {}).get("jam_selesai")
            ruang = j.get("no_ruang")

            embed.add_field(
                name=mata_kuliah,
                value=f"🗓 {hari}, {tanggal}\n🕒 {jam_mulai} - {jam_selesai}\n📍 {ruang}",
                inline=False
            )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Auth(bot))