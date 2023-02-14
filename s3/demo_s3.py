import argparse
import boto3
from botocore.exceptions import NoCredentialsError

# Create an S3 client
s3 = boto3.client('s3')

# Define the argument parser
parser = argparse.ArgumentParser(description='Manage an S3 bucket')
subparsers = parser.add_subparsers(dest='subcommand', description='Subcommands')

# Subparser for creating a new bucket
create_parser = subparsers.add_parser('create-bucket', help='Create a new S3 bucket')
create_parser.add_argument('bucket_name', help='The name of the S3 bucket to create')
create_parser.add_argument('--region', help='The AWS region to use')

# Subparser for deleting a bucket
delete_parser = subparsers.add_parser('delete-bucket', help='Delete an S3 bucket')
delete_parser.add_argument('bucket_name', help='The name of the S3 bucket to delete')

# Subparser for uploading a file to a bucket
upload_parser = subparsers.add_parser('upload-file', help='Upload a file to an S3 bucket')
upload_parser.add_argument('file_path', help='The path to the file to upload')
upload_parser.add_argument('bucket_name', help='The name of the S3 bucket to upload the file to')
upload_parser.add_argument('--key', help='The S3 key to use for the uploaded file')

# Subparser for deleting a file from a bucket
delete_file_parser = subparsers.add_parser('delete-file', help='Delete a file from an S3 bucket')
delete_file_parser.add_argument('file_key', help='The S3 key of the file to delete')
delete_file_parser.add_argument('bucket_name', help='The name of the S3 bucket to delete the file from')

args = parser.parse_args()

# Define a function to get the region associated with the AWS profile
def get_profile_region():
    session = boto3.Session()
    return session.region_name

# Define the main function
def main():
    # Check which subcommand was selected
    if args.subcommand == 'create-bucket':
        # Set the region to use
        region = args.region or get_profile_region()
        # Create the bucket
        try:
            s3.create_bucket(Bucket=args.bucket_name, CreateBucketConfiguration={'LocationConstraint': region})
            print(f'Bucket {args.bucket_name} created successfully in region {region}')
        except NoCredentialsError:
            print('AWS credentials could not be found')

    elif args.subcommand == 'delete-bucket':
        # Delete the bucket
        try:
            s3.delete_bucket(Bucket=args.bucket_name)
            print(f'Bucket {args.bucket_name} deleted successfully')
        except NoCredentialsError:
            print('AWS credentials could not be found')

    elif args.subcommand == 'upload-file':
        # Set the S3 key to use
        key = args.key or args.file_path.split('/')[-1]
        # Upload the file
        try:
            s3.upload_file(args.file_path, args.bucket_name, key)
            print(f'File {args.file_path} uploaded successfully to bucket {args.bucket_name} with key {key}')
        except NoCredentialsError:
            print('AWS credentials could not be found')

    elif args.subcommand == 'delete-file':
        # Delete the file
        try:
            s3.delete_object(Bucket=args.bucket_name, Key=args.file_key)
            print(f'File {args.file_key} deleted successfully from bucket {args.bucket_name}')
        except NoCredentialsError:
            print('AWS credentials could not be found')

if __name__ == '__main__':
    main()
