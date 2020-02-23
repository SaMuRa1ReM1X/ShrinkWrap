import psycopg2


def update_last_accessed_dao(user_name, service, last_accessed):
    conn = None
    cur = None
    conn_string = ('dbname=dev user=awsuser password=awsPDXhackathon1 host=aws-pdx-hackathon.c8vcduzakdyw.us-west-2.redshift.amazonaws.com port=5439')
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()
    cur.execute('update usage_tracker set last_use_date = %s where user_name = %s and service = %s',(last_accessed,user_name,service,))
    conn.commit()
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()


def get_user_dao():
    conn = None
    cur = None
    conn_string = ('dbname=dev user=awsuser password=awsPDXhackathon1 host=aws-pdx-hackathon.c8vcduzakdyw.us-west-2.redshift.amazonaws.com port=5439')
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()
    cur.execute('select distinct user_name from usage_tracker')    
    response = cur.fetchall()
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
    return response