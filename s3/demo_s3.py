import argparse
import os
import boto3
from botocore.exceptions import ClientError
from boto3.s3.transfer import TransferConfig


# Create an S3 client
s3 = boto3.client('s3')

# Define the argument parser
parser = argparse.ArgumentParser(description='Manage an S3 bucket')
subparsers = parser.add_subparsers(
    dest='subcommand', description='Subcommands')

# Subparser for creating a new bucket
create_parser = subparsers.add_parser(
    'create-bucket', help='Create a new S3 bucket')
create_parser.add_argument(
    'bucket_name', help='The name of the S3 bucket to create')
create_parser.add_argument('--region', help='The AWS region to use')

# Subparser for deleting a bucket
delete_parser = subparsers.add_parser(
    'delete-bucket', help='Delete an S3 bucket')
delete_parser.add_argument(
    'bucket_name', help='The name of the S3 bucket to delete')

# Subparser for uploading a file to a bucket
upload_parser = subparsers.add_parser(
    'upload-file', help='Upload a file or folder to an S3 bucket')
upload_parser.add_argument(
    'file_path', help='The path to the file or folder to upload')
upload_parser.add_argument(
    'bucket_name', help='The name of the S3 bucket to upload the file to')
upload_parser.add_argument(
    '--key', help='The S3 key to use for the uploaded file. Uploading folders will use the name of the files as keys.')

# Subparser for deleting a file from a bucket
delete_file_parser = subparsers.add_parser(
    'delete-file', help='Delete a file from an S3 bucket')
delete_file_parser.add_argument(
    'file_key', help='The S3 key of the file to delete')
delete_file_parser.add_argument(
    'bucket_name', help='The name of the S3 bucket to delete the file from')

# Subparser for generating a presigned URL for a file in a bucket
url_parser = subparsers.add_parser(
    'generate-url', help='Generate a presigned URL for a file in an S3 bucket')
url_parser.add_argument(
    'file_key', help='The S3 key of the file to generate the URL for')
url_parser.add_argument(
    'bucket_name', help='The name of the S3 bucket containing the file')
url_parser.add_argument(
    '--expiration', help='The expiration time for the URL, in seconds')

# Subparser for configuring a bucket as a website
web_parser = subparsers.add_parser(
    'web', help='Configure an S3 bucket as a website')
web_parser.add_argument(
    'bucket_name', help='The name of the S3 bucket to configure as a website')
web_parser.add_argument(
    'index_document', help='The name of the index document')
web_parser.add_argument(
    '--error-document', help='The name of the error document')

args = parser.parse_args()

# Define a function to get the region associated with the AWS profile


def get_profile_region():
    session = boto3.Session()
    return session.region_name


def main():
    # Check which subcommand was selected
    if args.subcommand == 'create-bucket':
        # Set the region to use
        region = args.region or get_profile_region()
        # Create the bucket
        try:
            s3.create_bucket(Bucket=args.bucket_name, CreateBucketConfiguration={
                             'LocationConstraint': region})
            print(
                f'Bucket {args.bucket_name} created successfully in region {region}')
        except ClientError as e:
            print(f'Error creating the bucket: {e}')

    elif args.subcommand == 'delete-bucket':
        # Delete the bucket
        try:
            s3.delete_bucket(Bucket=args.bucket_name)
            print(f'Bucket {args.bucket_name} deleted successfully')
        except ClientError as e:
            print(f'Error deleting the bucket: {e}')


    elif args.subcommand == 'upload-file':
        path = args.file_path
        # Determine whether the path is a file or a directory
        if os.path.isfile(path):
            # Upload the file
            try:
                s3.upload_file(
                    path,
                    args.bucket_name,
                    os.path.basename(path)
                )
                print(
                    f'File {path} uploaded successfully to bucket {args.bucket_name}')
            except ClientError as e:
                print(f'Error uploading the file: {e}')
        elif os.path.isdir(path):
            # Traverse the directory and upload each file
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    try:
                        file_path = os.path.join(dirpath, filename)
                        s3.upload_file(
                            file_path,
                            args.bucket_name,
                            os.path.relpath(file_path, path)
                        )
                        print(
                            f'File {file_path} uploaded successfully to bucket {args.bucket_name}')
                    except ClientError as e:
                        print(f'Error uploading the file: {e}')
        else:
            print(f'{path} is not a valid file or directory')

    elif args.subcommand == 'delete-file':
        # Delete the file
        try:
            s3.delete_object(Bucket=args.bucket_name, Key=args.file_key)
            print(
                f'File {args.file_key} deleted successfully from bucket {args.bucket_name}')
        except ClientError as e:
            print(f'Error deleting the file: {e}')

    elif args.subcommand == 'generate-url':
        # Generate a presigned URL
        try:
            url = s3.generate_presigned_url(
                ClientMethod='get_object',
                Params={'Bucket': args.bucket_name, 'Key': args.file_key},
                ExpiresIn=args.expiration
            )
            print(
                f'Presigned URL for file {args.file_key} in bucket {args.bucket_name}:')
            print(url)
        except ClientError as e:
            if e.response['Error']['Code'] == 'ExpiredToken':
                print('Error: AWS token has expired')
            else:
                print(f'Error: {e}')


if __name__ == '__main__':
    main()
