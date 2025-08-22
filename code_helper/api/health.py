"""
Vercel serverless function for health check.
"""

from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        response = {
            "status": "healthy",
            "message": "Demo version running on Vercel",
            "analyzer_ready": False,
            "model_loaded": False,
            "note": "Full functionality requires local deployment with gpt-oss-20b"
        }

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
        return
