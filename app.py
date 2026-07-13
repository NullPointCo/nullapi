#!/usr/bin/env python3
"""
NullAPI - Free utility APIs for developers
First product: QR Code Generator + URL Shortener

Deploy on Render free tier or run locally.
Sells via RapidAPI for $0.001-0.01 per call.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
import urllib.request
import hashlib
import os
import time

# Simple in-memory URL store (use SQLite for production)
url_store = {}

def generate_qr_svg(text, size=200):
    """Generate QR code as SVG using free API or manual encoding"""
    # Use the free QR Server API
    encoded = urllib.parse.quote(text)
    api_url = f"https://api.qrserver.com/v1/create-qr-code/?size={size}x{size}&data={encoded}"
    try:
        with urllib.request.urlopen(api_url, timeout=10) as resp:
            return resp.read()
    except:
        return None

def generate_id(url):
    """Generate short ID from URL"""
    return hashlib.md5(url.encode()).hexdigest()[:8]

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        
        # Root - health check
        if parsed.path == '/':
            self.send_json({
                "service": "NullAPI",
                "version": "1.0.0",
                "endpoints": {
                    "/qr?text=hello": "Generate QR code",
                    "/shorten?url=example.com": "Create short URL",
                    "/s/{id}": "Redirect to original URL",
                    "/api/v1/status": "API status"
                }
            })
            return
        
        # QR Code endpoint
        if parsed.path == '/qr':
            text = params.get('text', [''])[0]
            size = int(params.get('size', ['200'])[0])
            if not text:
                self.send_json({"error": "Missing 'text' parameter"}, 400)
                return
            qr_data = generate_qr_svg(text, size)
            if qr_data:
                self.send_response(200)
                self.send_header('Content-Type', 'image/png')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(qr_data)
            else:
                self.send_json({"error": "QR generation failed"}, 500)
            return
        
        # Shorten URL
        if parsed.path == '/shorten':
            url = params.get('url', [''])[0]
            if not url:
                self.send_json({"error": "Missing 'url' parameter"}, 400)
                return
            short_id = generate_id(url + str(time.time()))
            url_store[short_id] = {
                "url": url,
                "created": time.time(),
                "clicks": 0
            }
            self.send_json({
                "short_id": short_id,
                "short_url": f"{parsed.scheme}://{self.headers.get('Host', 'localhost:8080')}/s/{short_id}",
                "original_url": url
            })
            return
        
        # Redirect short URL
        if parsed.path.startswith('/s/'):
            short_id = parsed.path[3:]
            if short_id in url_store:
                url_store[short_id]["clicks"] += 1
                self.send_response(302)
                self.send_header('Location', url_store[short_id]["url"])
                self.end_headers()
            else:
                self.send_json({"error": "Short URL not found"}, 404)
            return
        
        # Stats
        if parsed.path == '/api/v1/status':
            self.send_json({
                "urls_shortened": len(url_store),
                "total_clicks": sum(u["clicks"] for u in url_store.values())
            })
            return
        
        self.send_json({"error": "Not found"}, 404)
    
    def send_json(self, data, code=200):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    server = HTTPServer(('0.0.0.0', port), Handler)
    print(f"NullAPI running on port {port}")
    server.serve_forever()
