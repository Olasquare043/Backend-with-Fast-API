from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

file_path= "database.json"
# load data function
def load_data():
    if not os.path.exists(file_path):
        return []
    with open(file_path) as f:
        return json.load(f)
# function to update the json file
def update_database(data_to_update):
    if data_to_update:
        with open(file_path, 'w') as f:
            json.dump(data_to_update,f, indent=2)
            return True
    return False


class BasicAPI(BaseHTTPRequestHandler):
    def send_data(self, payload,status=200):
        self.send_response(status)
        self.send_header("Content-Type","application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def do_POST(self):
        # load the dats from file
        data= load_data()
        # get the incoming data from the request
        content_size= int(self.headers.get("Content-Length", 0))
        parse_data= self.rfile.read(content_size)
        post_data = json.loads(parse_data)
        data.append(post_data)
        updated=update_database(data)
        if updated:
            return self.send_data({"Message": "Data Received and Saved ","data": post_data},status= 201)
        else:
            return self.send_data({"Message": "Failed to save data "},status= 500)

def run():
     HTTPServer(('localhost', 5000),BasicAPI).serve_forever()
if __name__ == "__main__":
    print("The App hit the ground an running 🏃‍♀️‍➡️ 🏃‍♀️‍➡️ on port 5000 🏃‍♀️‍➡️")
    run()