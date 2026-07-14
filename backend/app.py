# backend/app.py

from flask import Flask, send_from_directory
from flask_cors import CORS
from api.routes import register_routes
import os

# Create Flask app
app = Flask(__name__, static_folder='../frontend/build', static_url_path='')
CORS(app)

# Register API routes
register_routes(app)

# Serve React app
@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True, port=5000)