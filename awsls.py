# Amazon SDK
import boto3

# Amazon SDK exceptions
from boto3.exceptions import botocore

# Arguments parsing utility
import argparse

# System library to exit to console
import sys

# Datetime for date manipulation
from datetime import datetime, timedelta

# Pandas for data filtering and visualization
import pandas as pd

class cBucket:
    """ Class that represents a bucket in AWS. Contains name, creation date, files count, total files size, most recent file date modification, files count per storage types, cost and region
    """
    total_size_list = []

    def __init__(self, name):
        self.name = name
        self.creation_date = datetime(1, 1, 1).replace(tzinfo=None)
        self.files_count = 0
        self.files_size = 0
        self.last_modified = datetime(1, 1, 1).replace(tzinfo=None)
        self.storage_types = {}
        self.cost = 0.
        self.region = ''

def format_size(value):
    """ Convert bytes to other units, such as KB, MB, GB
    """
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
    """ Print bucket in different ways
    """
    data = []
    names = []    
    for bucket in buckets:
        total_size = sum(bucket.total_size_list)
        if total_size == 0:
            bucket.cost = 0
        else:
            bucket.cost = (bucket.files_size/total_size) * (float(total_cost))

        d = [            
            bucket.region,
            bucket.creation_date,
            bucket.files_count,
            format_size(bucket.files_size),
            bucket.last_modified,
            bucket.cost ]
        data.append(d)
        names.append(bucket.name)

    features = {'region':'Region', 'creation':'Creation Date', 'files':'Files', 'size':'Size', 'modified':'Last modified' , 'cost':'Cost'}
    dataframe = pd.DataFrame(data=data,columns=features.values(),index=names)

    if args.group:
        dataframe = dataframe.groupby('Region').sum()        
    elif args.regionfilter:
        dataframe = dataframe[dataframe.Region == args.regionfilter]
    
    if args.sort:
        dataframe = dataframe.sort_values(features[args.sort], ascending=False)

    if not dataframe.empty:
        print(dataframe)
    else:
        print("No buckets match your criteria")

def isValidFile(f):
    """ Return a boolean indicating if file f is valid
    """
    result = False
    if f.storage_class == args.type or not(args.type):
        if str(args.filefilter) in str(f.key) or not(args.filefilter):
            result = True
    return result
    
def get_bucket_details(bucket):
    """ Get bucket details from amazon, create an populate a cBucket object and return it at the end
    """ 
    if args.verbose:        
            print('\tRetreving files in bucket {}'.format(bucket.name), end='...', flush=True)
    files = bucket.objects.all()
    if args.verbose:        
            print('done')
    
    last_modified_file = datetime(1, 1, 1).replace(tzinfo=None)
    total_files_size = 0
    valid_files_count = 0
    storage_types = {}

    for f in files:
        if isValidFile(f):
            total_files_size+=f.size
            valid_files_count+=1

            last_change = f.last_modified.replace(tzinfo=None)
            if last_modified_file < last_change or last_modified_file=='':
                last_modified_file = last_change
            
            if (f.storage_class in storage_types): 
                storage_types[f.storage_class] += 1
            else: 
                storage_types[f.storage_class] = 1

    location_response = client.get_bucket_location( Bucket=bucket.name )
    location = location_response['LocationConstraint']

    coveo_bucket = cBucket(bucket.name)
    coveo_bucket.creation_date = bucket.creation_date.replace(tzinfo=None)
    coveo_bucket.files_count = valid_files_count
    coveo_bucket.files_size = total_files_size
    coveo_bucket.last_modified = last_modified_file.replace(tzinfo=None)
    coveo_bucket.storage_types = storage_types   
    coveo_bucket.region = location_response['LocationConstraint']
    coveo_bucket.total_size_list.append(total_files_size)

    return coveo_bucket

def get_y_n(text):
    """ Get Y or N from user with a friendly message. No input returns False (N)
    """
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
    """ Get all buckets from Amazon and return a filtered subset of them using command-line filters
    """
    buckets = s3.buckets.all()
    filtered_buckets = []
    
    for bucket in buckets:
        if str(args.bucketfilter) in str(bucket.name) or not(args.bucketfilter):
            location = ''
            if args.regionfilter:
                location_response = client.get_bucket_location( Bucket=bucket.name )
                location = location_response['LocationConstraint']
            if location == args.regionfilter or not(args.regionfilter):
                filtered_buckets.append(bucket)
    
    return filtered_buckets, len(filtered_buckets)

