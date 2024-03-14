from src.app import app
from flask import Flask, redirect, request
from urllib.parse import urlparse, urlunparse
from flask_cors import CORS
CORS(app)


@app.route('/favicon.ico')
def favicon():
    return '', 204



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8001,debug=True)
