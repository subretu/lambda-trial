import json
import urllib.parse
import boto3
import time
import decimal


dynamodb = boto3.resource("dynamodb")


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

        usertable = dynamodb.Table("user")
        usertable.put_item(
            Item={
                "id": nextseq,
                "username": username,
                "email": email,
                "accepted_at": decimal.Decimal(str(now)),
                "host": host,
            }
        )

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
            "body": '<!DOCTYPE html><html><head><meta charset="UTF-8"></head><body内部エラーが発生しました。</body></html>',
        }
