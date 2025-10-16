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



class PutAPI(BaseHTTPRequestHandler):
    def send_data(self,payload,status):
        self.send_response(status)
        self.send_header("Content-Type","application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def do_PUT(self):
        # load data from file
        data = load_data()

        # getting ID from url path
        try:
            id=int(self.path.strip("/"))
        except ValueError:
            return self.send_data({"message":"Invalid ID"}, status=400)
        # getting the input data
        content_size= int(self.headers.get("Content-Length",0))
        parse_data=self.rfile.read(content_size)
        data_to_update= json.loads(parse_data)

        # looking for the data
        for item in data:
            if item["id"]== id:
                item.update(data_to_update)
                
                if save_to_db(data):
                    return self.send_data({"message":"Record updated", "data": item}, status=200)
                else:
                    return self.send_data({"message":"Failed to save data"}, status=404)

        # if loop finish and no record
        return self.send_data({"message":"Record not found"}, status=404)
def run():
    return HTTPServer(("localhost",5000), PutAPI).serve_forever()

if __name__ == "__main__":
    print("The App hit the ground and running 🏃‍♀️‍➡️ on port 5000 🏃‍♀️‍➡️")
    run()