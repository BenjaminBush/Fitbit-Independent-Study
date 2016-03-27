from flask import Flask, render_template, request, session, url_for, redirect, jsonify
from werkzeug.contrib.fixers import ProxyFix
import requests, psycopg2

from routes import views

intraday = Flask(__name__)
intraday.wsgi_app = ProxyFix(intraday.wsgi_app)

conn = psycopg2.connect("dbname='dc7qf7cii79rie' password='9yuoOs84Nr7k-r3H7ioZxVzPoV' user='qhazfngzupdgdj' host='ec2-54-83-22-48.compute-1.amazonaws.com' port='5432'");
conn.autocommit = True

intraday.db = conn
intraday.secret_key = 'i\x0b\x8d\r\xc2\xa83\x1dD8\x10_\xb8Q\x87\xce@\xf1k\xd6\x14\xa1\xffP'
