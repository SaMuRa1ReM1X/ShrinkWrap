import psycopg2
import json
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

iam = boto3.client('iam')

event = {
    'user_name': ''
}

def get_iam_usage(event):
    
    user_list = get_user_dao()
    print(user_list)

    for user_name in user_list:   
        print(user_name[0])
        response_1 = iam.generate_service_last_accessed_details(
            Arn='arn:aws:iam::132865025212:user/'+user_name[0]
        )
        
        print(response_1)
        response_dict = json.loads(json.dumps(response_1))
        
        response_2 = iam.get_service_last_accessed_details(
            JobId=response_dict['JobId']
        )

        response_2_dict = json.loads(json.dumps(response_2, default=str))
        
        if response_2_dict['ServicesLastAccessed']:
            svcs_last_accessed_list = response_2_dict['ServicesLastAccessed']
            print(svcs_last_accessed_list)
            for svcs_last_accessed in svcs_last_accessed_list:
                if svcs_last_accessed['TotalAuthenticatedEntities'] > 0:
                    update_last_accessed_dao(user_name,svcs_last_accessed['ServiceNamespace'],svcs_last_accessed['LastAuthenticated'])

    return "Successfully updated last accessed dates!!"


def update_last_accessed_dao(user_name, service, last_accessed):
    conn = None
    cur = None
    conn_string = ('dbname= user= password= host= port=')
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
    conn_string = ('dbname= user= password= host= port=')
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()
    cur.execute('select distinct user_name from usage_tracker')    
    response = cur.fetchall()
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
    return response


def lambda_handler(event, context):
    output = get_iam_usage(event)
    return output


if __name__ == "__main__":
    lambda_handler(event, None)
