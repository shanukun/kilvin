from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

from kilvin import log
from kilvin.utils import is_kilvin_dir

PORT = 8000
PUBLIC = "./public"


class KilvinHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PUBLIC, **kwargs)


class KilvinTCPServer(TCPServer):
    def __init__(self, *args, **kwargs):
        self.allow_reuse_address = True
        super().__init__(*args, **kwargs)


@is_kilvin_dir
def start_server():
    handler = KilvinHTTPRequestHandler
    with KilvinTCPServer(("", PORT), handler) as httpd:
        log.info(f"Serving at port: {PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            log.info("Shutting down server.")
            httpd.server_close()
