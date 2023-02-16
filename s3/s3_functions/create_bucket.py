import boto3


def create_bucket(s3, bucket_name, region=None, is_public=False):
    """
    Creates an S3 bucket with the specified name.

    :param s3: the boto3 s3 client
    :param bucket_name: The name of the bucket to create.
    :param region: The AWS region in which to create the bucket. If not provided, the default region associated with the AWS profile will be used.
    :param is_public: Whether the bucket should be made public. If True, the ACL of the bucket will be set to allow public read access. Defaults to False.
    """
    location = {'LocationConstraint': region} if region else {}

    # Create the bucket
    s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)

    # Set public access
    if is_public:
        s3.put_bucket_acl(Bucket=bucket_name, ACL='public-read')

    print(f'Bucket {bucket_name} created successfully')
