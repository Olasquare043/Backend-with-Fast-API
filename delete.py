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
# creating class
class deleteAPI(BaseHTTPRequestHandler):
    def send_data(self, payload, status):
        self.send_response(status)
        self.send_header("content-Type","application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def do_DELETE(self): 
        # load data from file
        data = load_data()

        # getting ID from url path

        try:
           id= int(self.path.strip("/"))  # get the id of item from the url path
        except ValueError:
            return self.send_data({f"message":"Invalid ID:"},status=400)

        for item in data:
            if id == item["id"]:
                data.remove(item)
                if save_to_db(data):
                    return self.send_data({"message":"Record deleted", "data": data}, status=200)
                else:
                    return self.send_data({"message":"Unable to save the data", "data": data}, status=400)
    
        # if loop finish and no record
        return self.send_data({"message":"Record not found"}, status=404)
def run():
    return HTTPServer(("localhost", 5000), deleteAPI).serve_forever()

print("The App hit the ground an running 🏃‍♀️‍➡️🏃‍♀️‍➡️🏃‍♀️‍➡️")
run()