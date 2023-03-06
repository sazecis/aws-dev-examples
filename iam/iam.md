# Managing users using AWS CLI and Windows Batch

This section covers creating and managing IAM users. For IAM I used simple **AWS CLI** commands embeded into Windows **batch** scripts.

## Creating a user

To create a new IAM user, follow these steps:

1. Change directory to the **iam** directory.
```
cd iam
```

2. Run the `create-user.bat` script and specify a username for the new user. For example:
```
create-user.bat john.doe
```

This will create a new IAM user with the specified username and permissions taken from `bookshelf-policy.json` and will also create the credentials needed to access AWS services programatically.
The credentials are created and a profile is also created in **.aws** directory of your **User** directory.

## Deleting a user

If you are building the whole application then **skip** this step and do it only at the end. This user shall be used to deploy the following services.

To delete an IAM user, follow these steps:

1. Change directory to the **iam** directory.
```
cd iam
```

2. Run the `delete-user.bat` script and specify the username of the user you want to delete. For example:
```
delete-user.bat john.doe
```
This will delete the IAM user with the specified username and the related credentials and profile.

## Switch to the created user

Using the AWS CLI switch to the created user. You can easily do that by setting the **AWS_PROFILE** environment variable.
```
set AWS_PROFILE=john.doe
```
Check if everything is set up correctly:
```
aws sts get-caller-identity
```
You should see the john.doe user as the active user.

