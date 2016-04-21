import requests, psycopg2, base64, fitbit, datetime

conn = psycopg2.connect("dbname='dc7qf7cii79rie' password='9yuoOs84Nr7k-r3H7ioZxVzPoV' user='qhazfngzupdgdj' host='ec2-54-83-22-48.compute-1.amazonaws.com' port='5432'")
conn.autocommit = True

def get_user():

    cur = conn.cursor()
    cur.execute("""
        SELECT id, access_token, refresh_token FROM users
    """)
    ben = cur.fetchall()

    ben_id = ben[0][0]
    ben_access_token = ben[0][1]
    ben_refresh_token = ben[0][2]

    authd_client = fitbit.Fitbit('227FD3', '5543280369ea955f96decf9e635c29f9',
                                 access_token=ben_access_token, refresh_token=ben_refresh_token)

    #Always refresh the token here so you don't run into authentication problems

    URLBASE = URLBASE = "%s/%s/user" % (fitbit.Fitbit.API_ENDPOINT, fitbit.Fitbit.API_VERSION)

    resource = "activities"
    date = datetime.date(2016, 4, 20)
    user_id = ben_id
    data = None
    url = URLBASE + "/%s/%s.json" % (user_id, resource)

    hr = fitbit.Fitbit._COLLECTION_RESOURCE(authd_client, resource, date, user_id, data)
     #self.common_api_test('_COLLECTION_RESOURCE', (resource, date, user_id, data), {}, (url), {})

    #url = 'https://api.fitbitcom/1/user/'+ben[0][0]+'/activities/date/[2016-03-19].json'
    #today = datetime.date
    #hr = fitbit._COLLECTION_RESOURCE
    #hr = fitbit.heart(date=today, user_id=ben[0][0], data=None)

    import pdb; pdb.set_trace()
    #except requests.exceptions.RequestException as e:
    #    print(type(e))
    #    print(e)

get_user()
