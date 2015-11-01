#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import ConfigParser

from appstorereview import AppStoreReview


def main():

    inifile = ConfigParser.SafeConfigParser()
    inifile.read("./config.ini")

    for review in AppStoreReview(
            inifile.get('appstore', 'app_id'),
            inifile.get('appstore', 'country')):
        print('----------------------------------------------------------')
        print("id: {0}".format(review['id']))
        print(u"author_name: {0}".format(review['author_name']))
        print("version: {0}".format(review['version']))
        print("rating: {0}".format(review['rating']))
        print(u"title: {0}".format(review['title']))
        print(u"comment: {0}".format(review['comment']))
        print("voted: {0}".format(review['voted']))

if __name__ == '__main__':
    sys.exit(main())
