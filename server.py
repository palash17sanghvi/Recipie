#!/usr/bin/env python3
"""
Simple HTTP server to serve the recipe application files.
This server serves HTML files and JSON data for the recipe application.
"""

import http.server
import socketserver
import os
import json
from urllib.parse import urlparse, parse_qs

class RecipeHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)
    
    def end_headers(self):
        # Add CORS headers to allow cross-origin requests
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def log_message(self, format, *args):
        # Suppress favicon.ico 404 errors
        if 'favicon.ico' not in str(args):
            super().log_message(format, *args)
    
    def do_GET(self):
        # Parse the URL
        parsed_path = urlparse(self.path)
        
        # Handle root path - serve index.html
        if parsed_path.path == '/' or parsed_path.path == '':
            self.path = '/index.html'
        
        # Handle JSON file requests
        if parsed_path.path.endswith('.json'):
            try:
                # Read and serve JSON files
                json_file = parsed_path.path[1:]  # Remove leading slash
                if os.path.exists(json_file):
                    with open(json_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Remove BOM if present
                        if content.startswith('\ufeff'):
                            content = content[1:]
                        
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(content.encode('utf-8'))
                    return
                else:
                    self.send_error(404, f"File not found: {json_file}")
                    return
            except Exception as e:
                self.send_error(500, f"Error reading JSON file: {str(e)}")
                return
        
        # For all other files, use the default handler
        super().do_GET()

def start_server(port=8000):
    """Start the HTTP server on the specified port."""
    try:
        with socketserver.TCPServer(("", port), RecipeHandler) as httpd:
            print(f"Recipe server starting on port {port}")
            print(f"Open your browser and go to: http://localhost:{port}")
            print("Press Ctrl+C to stop the server")
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"Port {port} is already in use. Trying port {port + 1}")
            start_server(port + 1)
        else:
            print(f"Error starting server: {e}")

if __name__ == "__main__":
    import sys
    
    # Check if port is provided as command line argument
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number. Using default port 8000.")
    
    start_server(port)
