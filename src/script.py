import http.server
import json
import os
import socketserver

PORT = 8001  # Change this to the desired port number

class MyHandler(http.server.BaseHTTPRequestHandler):
    def _send_response(self, code, message):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Max-Age', '86400')
        self.end_headers()
        self.wfile.write(json.dumps(message).encode())

    def do_OPTIONS(self):
        self._send_response(200, {})

    def do_GET(self):
        self._send_response(404, {'error': 'Not found'})

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        payload = self.rfile.read(content_length)
        data = json.loads(payload.decode())
        path = self.path.strip('/')
        parts = path.split('/')
        if len(parts) != 4 or parts[0] != 'datastore':
            self._send_response(400, {'error': 'Invalid path'})
            return
        scope = parts[2]
        name = parts[3]
        key = self.headers.get('X-Key')
        if not key:
            self._send_response(400, {'error': 'Key not provided'})
            return
        if self.headers.get('X-Method') == 'SetAsync':
            value = json.loads(payload.decode())
            with open(f'{scope}_{name}_{key}.json', 'w') as f:
                json.dump(value, f)
            self._send_response(200, {'success': True})
        elif self.headers.get('X-Method') == 'GetAsync':
            try:
                with open(f'{scope}_{name}_{key}.json', 'r') as f:
                    value = json.load(f)
                self._send_response(200, {'success': True, 'value': value})
            except FileNotFoundError:
                self._send_response(404, {'error': 'Data not found'})
        else:
            self._send_response(400, {'error': 'Invalid method'})

if __name__ == '__main__':
    os.makedirs('datastore', exist_ok=True)
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("Server started on port", PORT)
        httpd.serve_forever()
