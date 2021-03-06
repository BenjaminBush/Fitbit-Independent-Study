from intraday import intraday
from flask import render_template, request, session, url_for, redirect, jsonify
import requests, psycopg2, base64

import fitbit
#Handle the routing
@intraday.route('/')
def home():
    return render_template('home.html')
#On the auth callback redirect to here:
@intraday.route('/auth_redirect')
def auth_redirect():

    cur = intraday.db.cursor()
    #Using a post request, send the client id + secret to grant authorization
    result = requests.post('https://api.fitbit.com/oauth2/token', data={
        'client_id': '227FD3',
        'client_secret': '5543280369ea955f96decf9e635c29f9',
        'grant_type': 'authorization_code',
        'redirect_uri': 'https://intraday.herokuapp.com/auth_redirect',
        'code': request.args.get('code')
    }, headers={
        'Authorization': b'Basic ' + base64.b64encode(('227FD3:5543280369ea955f96decf9e635c29f9').encode('utf8')),
        'Content-Type': 'application/x-www-form-urlencoded'
    })
    #Turn the result into JSON
    result = result.json()
    #See what is currently in the database
    cur.execute("""
            SELECT * FROM users WHERE id = %s
        """, (result['user_id'],))
    user = cur.fetchall()
    #Refresh the tokens if this is not a new user
    if len(user) > 0:
        cur.execute("""
                UPDATE users SET access_token = %s WHERE id = %s
            """, (result['access_token'], result['user_id']))
    else: #Insert a new user
        insert_user_query = """
                INSERT INTO users (
                        id,
                        access_token,
                        refresh_token
                    )
                VALUES (%s, %s, %s)"""
        cur.execute(insert_user_query, (
            result['user_id'],
            result['access_token'],
            result['refresh_token']
        ))

    cur.close()
    #Go back to the homepage
    return render_template('success.html')
