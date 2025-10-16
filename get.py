from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

data_file_path= "data."

class GetAPI(BaseHTTPRequestHandler):
    def send_data(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        if self.path=="/":
           return self.send_data(data)
        try:
            id= int(self.path.strip("/"))
        except ValueError:
            return self.send_data({"message":f"Invalid ID: {id}"}, status=400)
        # finding the actual record with the ID
        for item in data:
            if id==item["id"]:
                return self.send_data({"message":"Here is the record:", "data":item})
        # if loop finish and no record
        return self.send_data({"message":"Record not found"}, status=404)
def run():
    HTTPServer(('localhost', 5000),GetAPI).serve_forever()
if __name__ == "__main__":
    print("The App hit the ground an running 🏃‍♀️‍➡️ 🏃‍♀️‍➡️ on port 5000 🏃‍♀️‍➡️")
    run()