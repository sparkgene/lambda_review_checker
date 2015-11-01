#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import json
import ConfigParser

from slackclient import SlackClient

def main():

    inifile = ConfigParser.SafeConfigParser()
    inifile.read("./config.ini")

    attachments = [
        {
            "fallback": ":star::star::star::star: awsome app!",
            "pretext": ":star::star::star::star: awsome app!",
            "author_name": "review author",
            "text": "review description.",
            "color": "good"
        }
    ]

    sc = SlackClient(inifile.get('slack', 'token'))
    ret = sc.api_call("chat.postMessage",
                channel=inifile.get('slack', 'channel'),
                attachments=json.dumps(attachments),
                username=inifile.get('slack', 'username'),
                icon_emoji=inifile.get('slack', 'icon_emoji'))
    print ret

if __name__ == '__main__':
    sys.exit(main())
