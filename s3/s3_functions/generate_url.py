from botocore.exceptions import ClientError


def generate_url(s3, file_key: str, bucket_name: str, expiration: int = 3600):
    """
    Generates a pre-signed URL for an S3 object.

    :param s3: The Boto3 S3 client.
    :param file_key: The key of the object to generate the URL for.
    :param bucket_name: The name of the bucket that contains the object.
    :param expiration: The number of seconds until the URL expires (default 3600 seconds).
    :return: A pre-signed URL for the S3 object.
    """
    try:
        url = s3.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': file_key
            },
            ExpiresIn=expiration
        )
        print(url)
    except ClientError as e:
        print(f'Error generating URL: {e}')
