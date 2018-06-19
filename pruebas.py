
import boto3

s3 = boto3.client('s3')

try:
    s3.create_bucket(
        Bucket='face-recognition'
    )
# except BucketAlreadyExists as ex:
#     pass
except Exception as ex:
    print(str(ex))


