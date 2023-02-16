from botocore.exceptions import ClientError
import boto3

def delete_bucket(s3, bucket_name: str):
    """
    Deletes an S3 bucket.

    :param s3: the boto3 s3 client
    :param bucket_name: The name of the bucket to delete.
    """
    try:
        # Empty the bucket before deletion
        s3_resource = boto3.resource('s3')
        bucket = s3_resource.Bucket(bucket_name)
        bucket.objects.all().delete()

        s3.delete_bucket(Bucket=bucket_name)
        print(f'Bucket {bucket_name} deleted successfully')
    except ClientError as e:
        print(f'Error deleting the bucket: {e}')
