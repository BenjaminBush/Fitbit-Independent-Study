import requests, psycopg2

conn = psycopg2.connect("dbname='dc7qf7cii79rie' password='9yuoOs84Nr7k-r3H7ioZxVzPoV' user='qhazfngzupdgdj' host='ec2-54-83-22-48.compute-1.amazonaws.com' port='5432'")
conn.autocommit = True

def get_user():

    authd_client = fitbit.Fitbit('227FD3', '5543280369ea955f96decf9e635c29f9',
                                 access_token='<access_token>', refresh_token='<refresh_token>')
    authd_client.sleep()

    #Reptar

    cur = conn.cursor()
    #Get all of the information for a given user
    #for each user, send the request to get all activity data + sleep + hr and store it in the db
    #must make requst with access token as authorization header
    cur.execute("""
            SELECT * FROM users
        """)
    users = cur.fetchall()
    #For each user, get their data
    for(user in users){
        hr = requests.get('https://api.fitbit.com/1/user/'+user['id']+'/activities/heart/date/today/1d/1d/1sec/time/11:20/11:30.json', headers={'Authorization':user['access_token']})
        hr = hr.json();
        print(hr);
    }
