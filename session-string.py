# @name SessionGenerator_v1.2
import asyncio
from pyrogram import Client
from dotenv import load_dotenv
from config import PyroConf

load_dotenv()

# ==========================================
# MASUKKAN DATA KAMU DI BAWAH INI (opsional)
# Kosongkan jika sudah diisi di file .env
# ==========================================
API_ID = PyroConf.API_ID
API_HASH = PyroConf.API_HASH
NOMOR_HP = ""  # Contoh: +62812xxxxxxx
# ==========================================

async def main():
    print("\n" + "="*50)
    print("🤖 Bot Simpan Konten Terbatas - Generator Sesi Otomatis")
    print("="*50 + "\n")

    phone = NOMOR_HP.strip() or input("Masukkan nomor HP (format +62...): ").strip()
    print(f"🔄 Mencoba login dengan nomor: {phone}...")
    proxy = PyroConf.get_proxy()
    if proxy:
        print(f"🌐 Menggunakan proxy: {proxy['scheme']}://{proxy['hostname']}:{proxy['port']}")

    try:
        async with Client(
            name="session",
            api_id=API_ID,
            api_hash=API_HASH,
            phone_number=phone,
            in_memory=True,
            proxy=proxy,
        ) as app:
            session = await app.export_session_string()
            print("\n✅ Autentikasi Berhasil!\n")
            print("👇 STRING SESI KAMU 👇\n")
            print(session)
            print("\n⚠️ Simpan string ini baik-baik dan JANGAN PERNAH bagikan ke siapa pun!")
            print("Salin ke SESSION_STRING di file .env")

    except KeyError as e:
        if e.args and e.args[0] == 0:
            print("\n❌ GAGAL TERHUBUNG KE SERVER TELEGRAM!")
            print("Penyebab: Jaringan atau ISP memblokir koneksi ke Telegram.")
            print("Solusi  : Aktifkan VPN (contoh: WARP 1.1.1.1) atau isi PROXY_* di .env, lalu coba lagi.")
        else:
            print(f"\n❌ Terjadi kesalahan (KeyError): {e}")
    except Exception as e:
        print(f"\n❌ Terjadi kesalahan saat autentikasi: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProses pembuatan sesi dibatalkan oleh pengguna.")
