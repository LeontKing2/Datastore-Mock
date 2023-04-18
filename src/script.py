import json
from http.server import BaseHTTPRequestHandler, HTTPServer

data_store = {}

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/favicon.ico':
            self.send_response(404)
            self.end_headers()
        else:
            key = self.path[1:]
            if key in data_store:
                response = {
                    'status': 'success',
                    'data': data_store[key]
                }
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
            else:
                response = {
                    'status': 'error',
                    'message': 'Key not found'
                }
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode())
        key = self.path[1:]
        if key in data_store:
            response = {
                'status': 'error',
                'message': 'Key already exists'
            }
            self.send_response(400)
        else:
            data_store[key] = data
            response = {
                'status': 'success',
                'message': 'Data created successfully'
            }
            self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting server on port', port)
    httpd.serve_forever()

if __name__ == '__main__':
    run()
