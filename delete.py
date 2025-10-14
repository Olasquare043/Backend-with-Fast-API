from http.server import BaseHTTPRequestHandler, HTTPServer
import json

data=[
    {
    "name": "Olayemi",
    "email": "olasquare@gmail.com",
    "kghhgds": "hfjghgfsf"
}
]
# creating class
class delete(BaseHTTPRequestHandler):
    def send_data(self, payload, status=200):
        self.send_response(status)
        self.send_header("content-Type","application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def do_DELETE(self):
        content_size = int(self.headers.get("content-Length"),0)
        parse_data= self.rfile.read(content_size)
