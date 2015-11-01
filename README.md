# lambda_review_checker
AWS Lambda function for watching AppStore reviews.

## Overview

This is a Scheduled Lambda function to check your app's review posted at AppStore.
The function use DynamoDB to store last review id.(setting up DynamoDB is required. DynamoDB and Lambda function must located on same region)

![slack post image](https://raw.githubusercontent.com/sparkgene/lambda_review_checker/master/slack_post_image.png)

## Installation

```
git clone https://github.com/sparkgene/lambda_review_checker
pip install -r requirements.txt -t /path/to/lambda_review_checker
```

## Configuration

```
cp lambda_review_checker/config.ini.org lambda_review_checker/config.ini
```

Edit `config.ini` with editor and fill up the settings.

```
[appstore]
app_id = # your app id
country = JP # The two-letter country code for the store.

[slack]
token = # slack api token
username = py_bot # name shown on slack message
channel = # post channel ID
icon_url = # costom icon for slack message
icon_emoji = :slack: # use icon. this overrides icon_url.
```
### appstore secion

This script use Search API.
https://www.apple.com/itunes/affiliates/resources/documentation/itunes-store-web-service-search-api.html

But the customer review feed is not public.
Use this script at your own risk.

### slack section

Create a api token. https://api.slack.com/web
Other keys are based on https://api.slack.com/methods/chat.postMessage
If post do not appear to your channel, set `channel id` to `channel`.

## Testing config.ini

Test the slack configuration with following command.

``` shell
python test_slack.py
```

Test the AppStore configuration with following command.

``` shell
python test_appstorereview.py
```

## Usage

1. Edit config.ini
2. Create Amazon DynamoDB table.

  ``` shell
  # create table
  aws dynamodb create-table --table-name lambda_ids --attribute-definitions AttributeName=Id,AttributeType=N --key-schema AttributeName=Id,KeyType=HASH --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1

  # insert default value
  aws dynamodb put-item --table-name lambda_ids --item '{"Id":{"N":"1"},"LastId":{"N":"0"}, "source": {"S":"appstore"}}'

  # confirm data is insert correct.
  aws dynamodb get-item --table-name lambda_ids --key '{"Id":{"N":"1"}}'
  ```
3. Pack function

  ``` shell
  zip -r func.zip . -x .git/**/*
  ```
  details
  http://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html
4. Upload to your lambda function
  See details createing scheduled lambda function.
  http://docs.aws.amazon.com/lambda/latest/dg/getting-started-scheduled-events.html

## Caution

Using this scripts on AWS is not free.
[Amazon DynamoDB Pricing](https://aws.amazon.com/dynamodb/pricing/)
[AWS Lambda Pricing](https://aws.amazon.com/lambda/pricing/)
