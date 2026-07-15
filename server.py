from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os
import re

class FileHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/save':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            base_path = data.get('base_path', 'D:/my_project')
            files = data.get('files', {})
            
            created = 0
            errors = []
            file_list = []
            
            for file_path, content in files.items():
                full_path = os.path.join(base_path, file_path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                
                try:
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    created += 1
                    file_list.append(file_path)
                    print(f"✅ Created: {file_path}")
                except Exception as e:
                    errors.append(f"{file_path}: {str(e)}")
                    print(f"❌ Error: {file_path} - {e}")
            
            response = {
                'success': True,
                'created': created,
                'total': len(files),
                'errors': errors,
                'files': file_list
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            with open('index.html', 'rb') as f:
                self.wfile.write(f.read())
        else:
            super().do_GET()

if __name__ == '__main__':
    port = 8000
    print(f"""
╔═══════════════════════════════════════════════════════════╗
║  🚀 SERVER STARTED!                                      ║
║  📂 Open in browser: http://localhost:{port}             ║
║  📁 Files will be created on disk D:/my_project          ║
║  ⚠️  Press Ctrl+C to stop the server                     ║
║  💡 PASTE THE ENTIRE CHAT RESPONSE                       ║
╚═══════════════════════════════════════════════════════════╝
    """)
    server = HTTPServer(('localhost', port), FileHandler)
    server.serve_forever()