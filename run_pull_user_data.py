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



    user_id = users[2][0]
    user_access_token = users[2][1]
    user_refresh_token = users[2][2]

    #Always refresh the token here so you don't run into authentication problems
    #reptar = fitbit.FitbitOauth2Client(clientId, clientSecret,
    #                             access_token=user_access_token, refresh_token=user_refresh_token)

#    reptar.refresh_token()
    authd_client = fitbit.Fitbit(clientId, clientSecret,
                                 access_token=user_access_token, refresh_token=user_refresh_token)


    URLBASE = URLBASE = "%s/%s/user" % (fitbit.Fitbit.API_ENDPOINT, fitbit.Fitbit.API_VERSION)
    resource = "activities"
    date = datetime.date(2016, 4, 22)
    user_id = user_id
    data = None
    url = URLBASE + "/%s/%s.json" % (user_id, resource)
    data = fitbit.Fitbit._COLLECTION_RESOURCE(authd_client, resource, date, user_id, data)
    print data

get_user()
