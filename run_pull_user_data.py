import requests, psycopg2, base64, fitbit, datetime, json
#Connect to the databases using psycopg2
conn = psycopg2.connect("dbname='dc7qf7cii79rie' password='9yuoOs84Nr7k-r3H7ioZxVzPoV' user='qhazfngzupdgdj' host='ec2-54-83-22-48.compute-1.amazonaws.com' port='5432'")
conn.autocommit = True

def get_user():
    #Store the id and secret for future reference
    clientId = '227FD3'
    clientSecret = '5543280369ea955f96decf9e635c29f9'
    #Connect to the database and get all user information
    cur = conn.cursor()
    cur.execute("""
        SELECT id, access_token, refresh_token FROM users
    """)
    users = cur.fetchall()
    #Iterate over each user in the databae
    for user in users:
        user_id = user[0]
        user_access_token = user[1]
        user_refresh_token = user[2]

        #Use the api to get the resources
        authd_client = fitbit.Fitbit(clientId, clientSecret,
                                     access_token=user_access_token, refresh_token=user_refresh_token)


        #Refresh the token here just so we don't run into any problems (every time)
        result = requests.post('https://api.fitbit.com/oauth2/token', data={
            'grant_type': 'refresh_token',
            'refresh_token': user_refresh_token
        }, headers={
            'Authorization': b'Basic ' + base64.b64encode(('227FD3:5543280369ea955f96decf9e635c29f9').encode('utf8')),
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        #JSONify the response
        json_response = json.loads(result.content)

        #If errors exist, fail. Otherwise continue
        #Note: if one user fails, the app will continue to execute for other users!
        if 'errors' in json_response:
            print(user_id + ': failed miserably')
        else:
            #Update the database with the new tokens
            user_access_token = json_response['access_token']
            user_refresh_token = json_response['refresh_token']
            cur.execute("""
                    UPDATE users SET access_token = %s, refresh_token = %s WHERE id = %s
                """, (user_access_token, user_refresh_token, user_id))


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
            #Check to see if there is hr data
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
    #Close connection to the database
    cur.close()


#Call the function!
get_user()
