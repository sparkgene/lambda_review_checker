#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import urllib2


class AppStoreReview:
    APPSTORE_RSS_URL = 'https://itunes.apple.com/rss/customerreviews/page=1/id={0}/sortby=mostrecent/json?cc={1}'

    def __init__(self, app_id, country):
        self._results = []
        self._i = 0

        req = urllib2.Request(AppStoreReview.APPSTORE_RSS_URL.format(
                    app_id, country
                )
            )
        req.add_header('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36')

        response = urllib2.urlopen(req, timeout=15)
        response_string = str(response.read())
        data = json.loads(response_string)
        feed = data.get('feed')
        if feed.get('entry') == None:
            return

        for entry in feed.get('entry'):
            if entry.get('im:name'):
                continue

            self._results.append(
                {
                    'id': long(entry.get('id').get('label')),
                    'author_name':
                        entry.get('author').get('name').get('label'),
                    'version': entry.get('im:version').get('label'),
                    'rating': int(entry.get('im:rating').get('label')),
                    'title': entry.get('title').get('label'),
                    'comment': entry.get('content').get('label'),
                    'voted': entry.get('im:voteCount').get('label')
                }
            )

    def __iter__(self):
        return self

    def next(self):
        if self._i == len(self._results):
            raise StopIteration()
        value = self._results[self._i]
        self._i += 1
        return value
