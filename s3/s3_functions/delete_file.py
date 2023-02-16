from botocore.exceptions import ClientError


def delete_file(s3, file_key: str, bucket_name: str):
    """
    Deletes a file from an S3 bucket.

    :param s3: the boto3 s3 client
    :param file_key: The key of the file to delete.
    :param bucket_name: The name of the bucket to delete the file from.
    """
    try:
        s3.delete_object(Bucket=bucket_name, Key=file_key)
        print(f'File {file_key} deleted successfully from bucket {bucket_name}')
    except ClientError as e:
        print(f'Error deleting the file: {e}')
