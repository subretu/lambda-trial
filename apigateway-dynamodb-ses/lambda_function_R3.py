import json
import urllib.parse
import boto3
import time
import decimal


dynamodb = boto3.resource("dynamodb")

# 送信元アドレス
MAILFROM = 'xxxxxx'


def sendmail(to, subject, body):
    client = boto3.client('ses')

    response = client.send_email(
        Source=MAILFROM,
        ReplyToAddresses=[MAILFROM],
        Destination={
            # 宛先アドレス
            'ToAddresses': [
                'yyyyyy'
            ]
        },
        Message={
            'Subject': {
                'Data': subject,
                'Charset': 'UTF-8'
            },
            'Body': {
                'Text': {
                    'Data': body,
                    'Charset': 'UTF-8'
                }
            }
        }
    )


def next_seq(table, tablename):
    response = table.update_item(
        Key={"tablename": tablename},
        UpdateExpression="set seq = seq + :val",
        ExpressionAttributeValues={":val": 1},
        ReturnValues="UPDATED_NEW",
    )

    return response["Attributes"]["seq"]


def lambda_handler(event, context):
    try:
        seqtable = dynamodb.Table("sequence")
        nextseq = next_seq(seqtable, "user")

        param = urllib.parse.parse_qs(event["body"])

        username = param["username"][0]
        email = param["email"][0]
        host = event["requestContext"]["identity"]["sourceIp"]
        now = time.time()

        s3 = boto3.client("s3")
        url = s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": "lambda-secret-test", "Key": "Earth.png"},
            ExpiresIn=48 * 24 * 60 * 60,
            HttpMethod="GET",
        )

        usertable = dynamodb.Table("user")
        usertable.put_item(
            Item={
                "id": nextseq,
                "username": username,
                "email": email,
                "accepted_at": decimal.Decimal(str(now)),
                "host": host,
                "url": url,
            }
        )

        mailbody = """
        {0}様

        ご登録ありがとうございました。
        下記のURLからダウンロードできます。

        {1}
        """.format(username, url)

        sendmail(email, "登録ありがとうございました", mailbody)

        return {
            "statusCode": 200,
            "headers": {"content-type": "text/html"},
            "body": '<!DOCTYPE html><html><head><meta charset="UTF-8"></head><body>登録ありがとうございました。</body></html>',
        }
    except:
        import traceback

        traceback.print_exc()

        return {
            "statusCode": 500,
            "headers": {"content-type": "text/html"},
            "body": '<!DOCTYPE html><html><head><meta charset="UTF-8"></head><body>内部エラーが発生しました。</body></html>',
        }
