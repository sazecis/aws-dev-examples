import os
import boto3
from botocore.exceptions import ClientError
from boto3.s3.transfer import TransferConfig


def upload_file(s3, file_path, bucket_name, key=None, public=False):
    """
    Uploads a file or folder to an S3 bucket.

    :param s3: the boto3 s3 client
    :param file_path: The path to the file or folder to upload.
    :param bucket_name: The name of the S3 bucket to upload the file to.
    :param key: The S3 key to use for the uploaded file. Uploading folders will use the name of the files as keys.
    :param public: Make the uploaded public with ACL.
    """
    # Determine whether the path is a file or a directory
    if os.path.isfile(file_path):
        # Upload the file
        try:
            s3.upload_file(
                file_path,
                bucket_name,
                key or os.path.basename(file_path),
                ExtraArgs={'ContentType': 'text/html'}
            )
            if public:
                # Make the object publicly accessible
                s3.put_object_acl(ACL='public-read', 
                    Bucket=bucket_name, Key=key or os.path.basename(file_path))
            print(
                f'File {file_path} uploaded successfully to bucket {bucket_name}')
        except ClientError as e:
            print(f'Error uploading the file: {e}')
    elif os.path.isdir(file_path):
        # Traverse the directory and upload each file
        for dirpath, dirnames, filenames in os.walk(file_path):
            for filename in filenames:
                try:
                    _, extension = os.path.splitext(filename)
                    if extension == '.css':
                        content_type = {'ContentType': 'text/css'}
                    else:
                        content_type = {'ContentType': 'text/html'}
                    file_path = os.path.join(dirpath, filename)
                    dir_path = '/'.join(dirpath.split('\\')[1:])
                    if dir_path:
                        s3_file_path = '/'.join([dir_path, filename])
                    else:
                        s3_file_path = filename
                    s3.upload_file(
                        file_path,
                        bucket_name,
                        s3_file_path,
                        ExtraArgs=content_type
                    )

                    s3.put_object_acl(ACL='public-read',
                                      Bucket=bucket_name, Key=s3_file_path)
                    print(
                        f'File {file_path} uploaded successfully to bucket {bucket_name} with key: {s3_file_path}')
                except ClientError as e:
                    print(f'Error uploading the file: {e}')
    else:
        print(f'{file_path} is not a valid file or directory')
