from intraday import intraday
from flask import render_template, request, session, url_for, redirect, jsonify
import requests, psycopg2

import fitbit

@intraday.route('/')
def home():
    return render_template('home.html')

@intraday.route('/auth_redirect')
def auth_redirect():
    print('hello')

    cur = intraday.db.cursor()
    print('cur')

    result = requests.post('https://api.fitbit.com/oauth2/token', data={
        'client_id': '227FD3',
        'client_secret': '5543280369ea955f96decf9e635c29f9',
        'grant_type': 'authorization_code',
        'redirect_uri': 'https://intraday.herokuapp.com/auth_redirect',
        'code': request.args.get('code')
    })
    print('result:')
    result = result.json()
    print('result-json:')

    insert_user_query = """
            INSERT INTO users (
                    id,
                    device_name,
                    access_token,
                    refresh_token
                )
            VALUES (%s, %s, %s, %s)"""
    cur.execute(insert_user_query, (
        result['user_id'],
        result['access_token'],
        result['refresh_token']
    ))

    cur.close()
    return render_template('home.html')
