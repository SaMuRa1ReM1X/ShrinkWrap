import boto3

client = boto3.client('lambda')

def invoke_lambda():
    response = client.invoke(
        FunctionName='GetLastAccessedFunction-Lambda',
        InvocationType='Event',
        LogType='Tail',
        ClientContext='TestApp',
        # Payload=b'bytes'|file,
        Qualifier='1'
    )
    print (response)

if __name__ == "__main__":
    invoke_lambda()