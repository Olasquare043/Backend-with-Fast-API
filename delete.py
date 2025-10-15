from http.server import BaseHTTPRequestHandler, HTTPServer
import json

data=[
    {
    "id": 1,
    "name": "Olayemi",
    "email": "olasquare@gmail.com",
    "kghhgds": "hfjghgfsf"  
},
{
    "id": 2,
    "name": "Olayinka",
    "email": "olas@gmail.com",
    "kghhgds": "hkkhsf"
}
]
# creating class
class deleteAPI(BaseHTTPRequestHandler):
    def send_data(self, payload, status):
        self.send_response(status)
        self.send_header("content-Type","application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def do_DELETE(self):
        content_size= int(self.headers.get("Content-Length", 0))
        parse_data= self.rfile.read(content_size)
        updated_data= json.loads(parse_data)
        if self.path=="/":
            return self.send_data({"message":"Content to change can not be empty"}, status=400)  
        # get the index of item from the specified route id
        id= int(self.path.split("/"))
        if updated_data:
            for item in data:
                if id == item["id"]:
                    data.update(updated_data)
                    return self.send_data({"message":"Record updated"}, status=200)
                else:
                    return self.send_data({"message":"Record not found"}, status=400)
        else: 
            return self.send_data({"message":"Content to change can not be empty"}, status=400)
def run():
    return HTTPServer(("localhost", 5000), deleteAPI).serve_forever()

print("The App hit the ground an running 🏃‍♀️‍➡️🏃‍♀️‍➡️🏃‍♀️‍➡️")
run()