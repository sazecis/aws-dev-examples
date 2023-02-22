import boto3

from s3_functions.create_bucket import create_bucket
from s3_functions.delete_bucket import delete_bucket
from s3_functions.upload_file import upload_file
from s3_functions.delete_file import delete_file
from s3_functions.generate_url import generate_url
from s3_functions.configure_bucket_website import configure_bucket_website

from arguments import parse_args

s3 = boto3.client('s3')


def get_profile_region():
    session = boto3.Session()
    return session.region_name

def main():
    # Parse command line arguments
    args = parse_args()
    # Define the switch statement as a dictionary
    switch = {
        'create-bucket': lambda: create_bucket(
            s3, args.bucket_name, region=(args.region or get_profile_region()), is_public=args.public),
        'delete-bucket': lambda: delete_bucket(s3, args.bucket_name),
        'upload-file': lambda: upload_file(
            s3, args.file_path, args.bucket_name, args.key, args.public),
        'delete-file': lambda: delete_file(s3, args.file_key, args.bucket_name),
        'generate-url': lambda: generate_url(
            s3, args.file_key, args.bucket_name, args.expiration),
        'web': lambda: configure_bucket_website(
            s3, args.bucket_name, args.index_document, args.error_document),
    }

    # Call the function associated with the selected subcommand
    switch[args.subcommand]()


if __name__ == '__main__':
    main()
