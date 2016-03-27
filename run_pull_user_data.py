import requests, psycopg2

conn = psycopg2.connect("dbname='dc7qf7cii79rie' password='9yuoOs84Nr7k-r3H7ioZxVzPoV' user='qhazfngzupdgdj' host='ec2-54-83-22-48.compute-1.amazonaws.com' port='5432'")
conn.autocommit = True

def get_user():

    authd_client = fitbit.Fitbit('227FD3', '5543280369ea955f96decf9e635c29f9',
                                 access_token='<access_token>', refresh_token='<refresh_token>')
    authd_client.sleep()
