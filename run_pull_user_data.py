import requests, psycopg2, base64

conn = psycopg2.connect("dbname='dc7qf7cii79rie' password='9yuoOs84Nr7k-r3H7ioZxVzPoV' user='qhazfngzupdgdj' host='ec2-54-83-22-48.compute-1.amazonaws.com' port='5432'")
conn.autocommit = True

def get_user():

    authd_client = fitbit.Fitbit('227FD3', '5543280369ea955f96decf9e635c29f9',
                                 access_token='<access_token>', refresh_token='<refresh_token>')
    authd_client.sleep()


def example():
    cur = conn.cursor()
    cur.execute("""
        SELECT id, access_token, refresh_token FROM users
    """)
    ben = cur.fetchall()
    print(ben[0][0])
    print(ben[0][1])
    print(ben[0][2])

    url = 'https://api.fitbitcom/1/user/'+ben[0][0]+'/activities/date/[2016-03-19].json'

    hr = requests.get(url)
    import pdb; pdb.set_trace()
    #except requests.exceptions.RequestException as e:
    #    print(type(e))
    #    print(e)

example()
