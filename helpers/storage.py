import os
import shutil
import threading
import time

from logger import LOGGER

DOWNLOADS_DIR = "downloads"
LOG_FILE = "logs.txt"


def cleanup_downloads_folder(max_age_seconds: int = 1800) -> int:
    """Hapus file lama di folder downloads/ agar hemat storage Koyeb."""
    if not os.path.isdir(DOWNLOADS_DIR):
        return 0

    removed = 0
    now = time.time()
    for name in os.listdir(DOWNLOADS_DIR):
        path = os.path.join(DOWNLOADS_DIR, name)
        try:
            if not os.path.isfile(path):
                continue
            if name.endswith(".temp") or (now - os.path.getmtime(path) > max_age_seconds):
                os.remove(path)
                removed += 1
        except OSError as e:
            LOGGER(__name__).warning(f"Gagal hapus {path}: {e}")

    return removed


def cleanup_logs(max_bytes: int = 4 * 1024 * 1024) -> bool:
    """Potong logs.txt jika terlalu besar (backup max ~5MB dari RotatingFileHandler)."""
    try:
        if os.path.isfile(LOG_FILE) and os.path.getsize(LOG_FILE) > max_bytes:
            backup = LOG_FILE + ".old"
            if os.path.exists(backup):
                os.remove(backup)
            os.rename(LOG_FILE, backup)
            open(LOG_FILE, "a", encoding="utf-8").close()
            return True
    except OSError as e:
        LOGGER(__name__).warning(f"Gagal bersihkan log: {e}")
    return False


def run_storage_cleanup():
    removed = cleanup_downloads_folder()
    logs_trimmed = cleanup_logs()
    if removed or logs_trimmed:
        LOGGER(__name__).info(f"Auto clean: {removed} file dihapus, log dipotong={logs_trimmed}")


def start_storage_cleaner(interval_minutes: int = 15):
    """Jalankan pembersihan storage berkala di background thread."""

    def _loop():
        while True:
            time.sleep(max(interval_minutes, 5) * 60)
            try:
                run_storage_cleanup()
            except Exception as e:
                LOGGER(__name__).error(f"Auto clean gagal: {e}")

    thread = threading.Thread(target=_loop, daemon=True, name="storage-cleaner")
    thread.start()
    return thread
