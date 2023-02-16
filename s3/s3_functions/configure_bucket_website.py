from botocore.exceptions import ClientError


def configure_bucket_website(s3, bucket_name: str, index_document: str, error_document: str = None):
    """
    Configures an S3 bucket as a website.

    :param s3: the boto3 s3 client
    :param bucket_name: the name of the bucket to configure
    :param index_document: the name of the index document
    :param error_document: the name of the error document, if any
    """
    website_config = {
        'IndexDocument': {'Suffix': index_document},
        'ErrorDocument': {'Key': error_document} if error_document else {}
    }

    try:
        s3.put_bucket_website(Bucket=bucket_name,
                              WebsiteConfiguration=website_config)
        print(f'Bucket {bucket_name} is now configured as a website')

        # Print the URL of the website
        url = f'http://{bucket_name}.s3-website.{s3.meta.region_name}.amazonaws.com'
        print(f'Website URL: {url}')
    except ClientError as e:
        print(f'Error configuring the bucket as a website: {e}')
