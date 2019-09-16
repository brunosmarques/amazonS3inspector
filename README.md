# AWS LS
Command line tool that returns information over all S3 buckets in a Amazon account

* must work on linux, OSX and Windows
* easy to install and use
* less frameworks, no external tools allowed
* must be fast!

# Installation

1. Install [Python](https://www.python.org/downloads/) 3.6 (or later) on your system
2. On a terminal at downloaded folder:
```
pip install -r requirements
```
3. Verify your Amazon Credentials in **~/.aws/credentials** file
    * Make sure to have [Cost Explorer](https://console.aws.amazon.com/cost-reports/home) enabled (it take at least 24h after activation to be available)
    * Make sure to have enabled the following API access in [IAM](https://console.aws.amazon.com/iam/home):
      - AmazonS3ReadOnlyAccess
      - AdministratorAccess (for cost)   
```
[default]
aws_access_key_id=AKIAIOSFODNN7EXAMPLE
aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

# Usage
```
python awsls.py 
```
### Arguments
```
  --help, -h
  --verbose, -v
  --bucketfilter, -b
  --filefilter, -f
  --regionfilter, -r
  --group, -g
  --unit, -u
  --sort, -s
  --type, -t
```
### Examples
Get all buckets details sorted by cost
```
python awsls.py -s cost
```

Get details from a specific bucket named mybucket1
```
python awsls.py -b mybucket1
```

List information about all buckets with "prd" on it's name
```
python awsls.py -b prd
```

Get information from all buckets in region us-east-2
```
python awsls.py -r us-east-2
```

Group all buckets by region, sum it's cost and size
```
python awsls.py -g
```

Get information from all buckets, but only for files that are inside a folder named CACHE
```
python awsls.py -f CACHE
```

Get information from all buckets, but only for files that are inside a folder named CACHE/TMP
```
python awsls.py -f CACHE/TMP
```

Get information from buckets named MyBucket, sort by size and display results in GB
```
python awsls.py -b MyBucket -s size -u MB
```

Get information from buckets named MyBucket and filter results by STANDARD storage class files only
```
python awsls.py -b MyBucket -t STANDARD
```
