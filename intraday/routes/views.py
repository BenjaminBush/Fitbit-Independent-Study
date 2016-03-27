from intraday import intraday
from flask import render_template, request, session, url_for, redirect, jsonify
import requests, psycopg2

import fitbit

@intraday.route('/')
def home():
    return render_template('home.html')

@intraday.route('/auth_redirect')
def auth_redirect():
    cur = blitzkrieg.db.cursor()

    result = requests.post('https://api.fitbit.com/oauth2/token', data={
        'client_id': '227FD3',
        'client_secret': '5543280369ea955f96decf9e635c29f9',
        'grant_type': 'authorization_code',
        'redirect_uri': 'https://intraday.herokuapp.com/auth_redirect',
        'code': request.args.get('code')
    })
    result = result.json()
    user_info = result['user']


    insert_instagram_user_query = """
            INSERT INTO users (
                    id,
                    device_name,
                    access_token,
                    refresh_token
                )
            VALUES (%s, %s, %s, %s)"""
    cur.execute(insert_instagram_user_query, (
        user_info['user_id'],
        user_info['access_token'],
        user_info['refresh_token']
    ))

    cur.close()
    return render_template('home.html')
