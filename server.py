import http.server
import json
import os
import urllib.request

PORT = 31350
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

JSONBIN_BIN_ID = "6a11bbaeee5a733b12091d85"
JSONBIN_API_KEY = "$2a$10$aoJ7a95xZXvGz/qS.oAmuOf9sP9uBJAs5xwvyj0bjU9DsJHGyYSm6"
JSONBIN_URL = f"https://api.jsonbin.io/v3/b/{JSONBIN_BIN_ID}"

class SmartServer(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_POST(self):
        if self.path == '/save':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            # Send data to JSONBin instead of local file
            req = urllib.request.Request(
                JSONBIN_URL,
                data=post_data,
                method='PUT'
            )
            req.add_header('Content-Type', 'application/json')
            req.add_header('X-Master-Key', JSONBIN_API_KEY)

            try:
                with urllib.request.urlopen(req) as res:
                    res.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"status":"saved"}')
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(f'{{"status":"error","message":"{str(e)}"}}'.encode())
        else:
            self.send_error(404, "File not found")

print(True, f"Stefi's Smart Server running on port {PORT}...")
http.server.HTTPServer(('0.0.0.0', PORT), SmartServer).serve_forever()
