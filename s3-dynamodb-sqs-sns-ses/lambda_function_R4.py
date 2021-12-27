import json
import boto3


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("mailaddress")


def lambda_handler(event, context):
    for rec in event["Records"]:
        message = rec["Sns"]["Message"]
        data = json.loads(message)
        bounces = data["bounce"]["bouncedRecipients"]
        for b in bounces:
            email = b["emailAddress"]
            response = table.update_item(
                Key={"email": email},
                UpdateExpression="set haserror= :val",
                ExpressionAttributeValues={":val": 1}
            )
