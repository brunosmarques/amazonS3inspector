# Amazon SDK
import boto3

# Amazon SDK exceptions
from boto3.exceptions import botocore

# Arguments parsing utility
import argparse

# System library to exit to console
import sys

# others, for debug
import time, random

from datetime import datetime

def pretty_bytes(value):
    if args.unit == "kb":
        return '{:.2f} KB'.format(value/float(1<<10))

    if args.unit == "mb":
        return '{:.2f} MB'.format(value/float(1<<20))

    return "{} bytes".format(value)

def print_bucket(bucket):    
    if args.verbose:        
            print('\tRetreving files in bucket {}'.format(bucket.name), end='...', flush=True)

    files = bucket.objects.all()
    # time.sleep(random.randrange(1,4))

    if args.verbose:        
            print('done')

    total_files_size = 0
    files_count = len(list(files))
    last_modified_file = datetime(1900, 9, 1).replace(tzinfo=None)
    storage_types = {}

    for file in files: 
        # print(file.key, '{:,.0f}'.format(file.size/float(1<<20))+' MB') #, file.last_modified)
        total_files_size+=file.size

        last_change = file.last_modified.replace(tzinfo=None)
        if last_modified_file < last_change:
            last_modified_file = last_change
        
        if (file.storage_class in storage_types): 
            storage_types[file.storage_class] += 1
        else: 
            storage_types[file.storage_class] = 1
        # storage_types[file.storage_class] = storage_types[file.storage_class] + 1
        
        # obj.last_modified

    print("Bucket name:{}".format(bucket.name))
    # print("Bucket location:{}".format(bucket.))
    print("Total file size: {}".format(pretty_bytes(total_files_size)))
    print("Number of files: {}".format(files_count))
    print("Last modified file: {}".format(last_modified_file))
    print("Bucket creation date: {}".format(bucket.creation_date))
    print("Storage type: {}".format(storage_types))
    

def print_buckets_info(buckets):
    for bucket in buckets:
        print("Bucket name:{}\nBucket creation date:{}".format(bucket.name, bucket.creation_date))

def get_buckets(s3):
    if args.bucket:
        return [ s3.Bucket(args.bucket) ]
    return s3.buckets.all()

def get_y_n(text):
    valid_answers = [ 'y','n','Y','N', '' ]
    while True:
        data = input(text)
        if data not in valid_answers:
            continue
        elif data=='y' or data=='Y':
            return True
        else:
            return False

def main():
    try:
        s3 = boto3.resource('s3')
        client = boto3.client('s3')

        buckets =  get_buckets(s3)
        buckets_count = len(list(buckets))

        # print_bucket
        # s_info(buckets)

        if args.verbose:        
            print('{} buckets found'.format(buckets_count))

        if buckets_count > HIGH_BUCKETS_COUNT_WARNING:
            allowed = get_y_n("WARNING: high number of buckets found, may take sometime to get all data. Continue (y/N)?")
            if not(allowed):
                sys.exit()
    
        for bucket in buckets:  
            response = client.get_bucket_location( Bucket=bucket.name )
            bucket_location = response['LocationConstraint']
            print("Bucket location: {}".format(bucket_location))

            print_bucket(bucket)
         

    except botocore.exceptions.NoCredentialsError:
        print("Sorry, I can't find your credentials.")
    except botocore.exceptions.ClientError as e:
        print("Client error, see details below:\n {}".format(e))
    except Exception as e:
        print("Unexpected error occoured, more details bellow\n{}".format(e))


def parsearguments():        
    # initiate the parser
    parser = argparse.ArgumentParser()

    help_text = 'This tool returns information from AWS S3 buckets in a Amazon account'
    parser = argparse.ArgumentParser(description = help_text)

    # add long and short argument
    # parser.add_argument("--filter", "-f", help="Filter results by a given string")
    
    # add long and short argument
    parser.add_argument("--verbose", "-v", help="Verbose mode", action="store_true")
    
    # add long and short argument
    parser.add_argument("--bucket", "-b", help="Bucket name" )

    parser.add_argument("--unit", "-u", help="unit")
    
    # read arguments from the command line
    return parser.parse_args()

    # check for --xxx

HIGH_BUCKETS_COUNT_WARNING = 100
args = parsearguments()
main()

# ---------------------------------------------------------------------------
# other code bellow
print("\nThis is the end, my only friend, the end...")

# asyncio.run(main())

# async def get_files(bucket):
#     print('{} requested files\n'.format(bucket.name))

    # files = bucket.objects.all()
    # for file in files:
    #     print(file.key, '{:,.0f}'.format(file.size/float(1<<20))+' MB') #, file.last_modified)


# async def get_files(bucket):
#     async for i in bucket.objects.all():
#         print(i.key)

# async def get_buckets():
#     for i in s3.buckets.all():
#         yield i

# async def main():
#     buckets = s3.buckets.all()
    
#     async for bucket in get_buckets():
#         print(bucket.name)
#         # get_files(bucket)

#         files = bucket.objects.all()
#         for file in files:
#             print(file.key, '{:,.0f}'.format(file.size/float(1<<20))+' MB') #, file.last_modified)
#         # print()

# loop = asyncio.get_event_loop()
# try:
#     loop.run_until_complete(main())
# finally:
#     loop.close()

    # print("Listing all buckets")

    # buckets = s3.buckets.all()


    # for bucket in buckets:
    #     files = bucket.objects.all()

    #     print('{} has {} files'.format(bucket.name, len(list(files))))
        
    #     for obj in files:
    #         print(obj.key, '{:,.0f}'.format(obj.size/float(1<<20))+' MB', obj.last_modified)
    #         # print(dir(obj))
    #     print('')

# except botocore.exceptions.NoCredentialsError:
#     print("Sorry, I can't find your credentials.")
# except botocore.exceptions.ClientError:
#     print("Your credentials are invalid, please check your credentials file (~/.aws/credentials)")

# except Exception as e:
#     print("Unexpected error occoured, can't list buckets right now\n{}".format(e))

# client = boto3.client('ce')

# response = client.get_cost_and_usage(TimePeriod={
#         'Start': '2019-09-01 00:00:00',
#         'End': '2019-09-14 00:00:00'
#     }
# )

# print(response)

    # bucket1 = s3.Bucket('brunomarques2')
    # print(bucket1.name)


# async def get_files(bucket):
#     # asyncio.sleep(random.randint(0,5))
#     await asyncio.sleep(2)
#     print(bucket)
#     files = bucket.objects.all()

#     # for file in files:
#     #     print(file.key, '{:,.0f}'.format(file.size/float(1<<20))+' MB') #, file.last_modified)

# async def main():
#     tasks = []

#     for bucket in s3.buckets.all():
#         tasks.append(asyncio.create_task(get_files(bucket)))

#     # print(tasks)

#     for task in tasks:
#         await task