from http.server import BaseHTTPRequestHandler, HTTPServer
import json 
import os
file_path = "database.json"

# function to load data from file

def load_data():
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        return json.load(f)
    
# function to save to file 
def save_to_db(data_to_update):
    if data_to_update:
        with open(file_path, "w") as f:
            json.dump(data_to_update, f, indent=2)
            return True
    else:
        return False
    
class PatchAPI(BaseHTTPRequestHandler):
    def send_data(self,payload, status):
        self.send_response(status)
        self.send_header("Content-Type","application/json")
        self.end_headers()
        self.rfile.read(json.dumps(payload).encode())
    def do_PATCH(self):
        content_size= int(self.headers.get("Content-Length",0))
        parse_data= self.rfile.read(content_size)
        read_data= json.loads(parse_data)
        