def parsearguments():
    """ Parse arguments from command-line
    """
    parser = argparse.ArgumentParser()
    help_text = 'This tool returns useful information from AWS S3 bucket'
    parser = argparse.ArgumentParser(description = help_text)
    
    aws_regions = [ 'us-east-2',
        'us-east-1',
        'us-west-1',
        'us-west-2',
        'ap-east-1',
        'ap-south-1',
        'ap-northeast-3',
        'ap-northeast-2',
        'ap-southeast-1',
        'ap-southeast-2',
        'ap-northeast-1',
        'ca-central-1',
        'cn-north-1',
        'cn-northwest-1',
        'eu-central-1',
        'eu-west-1',
        'eu-west-2',
        'eu-west-3',
        'eu-north-1',
        'me-south-1',
        'sa-east-1',
        'us-gov-east-1',
        'us-gov-west-1']

    parser.add_argument("--verbose", "-v", help="Verbose mode", action="store_true")
    parser.add_argument("--group", "-g", help="Group by regions", action="store_true")    
    # parser.add_argument("--cost", "-c", help="Try to get the cost", action="store_true")    
    parser.add_argument("--bucketfilter", "-b", help="Bucket name filter" )
    parser.add_argument("--regionfilter", "-r", help="Region filter", choices=aws_regions)
    parser.add_argument("--filefilter", "-f", help="File filter")
    parser.add_argument("--type", "-t", help="Storage type", choices=[ 'STANDARD', 'REDUCED_REDUNDANCY', 'STANDARD_IA', 'ONEZONE_IA', 'INTELLIGENT_TIE' ] )
    parser.add_argument("--unit", "-u", help="Size unit", choices=[ 'kb', 'KB', 'mb', 'MB', 'gb', 'GB', 'TB'])
    parser.add_argument("--sort", "-s", help="Sort by feature (descending)", choices=[ 'region', 'creation', 'files', 'modified', 'size', 'cost' ])

    return parser.parse_args()

def getTotalCost():
    """ Get total storage cost from last day from Amazon. Can't be filtered
    """
    if args.bucketfilter or args.type or args.filefilter:
        print("WARNING: cost estimation isn't compatible with filtering. Cost results may not be reliabe.")

    today = datetime.today().date()
    yesterday = today-timedelta(days=2)
    try:
        ce = boto3.client('ce')
        cost_response = ce.get_cost_and_usage(TimePeriod={
                                                'Start': str(yesterday),
                                                'End': str(today)
                                            },
                                            Granularity='MONTHLY',
                                            Metrics=[ 'AmortizedCost']
                                        )
        c = cost_response['ResultsByTime'].pop()['Total']['AmortizedCost']['Amount']
    except Exception:
        print("Can't get cost estimation from Amazon, cost will be zero")
        c = 0
    return c

def main():
    """ Main method that control global flow
    """
    try:
        buckets, buckets_count = get_buckets(s3)
        
        global total_cost
        total_cost = getTotalCost()

        if args.verbose:        
            print('{} buckets found'.format(buckets_count))
            
        if buckets_count > HIGH_BUCKETS_COUNT_WARNING:
            allowed = get_y_n("WARNING: high number of buckets found ({}), it may take a while to get all data. Continue (y/N)?".format(buckets_count))
            if not(allowed):
                sys.exit()
    
        target_buckets = []
        for bucket in buckets:  
            coveo_bucket = get_bucket_details(bucket)
            target_buckets.append(coveo_bucket)
        
        print_buckets(target_buckets)

    except botocore.exceptions.NoCredentialsError:
        print("Sorry, I can't find your credentials file. Please double check the ~/.aws/credentials configuration file")
    except botocore.exceptions.ClientError as e:
        print("Client error, see details below:\n {}".format(e))
    except Exception as e:
        print("Unexpected error occoured, more details bellow\n{}".format(e))

# Set constants
HIGH_BUCKETS_COUNT_WARNING = 3

# Initialize global variables
total_cost = 0

# Parse command-line arguments
args = parsearguments()

# Instantiates Amazon SDK resources
s3 = boto3.resource('s3')
client = boto3.client('s3')

main()