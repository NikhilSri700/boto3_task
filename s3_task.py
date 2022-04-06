import boto3
import os

'''
Globally creating aws session and two s3 console using both client and resource
'''
session = boto3.session.Session(
    profile_name='nikhil', region_name='ap-south-1')
s3_console_resource = session.resource(service_name='s3')
s3_console_client = session.client(service_name='s3')
bucket_name = 'training-wg-cloud-ir-my-bucket-test'


# Function for creating creating a s3 bucket
def create_s3_bucket():
    global bucket_name
    name = input("Enter your name: ")
    bucket_name = 'training-wg-cloud-ir-my-bucket-' + name
    try:
        s3_console_resource.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': 'ap-south-1'
            }
        )
        print(f"Bucket Created with bucket name as - {bucket_name}")
    except Exception as error:
        print(error)


# Function for enabling bucket versioning in s3
def enable_bucket_verisoning():
    try:
        s3_console_client.put_bucket_versioning(
            Bucket=bucket_name,
            VersioningConfiguration={
                'Status': 'Enabled'
            }
        )
        print("Bucket Versioning Enabled")
    except Exception as error:
        print(error)


# Function for suspending bucket versioning in s3
def suspend_bucket_verisoning():
    try:
        s3_console_client.put_bucket_versioning(
            Bucket=bucket_name,
            VersioningConfiguration={
                'Status': 'Suspended'
            }
        )
        print("Bucket Versioning Suspended")
    except Exception as error:
        print(error)


# Function will create a bucket key and put 2500 object in it at once
def create_folder_and_put_object():
    original_name = 'sample'
    s3_folder_path = 'images/'
    s3_bucket = s3_console_resource.Bucket(bucket_name)
    temp_name = original_name
    for counter in range(2500):
        new_name = original_name + str(counter)
        response = s3_bucket.upload_file(temp_name + '.jpg', s3_folder_path + temp_name + '.jpg')
        os.rename(temp_name + '.jpg', new_name + '.jpg')
        temp_name = new_name

    os.rename(temp_name + '.jpg', original_name + '.jpg')


# Function for retrieving all the objects from s3 bucket at a time using pagination
def retrieve_all_objects():
    paginator = s3_console_client.get_paginator('list_objects')
    cnt = 1
    for each_page in paginator.paginate(Bucket=bucket_name):
        for each_object in each_page.get('Contents'):
            print(cnt, each_object.get('Key'))
            cnt += 1


# Function will delete all the objects from the bucket
def empty_bucket():
    s3_bucket = s3_console_resource.Bucket(bucket_name)
    try:
        s3_bucket.objects.all().delete()
        print("All objects are deleted from the bucket")
    except Exception as error:
        print(error)


# Function for deleting the s3 bucket
def delete_bucket():
    try:
        s3_console_client.delete_bucket(Bucket=bucket_name)
        print("Bucket delelted")
    except Exception as error:
        print(error)


print("\n\t\t *** Welcome! Lets Interact with AWS S3 using boto3 *** ")
while True:
    print('''
1. Create a bucket.
2. Enable bucket versioning.
3. Suspend bucket versioning.
4. Create images folder and put images in it.
5. Retrieve all images.
6. Empty the bucket.
7. Delete the bucket.
8. Exit.
''')
    user_input = int(input("Choose an option: "))
    print('')

    if user_input == 1:
        create_s3_bucket()
    elif user_input == 2:
        enable_bucket_verisoning()
    elif user_input == 3:
        suspend_bucket_verisoning()
    elif user_input == 4:
        create_folder_and_put_object()
    elif user_input == 5:
        retrieve_all_objects()
    elif user_input == 6:
        empty_bucket()
    elif user_input == 7:
        delete_bucket()
    elif user_input == 8:
        print("Thank You, Bye!")
        exit()
    else:
        print("Wrong option!")
