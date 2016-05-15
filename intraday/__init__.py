from flask import Flask, render_template, request, session, url_for, redirect, jsonify
from werkzeug.contrib.fixers import ProxyFix
import requests, psycopg2

intraday = Flask(__name__)
intraday.wsgi_app = ProxyFix(intraday.wsgi_app)

from routes import views

conn = psycopg2.connect() #Enter database information here
conn.autocommit = True

intraday.db = conn
intraday.secret_key = 'i\x0b\x8d\r\xc2\xa83\x1dD8\x10_\xb8Q\x87\xce@\xf1k\xd6\x14\xa1\xffP'
