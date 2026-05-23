import http.server
import json
import os

PORT = 31350
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class SmartServer(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Tell the server to watch our specific directory
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    # This handles incoming save data from your phone
    def do_POST(self):
        if self.path == '/save':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Save the exact data into counts.json right on the PC hard drive
            json_path = os.path.join(DIRECTORY, 'counter', 'counts.json')
            with open(json_path, 'w') as f:
                f.write(post_data.decode('utf-8'))
            
            # Tell the phone "Success!"
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"saved"}')
        else:
            self.send_error(404, "File not found")

print(True, f"Stefi's Smart Server running on port {PORT}...")
http.server.HTTPServer(('0.0.0.0', PORT), SmartServer).serve_forever()