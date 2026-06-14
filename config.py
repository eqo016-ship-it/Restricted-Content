# @name config.py_v2.0
from os import getenv
from time import time
from dotenv import load_dotenv

# WAJIB: Memuat variabel dari file .env ke dalam sistem
load_dotenv()

def _require_env(name: str) -> str:
    value = getenv(name)
    if not value or not str(value).strip():
        raise ValueError(f"Variabel {name} belum diisi di file .env")
    return value.strip()

class PyroConf(object):
    API_ID = int(_require_env("API_ID"))
    API_HASH = _require_env("API_HASH")
    BOT_TOKEN = _require_env("BOT_TOKEN")
    SESSION_STRING = _require_env("SESSION_STRING")

    BOT_START_TIME = time()
    PORT = int(getenv("PORT", "8080"))
    MAX_CONCURRENT_DOWNLOADS = int(getenv("MAX_CONCURRENT_DOWNLOADS", "1"))
    MAX_CONCURRENT_UPLOADS = int(getenv("MAX_CONCURRENT_UPLOADS", "1"))
    MAX_CONCURRENT_TRANSMISSIONS = int(getenv("MAX_CONCURRENT_TRANSMISSIONS", "2"))
    BATCH_SIZE = int(getenv("BATCH_SIZE", "1"))
    FLOOD_WAIT_DELAY = int(getenv("FLOOD_WAIT_DELAY", "5"))
    STORAGE_CLEANUP_INTERVAL = int(getenv("STORAGE_CLEANUP_INTERVAL", "15"))

    @staticmethod
    def get_proxy():
        """Baca pengaturan proxy dari .env (socks5/http/mtproto)."""
        scheme = (getenv("PROXY_SCHEME") or "").strip().lower()
        if not scheme:
            return None

        proxy = {
            "scheme": scheme,
            "hostname": (getenv("PROXY_HOST") or "127.0.0.1").strip(),
            "port": int(getenv("PROXY_PORT", "1080")),
        }

        username = (getenv("PROXY_USER") or "").strip()
        password = (getenv("PROXY_PASS") or "").strip()
        secret = (getenv("PROXY_SECRET") or "").strip()

        if username:
            proxy["username"] = username
        if password:
            proxy["password"] = password
        if scheme == "mtproto" and secret:
            proxy["secret"] = secret

        return proxy