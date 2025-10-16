from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# creating class
class deleteAPI(BaseHTTPRequestHandler):
    def send_data(self, payload, status):
        self.send_response(status)
        self.send_header("content-Type","application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def do_DELETE(self):       
        try:
           id= int(self.path.strip("/"))  # get the id of item from the url path
        except ValueError:
            return self.send_data({f"message":"Invalid ID:"},status=400)

        for item in data:
            if id == item["id"]:
                data.remove(item)
                return self.send_data({"message":"Record deleted", "data": data}, status=200)
            
        # if loop finish and no record
        return self.send_data({"message":"Record not found"}, status=404)
def run():
    return HTTPServer(("localhost", 5000), deleteAPI).serve_forever()

print("The App hit the ground an running 🏃‍♀️‍➡️🏃‍♀️‍➡️🏃‍♀️‍➡️")
run()