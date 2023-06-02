import json


def create_bucket(s3, bucket_name, region=None, is_public=False):
    """
    Creates an S3 bucket with the specified name.

    :param s3: the boto3 s3 client
    :param bucket_name: The name of the bucket to create.
    :param region: The AWS region in which to create the bucket. If not provided, the default region associated with the AWS profile will be used.
    :param is_public: Whether the bucket should be made public. If True, a bucket policy allowing public read access will be applied, and Block Public Access settings will be disabled. Defaults to False.
    """
    location = {'LocationConstraint': region} if region else {}

    # Create the bucket
    s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)

    # Set public access
    if is_public:
        # Disable Block Public Access settings
        s3.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': False,
                'IgnorePublicAcls': False,
                'BlockPublicPolicy': False,
                'RestrictPublicBuckets': False
            }
        )

        # Create bucket policy for public access
        policy = {
            "Version": "2012-10-17",
            "Statement": [{
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": ["s3:GetObject"],
                "Resource":["arn:aws:s3:::%s/*" % bucket_name]
            }]
        }

        policy = json.dumps(policy)

        s3.put_bucket_policy(Bucket=bucket_name, Policy=policy)

    print(f'Bucket {bucket_name} created successfully')
