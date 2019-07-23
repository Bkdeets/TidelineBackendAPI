# Pivot Backend API

This repository contains the Pivot backend API that was built using the [AWS Chalice](https://github.com/aws/chalice) microframework. 

## Prerequisites

### Install & Configure the AWS CLI

1. Install the AWS CLI
   ```
   > pip install awscli
   ```
2. Configure the AWS CLI with IAM programmatic access credentials
   ```
   > aws configure
   AWS Access Key ID [None]: < AccessKeyId >
   AWS Secret Access Key [None]: < SecretAccessKey >
   Default region name [None]: us-east-1
   Default output format [None]: < PreferredOutput: text or json >
   ```

### Install the Chalice Dependencies

1. Navigate to the `.chalice/` directory
2. (_Optional_) Create a virtual environment: `virtualenv venv`
3. Install the following libraries:
   ```
   > pip install chalice
   > pip install boto3
   ```
4. Navigate to the root directory and install the remaining requirements:
   ```
   > pip install -r requirements.txt
   ```

## Usage

To deploy locally, navigate to the root directory of the repo and enter the following command:

```
> chalice local
Serving on http://127.0.0.1:8000
```

To deploy to AWS, navigate to the root directory of the repo and enter the following command:

```
> chalice deploy --api-gateway-stage dev
```

The `--api-gateway-stage dev` property is optional but **recommended** to avoid accidental deployments to production.