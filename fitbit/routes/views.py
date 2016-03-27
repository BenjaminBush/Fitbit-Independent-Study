from intraday import intraday
from flask import render_template, request, session, url_for, redirect, jsonify
import requests, psycopg2

@intraday.route('/')
def home():
    return render_template('home.html')
