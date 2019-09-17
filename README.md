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
pip install -r requirements.txt
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
  --bucketfilter, -b       BUCKETNAME
  --filefilter, -f         FILENAME
  --regionfilter, -r       { us-east-2,us-east-1,us-west-1,us-west-2,ap-east-1,ap-south-1,... }
  --unit, -u               {kb,KB,mb,MB,gb,GB,TB}
  --sort, -s               {region,creation,files,modified,size,cost}
  --type, -t               {STANDARD,REDUCED_REDUNDANCY,STANDARD_IA,ONEZONE_IA,INTELLIGENT_TIE}
  --group, -g
```
## Examples
#### Get information from all buckets, sort by cost
```
python awsls.py -s cost
```
<details>
  <summary>Result</summary>  
  
```
                   Region       Creation Date  Files             Size  % Size       Last modified      Cost
mybucketprd002  us-east-2 2019-09-13 12:05:44    373  721070816 bytes  86.03% 2019-09-14 15:01:38  1.193732
mybucketprd003  sa-east-1 2019-09-13 12:06:21      3  113500480 bytes  13.54% 2019-09-14 19:49:03  0.187900
mybucketprd001  us-east-2 2019-09-13 12:05:21      8    3552303 bytes   0.42% 2019-09-15 21:07:33  0.005881
bucket1         us-east-2 2019-09-15 19:26:16      1          0 bytes   0.00% 2019-09-15 19:27:18  0.000000
```
</details>

#### Get details from a specific bucket named "mybucket1"
```
python awsls.py -b bucket1
```
<details>
  <summary>Result</summary>  
  
```
            Region       Creation Date  Files     Size % Size       Last modified  Cost
bucket1  us-east-2 2019-09-15 19:26:16      1  0 bytes  0.00% 2019-09-15 19:27:18     0
```
</details>

#### Get information from buckets named "prd", sort by modified date, display results in MB
```
python awsls.py -b prd -s modified -u MB
```
<details>
  <summary>Result</summary>  
  
```
                   Region       Creation Date  Files    Size  % Size       Last modified      Cost
mybucketprd001  us-east-2 2019-09-13 12:05:21      8    3 MB   0.42% 2019-09-15 21:07:33  0.005881
mybucketprd003  sa-east-1 2019-09-13 12:06:21      3  108 MB  13.54% 2019-09-14 19:49:03  0.187900
mybucketprd002  us-east-2 2019-09-13 12:05:44    373  688 MB  86.03% 2019-09-14 15:01:38  1.193732
```
</details>

#### Get information from buckets in region us-east-2
```
python awsls.py -r us-east-2
```
<details>
  <summary>Result</summary>  
  
```
                   Region       Creation Date  Files             Size  % Size       Last modified      Cost
bucket1         us-east-2 2019-09-15 19:26:16      1          0 bytes   0.00% 2019-09-15 19:27:18  0.000000
mybucketprd001  us-east-2 2019-09-13 12:05:21      8    3552303 bytes   0.49% 2019-09-15 21:07:33  0.006802
mybucketprd002  us-east-2 2019-09-13 12:05:44    373  721070816 bytes  99.51% 2019-09-14 15:01:38  1.380711
```
</details>

#### Get information from all buckets, group by region, sum cost and size
```
python awsls.py -g
```
<details>
  <summary>Result</summary>  
  
```
           Files      Cost
Region
sa-east-1      3  0.187900
us-east-2    382  1.199613
```
</details>

#### Get information from all buckets, filter files that contains CACHE in their path
```
python awsls.py -f CACHE
```
<details>
  <summary>Result</summary>  
  
```
                   Region       Creation Date  Files           Size   % Size        Last modified      Cost
bucket1         us-east-2 2019-09-15 19:26:16      1        0 bytes    0.00%  2019-09-15 19:27:18  0.000000
mybucketprd001  us-east-2 2019-09-13 12:05:21      6  1974110 bytes  100.00%  2019-09-15 21:07:33  1.387513
mybucketprd002  us-east-2 2019-09-13 12:05:44      0        0 bytes    0.00%                    -  0.000000
mybucketprd003  sa-east-1 2019-09-13 12:06:21      0        0 bytes    0.00%                    -  0.000000
```
</details>

#### Get information from buckets named "mybucketprd2", filter by STANDARD storage class, display results in KB
```
python awsls.py -b mybucketprd2 -t STANDARD -u KB
```
<details>
  <summary>Result</summary>  
  
```
                   Region       Creation Date  Files        Size   % Size       Last modified      Cost
mybucketprd002  us-east-2 2019-09-13 12:05:44    373  704,171 KB  100.00% 2019-09-14 15:01:38  1.387513
```
</details>
