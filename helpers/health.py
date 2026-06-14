import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from time import time

from config import PyroConf
from helpers.files import get_readable_time

_server = None


class _HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path in ("/", "/health", "/ping"):
            uptime = get_readable_time(time() - PyroConf.BOT_START_TIME)
            body = json.dumps({"status": "ok", "uptime": uptime}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        self.send_response(404)
        self.end_headers()

    def log_message(self, *_):
        pass


def start_health_server(port: int):
    global _server
    if _server is not None:
        return _server

    _server = ThreadingHTTPServer(("0.0.0.0", port), _HealthHandler)
    thread = threading.Thread(target=_server.serve_forever, daemon=True)
    thread.start()
    return _server
