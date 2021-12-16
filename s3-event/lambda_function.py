import boto3
import zipfile
import glob
import os

s3 = boto3.resource('s3')

def lambda_handler(event, context):
    for rec in event['Records']:
        filename = rec['s3']['object']['key']
        bucketname = rec['s3']['bucket']['name']

        zipfilename = '/tmp/' + filename + '.zip'

        bucket = s3.Bucket(bucketname)
        bucket.download_file(filename, "/tmp/"+filename)

        with zipfile.ZipFile(zipfilename, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.write("/tmp/"+filename)

        bucket = s3.Bucket("examplewrite00000000")
        bucket.upload_file(zipfilename, filename + '.zip')

        # コンテナの再利用に備えてtmpファイルを削除
        for p in glob.glob('/tmp/' + '*'):
            if os.path.isfile(p):
                os.remove(p)
