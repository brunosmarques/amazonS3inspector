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
## Arguments
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
## Examples
### Get all buckets details sorted by cost
```
python awsls.py -s cost
```
Result
```
                   Region       Creation Date  Files             Size       Last modified      Cost
mybucketprd2    us-east-2 2019-09-13 12:05:44    373  721070816 bytes 2019-09-14 15:01:38  1.159216
mybucketprd3    sa-east-1 2019-09-13 12:06:21      3  113500480 bytes 2019-09-14 19:49:03  0.182467
mybucketprd1    us-east-2 2019-09-13 12:05:21      8    3552303 bytes 2019-09-15 21:07:33  0.005711
mybucket1       us-east-2 2019-09-15 19:26:16      1          0 bytes 2019-09-15 19:27:18  0.000000
```

### Get details from a specific bucket named "mybucket1"
```
python awsls.py -b mybucket1
```
Result
```
            Region       Creation Date  Files     Size       Last modified  Cost
mybucket1  us-east-2 2019-09-15 19:26:16      1  0 bytes 2019-09-15 19:27:18     0
```

### Get information from buckets named "prd", sort by modified date and display results in MB
```
python awsls.py -b "prd" -s modified -u MB
```
Result
```
                 Region       Creation Date  Files    Size       Last modified      Cost
mybucketprd1  us-east-2 2019-09-13 12:05:21      8    3 MB 2019-09-15 21:07:33  0.005881
mybucketprd3  sa-east-1 2019-09-13 12:06:21      3  108 MB 2019-09-14 19:49:03  0.187900
mybucketprd2  us-east-2 2019-09-13 12:05:44    373  688 MB 2019-09-14 15:01:38  1.193732
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



Get information from buckets named MyBucket and filter results by STANDARD storage class files only
```
python awsls.py -b MyBucket -t STANDARD
```
