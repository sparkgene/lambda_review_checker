# -*- coding: utf-8 -*-
import boto3
import json
from time import gmtime, strftime
import ConfigParser

from appstorereview import AppStoreReview
from slackclient import SlackClient

def lambda_handler(event, context):
    print(strftime('%a, %d %b %Y %H:%M:%S +0000', gmtime()))
    inifile = ConfigParser.SafeConfigParser()
    inifile.read('./config.ini')

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(inifile.get('dynamodb', 'table_id'))
    key_id = int(inifile.get('dynamodb', 'id_value'))
    result = table.get_item(
        Key={
            'Id': key_id
        }
    )
    previous_last_id = result['Item']['LastId']

    last_id = previous_last_id
    print('previous_last_id: {0}'.format(previous_last_id))

    send_count = 0
    sc = SlackClient(inifile.get('slack', 'token'))
    for review in AppStoreReview(
            inifile.get('appstore', 'app_id'),
            inifile.get('appstore', 'country')):

        print("review id: {0}".format(review['id']))
        if last_id < review['id']:
            last_id = review['id']
        else:
            if previous_last_id >= review['id']:
                print('old review.skip sending')
                continue

        send_count += 1
        title = "{0} {1}".format(':star:' * review['rating'], review['title'])
        color = '#439FE0'
        if review['rating'] in [1, 2]: color = 'danger'
        if review['rating'] in [3, 4]: color = 'good'
        attachments = [
            {
                'fallback': title,
                'pretext': title,
                'author_name': review['author_name'],
                'text': review['comment'],
                'color': color
            }
        ]
        sc.api_call('chat.postMessage',
                    channel=inifile.get('slack', 'channel'),
                    attachments=json.dumps(attachments),
                    username=inifile.get('slack', 'username'),
                    icon_emoji=inifile.get('slack', 'icon_emoji'))
        print('sended to slack')

    print('last_id: {0}'.format(last_id))
    if last_id > previous_last_id:
        table.put_item(
            Item={'Id': key_id, 'LastId': last_id}
        )
    return True
