#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deutsch A1 - ლოკალური სერვერი (Localhost Server)
გერმანული ენის შემსწავლელი ქართულენოვანი პლატფორმა
"""

import http.server
import socketserver
import os
import sys
import webbrowser
import socket

# Ensure directory is German A1 root
DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(DIR)

DEFAULT_PORT = 8000

class CustomHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/favicon.ico':
            self.send_response(204)
            self.end_headers()
            return
        super().do_GET()

    def do_POST(self):
        if self.path == '/api/qa-results':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            results_dir = os.path.join(DIR, "tests")
            os.makedirs(results_dir, exist_ok=True)
            results_file = os.path.join(results_dir, "_safari_qa_results.json")
            with open(results_file, "wb") as f:
                f.write(post_data)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
            return
        self.send_response(404)
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def end_headers(self):
        # Enable CORS and caching headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def guess_type(self, path):
        mtype = super().guess_type(path)
        if path.endswith(".js"):
            return "application/javascript; charset=utf-8"
        if path.endswith(".css"):
            return "text/css; charset=utf-8"
        if path.endswith(".html"):
            return "text/html; charset=utf-8"
        if path.endswith(".json"):
            return "application/json; charset=utf-8"
        return mtype

    def log_message(self, format, *args):
        # Clean logging
        sys.stderr.write(f"[{self.log_date_time_string()}] {format % args}\n")

def find_available_port(start_port=DEFAULT_PORT, max_tries=20):
    for port in range(start_port, start_port + max_tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) != 0:
                return port
    return DEFAULT_PORT

def main():
    port = find_available_port(DEFAULT_PORT)
    url = f"http://localhost:{port}"

    banner = f"""
======================================================================
  🇩🇪 DEUTSCH A1 • გერმანული ენის სრული პლატფორმა (A1 დონე)
  ქართულენოვანი საუნივერსიტეტო სტანდარტი (Schritte / Menschen)
======================================================================

  🌐 საიტი გაშვებულია ლოკალურ მისამართზე (Localhost):
     👉 {url}

  💡 შეგიძლიათ გახსნათ ბრაუზერში (Chrome, Safari, Firefox).
  🛑 გასაჩერებლად დააჭირეთ კლავიატურაზე: Ctrl + C
======================================================================
"""
    print(banner)

    # Automatically try opening the browser
    try:
        webbrowser.open(url)
    except Exception:
        pass

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", port), CustomHTTPHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 სერვერი შეჩერებულია. წარმატებულ სწავლას გისურვებთ!")
            sys.exit(0)

if __name__ == "__main__":
    main()
