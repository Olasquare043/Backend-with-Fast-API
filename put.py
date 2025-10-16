from http.server import BaseHTTPRequestHandler, HTTPServer
import json
data = [
    {"id": 1, "name": "Olayemi", "email": "olasquare@gmail.com", "kghhgds": "hfjghgfsf"},
    {"id": 2, "name": "Olayinka", "email": "olas@gmail.com", "kghhgds": "hkkhsf"}
]

class PutAPI(BaseHTTPRequestHandler):
    def send_data(self,payload,status):
        self.send_response(status)
        self.send_header("Content-Type","application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def do_PUT(self):
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
                return self.send_data({"message":"Record updated", "data": item}, status=200)
            
        # if loop finish and no record
        return self.send_data({"message":"Record not found"}, status=404)
def run():
    return HTTPServer(("localhost",5000), PutAPI).serve_forever()

print("The App hit the ground an running 🏃‍♀️‍➡️ 🏃‍♀️‍➡️ on port 5000 🏃‍♀️‍➡️")
run()