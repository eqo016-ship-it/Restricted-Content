import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from time import time

from config import PyroConf
from helpers.files import get_readable_time

_server = None


class _HealthHandler(BaseHTTPRequestHandler):
    _OK_PATHS = ("/", "/health", "/ping", "/ok")

    def _respond_ok(self):
        path = self.path.split("?", 1)[0]
        if path == "/ok":
            body = b"ok"
            content_type = "text/plain; charset=utf-8"
        else:
            uptime = get_readable_time(time() - PyroConf.BOT_START_TIME)
            body = json.dumps({"status": "ok", "uptime": uptime}).encode()
            content_type = "application/json"

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path in self._OK_PATHS:
            self._respond_ok()
            return

        self.send_response(404)
        self.send_header("Connection", "close")
        self.end_headers()

    def do_HEAD(self):
        path = self.path.split("?", 1)[0]
        if path in self._OK_PATHS:
            body_len = 2 if path == "/ok" else len(
                json.dumps({"status": "ok", "uptime": "0s"}).encode()
            )
            self.send_response(200)
            self.send_header("Content-Type", "text/plain" if path == "/ok" else "application/json")
            self.send_header("Content-Length", str(body_len))
            self.send_header("Connection", "close")
            self.end_headers()
            return

        self.send_response(404)
        self.send_header("Connection", "close")
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
