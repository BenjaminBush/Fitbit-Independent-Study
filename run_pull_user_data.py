import requests, psycopg2, base64, fitbit, datetime
#Connect to the databases using psycopg2
conn = psycopg2.connect("dbname='dc7qf7cii79rie' password='9yuoOs84Nr7k-r3H7ioZxVzPoV' user='qhazfngzupdgdj' host='ec2-54-83-22-48.compute-1.amazonaws.com' port='5432'")
conn.autocommit = True

# def revoke_access():
#     clientId = '227FD3'
#     clientSecret = '5543280369ea955f96decf9e635c29f9'
#     cur = conn.cursor()
#     cur.execute("""
#         SELECT id, access_token, refresh_token FROM users
#     """)
#     users = cur.fetchall()
#
#     access_token = users[1][1]
#
#     result = requests.post('https://api.fitbit.com/oauth2/revoke', data={
#         'token': access_token
#     }, headers={
#         'Authorization': b'Basic ' + base64.b64encode(('227FD3:5543280369ea955f96decf9e635c29f9').encode('utf8')),
#         'Content-Type': 'application/x-www-form-urlencoded'
#     })
#
#     print result


def get_user():
    #Store the id and secret for future reference
    clientId = '227FD3'
    clientSecret = '5543280369ea955f96decf9e635c29f9'

    cur = conn.cursor()
    cur.execute("""
        SELECT id, access_token, refresh_token FROM users
    """)
    users = cur.fetchall()


    user_id = users[1][0]
    user_access_token = users[1][1]
    user_refresh_token = users[1][2]

    #Use the api to get the resources
    authd_client = fitbit.Fitbit(clientId, clientSecret,
                                 access_token=user_access_token, refresh_token=user_refresh_token)


    #Refresh the token here just so we don't run into any problems
    token = authd_client.client.refresh_token()
    user_access_token = token['access_token']
    user_refresh_token = token['refresh_token']

    cur.execute("""
            UPDATE users SET access_token = %s, refresh_token = %s WHERE id = %s
        """, user_access_token, user_refresh_token, user_id)

    #Make the request
    URLBASE = URLBASE = "%s/%s/user" % (fitbit.Fitbit.API_ENDPOINT, fitbit.Fitbit.API_VERSION)
    resource = "activities"
    date = datetime.datetime.today().strftime("%Y-%m-%d")
    user_id = user_id
    data = None
    url = URLBASE + "/%s/%s.json" % (user_id, resource)
    data = fitbit.Fitbit._COLLECTION_RESOURCE(authd_client, resource, date, user_id, data)

    #Store the important data in local variables
    distance = data['summary']['distances'][1]['distance']
    floors = data['summary']['floors']
    steps = data['summary']['steps']
    calsout = data['summary']['caloriesOut']

    try:
        restinghr = data['summary']['restingHeartRate']
    except KeyError:
        restinghr = 0

    #Create the query
    insert_user_query = """
            INSERT INTO loggables (
                    id,
                    distance,
                    floors,
                    steps,
                    restinghr,
                    calsout,
                    day
                )
            VALUES (%s, %s, %s, %s, %s, %s, %s)"""

    #Insert into the table
    cur.execute(insert_user_query, (
        user_id,
        distance,
        floors,
        steps,
        restinghr,
        calsout,
        date
    ))

#Call the function!
get_user()
