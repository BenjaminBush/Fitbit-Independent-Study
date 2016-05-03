import requests, psycopg2, base64, fitbit, datetime
#Connect to the databases using psycopg2
conn = psycopg2.connect("dbname='dc7qf7cii79rie' password='9yuoOs84Nr7k-r3H7ioZxVzPoV' user='qhazfngzupdgdj' host='ec2-54-83-22-48.compute-1.amazonaws.com' port='5432'")
conn.autocommit = True

def get_user():
    #Store the id and secret for future reference
    clientId = '227FD3'
    clientSecret = '5543280369ea955f96decf9e635c29f9'

    cur = conn.cursor()
    cur.execute("""
        SELECT id, access_token, refresh_token FROM users
    """)
    users = cur.fetchall()


    user_id = users[0][0]
    user_access_token = users[0][1]
    user_refresh_token = users[0][2]
    #Always refresh the token here so you don't run into authentication problems
    result = requests.post('https://api.fitbit.com/oauth2/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': user_refresh_token
    }, headers={
        'Authorization': b'Basic ' + base64.b64encode(('227FD3:5543280369ea955f96decf9e635c29f9').encode('utf8')),
        'Content-Type': 'application/x-www-form-urlencoded'
    })
    #Turn the result into JSON
    result = result.json()
    
    #Must store the new access + refresh tokens in the database since they are only good once

    cur.execute("""
            UPDATE users SET access_token = %s, refresh_token = %s WHERE id = %s
        """, (result['access_token'], result['refresh_token'], result['user_id']))

    #Get the updated information
    cur.execute("""
            SELECT id, access_token, refresh_token FROM users
        """)
    users = cur.fetchall()

    authd_client = fitbit.Fitbit(clientId, clientSecret,
                                 access_token=user_access_token, refresh_token=user_refresh_token)

    URLBASE = URLBASE = "%s/%s/user" % (fitbit.Fitbit.API_ENDPOINT, fitbit.Fitbit.API_VERSION)
    resource = "activities"
    date = datetime.date(2016, 4, 22)
    user_id = user_id
    data = None
    url = URLBASE + "/%s/%s.json" % (user_id, resource)
    data = fitbit.Fitbit._COLLECTION_RESOURCE(authd_client, resource, date, user_id, data)

    insert_user_query = """
            INSERT INTO loggables (
                    id,
                    distance,
                    caloriesOut,
                    floors,
                    steps,
                    restingHeartRate
                )
            VALUES (%s, %s, %s, %s, %s, %s)"""

    cur.execute(insert_user_query, (
        data['summary']['distances']['distance'],
        data['summary']['caloriesOut'],
        data['summary']['floors'],
        data['summary']['steps'],
        data['summary']['restingHeartRate']
    ))


get_user()
