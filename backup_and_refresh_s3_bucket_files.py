import os
from datetime import datetime

import boto3
from django.core.files import File

AWS_ACCESS_KEY_ID = 'XXXXXXXXXXXXXXXXXX'
AWS_SECRET_ACCESS_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

react_app_build_path = 'react-project/dist'

bucket_name = 'test-bucket'
# bucket_name = 'prod-bucket'
backup_dir = 'old-builds/' + str(datetime.now()).split('.')[0]

session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)
s3 = session.resource('s3')
bucket = s3.Bucket(bucket_name)

# backup Delete all old objects
for obj in bucket.objects.all():
    if obj.key.split('/')[0] != 'old-builds':
        bucket.copy({'Bucket': bucket_name, 'Key': obj.key}, os.path.join(backup_dir, obj.key))
        print(print('File backed', obj.key))
        obj.delete()
        print(print('File deleted'))


# upload

def get_content_type(file_name):
    ext = file_name.split('.')[-1]
    if ext == 'txt':
        return 'text/plain'
    elif ext == 'html':
        return 'text/html'
    elif ext == 'woff2':
        return 'font/woff2'
    elif ext == 'woff':
        return 'font/woff'
    elif ext == 'svg':
        return 'image/svg+xml'
    elif ext == 'png':
        return 'image/png'
    elif ext == 'js':
        return 'application/javascript'
    elif ext == 'json':
        return 'application/json'
    return 'binary/octet-stream'


for key in os.listdir(react_app_build_path):
    bucket.upload_file(os.path.join(react_app_build_path, key), key)
    local_file_path = os.path.join(react_app_build_path, key)
    bucket.put_object(Key=key, Body=File(open(local_file_path, 'rb')),
                      ACL='public-read', ContentType=get_content_type(key))
    print('File uploaded', key)

print("{} Files back-up and latest upload Success!!!!!!!!!!!!!!!!".format(bucket_name))
