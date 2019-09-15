# Amazon SDK
import boto3

# Amazon SDK exceptions
from boto3.exceptions import botocore

# Arguments parsing utility
import argparse

# System library to exit to console
import sys

# Datetime
from datetime import datetime

# Pandas for dataframe
import pandas as pd

class cBucket:
    def __init__(self, name):
        self.name = name
        self.creation_date = datetime(1, 1, 1).replace(tzinfo=None)
        self.files_count = 0
        self.files_size = 0
        self.last_modified = 0
        self.storage_types = {}
        self.cost = 0
        self.region = ''

# def pretty_bytes(value): #TODO
#     if args.unit == "kb":
#         return '{:.2f} KB'.format(value/float(1<<10))

#     if args.unit == "mb":
#         return '{:.2f} MB'.format(value/float(1<<20))

def format_size(value):
    bit_shift = {"B": 0,
            "kb": 7,
            "KB": 10,
            "mb": 17,
            "MB": 20,
            "gb": 27,
            "GB": 30,
            "TB": 40,}
    if args.unit in bit_shift:
        return "{:,.0f} {}".format(value / float(1 << bit_shift[args.unit]),args.unit) 
    return "{} bytes".format(value)

def print_buckets(buckets):
    data = []
    names = []

    for bucket in buckets:
        d = [            
            bucket.region,
            bucket.creation_date,
            bucket.files_count,
            format_size(bucket.files_size),
            bucket.last_modified,
            bucket.cost ]
        data.append(d)
        names.append(bucket.name)

    features = ["Region", "Creation Date", "Files", "Size", "Last modified", "Cost"]
    dataframe = pd.DataFrame(data=data,columns=features,index=names)

    if args.group:
        grouped_dataframe = dataframe.groupby('Region').sum()
        print(grouped_dataframe)
    else:
        print(dataframe)
    
def get_bucket_details(bucket):    
    if args.verbose:        
            print('\tRetreving files in bucket {}'.format(bucket.name), end='...', flush=True)
    files = bucket.objects.all()
    if args.verbose:        
            print('done')
    
    last_modified_file = datetime(1, 1, 1).replace(tzinfo=None)
    total_files_size = 0
    storage_types = {}

    for file in files: 
        total_files_size+=file.size

        last_change = file.last_modified.replace(tzinfo=None)
        if last_modified_file < last_change or last_modified_file=='':
            last_modified_file = last_change
        
        if (file.storage_class in storage_types): 
            storage_types[file.storage_class] += 1
        else: 
            storage_types[file.storage_class] = 1

    location_response = client.get_bucket_location( Bucket=bucket.name )
        
    coveo_bucket = cBucket(bucket.name)
    coveo_bucket.creation_date = bucket.creation_date.replace(tzinfo=None)
    coveo_bucket.files_count = len(list(files))
    coveo_bucket.files_size = total_files_size
    coveo_bucket.last_modified = last_modified_file
    coveo_bucket.storage_types = storage_types   
    coveo_bucket.region = location_response['LocationConstraint']

    return coveo_bucket

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

def get_buckets(s3):
    if args.bucket:
        return [ s3.Bucket(args.bucket) ]
    return s3.buckets.all()

def parsearguments():
    parser = argparse.ArgumentParser()
    help_text = 'This tool returns information from AWS S3 buckets in a Amazon account'
    parser = argparse.ArgumentParser(description = help_text)
    
    parser.add_argument("--verbose", "-v", help="Verbose mode", action="store_true")
    parser.add_argument("--group", "-g", help="Group by regions", action="store_true")    
    parser.add_argument("--bucket", "-b", help="Bucket name" )
    parser.add_argument("--unit", "-u", help="Size unit [kb|KB|mb|MB|gb|GB|TB]")

    return parser.parse_args()

def main():
    try:
        buckets =  get_buckets(s3)
        buckets_count = len(list(buckets))

        if args.verbose:        
            print('{} buckets found'.format(buckets_count))

        if buckets_count > HIGH_BUCKETS_COUNT_WARNING:
            allowed = get_y_n("WARNING: high number of buckets found, may take sometime to get all data. Continue (y/N)?")
            if not(allowed):
                sys.exit()
    
        all_coveo_buckets = []

        for bucket in buckets:  
            coveo_bucket = get_bucket_details(bucket)
            all_coveo_buckets.append(coveo_bucket)

        print_buckets(all_coveo_buckets)

    except botocore.exceptions.NoCredentialsError:
        print("Sorry, I can't find your credentials file. Please double check the ~/.aws/credentials configuration file")
    except botocore.exceptions.ClientError as e:
        print("Client error, see details below:\n {}".format(e))
    except Exception as e:
        print("Unexpected error occoured, more details bellow\n{}".format(e))

HIGH_BUCKETS_COUNT_WARNING = 100
args = parsearguments()
s3 = boto3.resource('s3')
client = boto3.client('s3')
main()