import argparse


def parse_args():
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
    create_parser.add_argument(
        '--public', action='store_true', help='Set bucket ACL to public-read')

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
    upload_parser.add_argument(
        '--public', action='store_true', help='Make the uploaded public with ACL.')

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

    return parser.parse_args()
