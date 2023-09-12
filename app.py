import os

from flask import Flask, request, jsonify, make_response, render_template
app = Flask(__name__, static_url_path='', static_folder='./static')
