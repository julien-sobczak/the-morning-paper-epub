#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
$ python main.py --start 2014-10-08 --end 2016-01-01
"""

import pypub
import re, unicodedata
import requests
from bs4 import BeautifulSoup
import time
import os
import argparse
import collections

import sys
reload(sys)
sys.setdefaultencoding('utf8')



def generate_epub(name, start=None, end=None):
    """
    Main method.
    """

    # Collect post to sort them after
    posts = {}

    page = 1
    while True:
        r = requests.get('https://blog.acolyer.org/page/%s/' % page)
        if r.status_code == 404:
            print("Reach the end of the blog at page %s" % page)
            break
        page = page + 1

        html_doc = r.text
        soup = BeautifulSoup(html_doc, 'html.parser')
        for post in soup.select(".post"):
            #print(post)

            post_link = post.select(".post-header h2 a")[0]
            post_date = post.select(".post-header .date")[0]

            # Collect the HREF
            # Note: the link is useless because the list page contains the full post text.
            href = post_link.attrs['href']

            # Collect the title
            title = post_link.get_text()

            if not title:
                print("Fail to find the title: %s" % post)

            # Collect and parse the data
            date_text = post_date.get_text()  # Ex: December 16, 2016
            conv = time.strptime(date_text, "%B %d, %Y")
            date_en = time.strftime("%Y-%m-%d", conv) # Ex: 2016-12-16

            # Filter according the dates
            if start and date_en < start:
                continue
            if end and date_en >= end:
                continue

            print("Processing post %s (%s)" % (title, date_en))

            # Collect the content
            content = post.select(".entry")[0]
            content_text = u"""
            <h2>%s</h2>
            <h3>%s</h3>
            %s
            """ % (title, date_text, str(content))

            # Post are traversed in reverse order
            posts[date_en] = {
                "date": date_text,
                "title": title,
                "content": content_text
            }

    # Sort the post starting from the oldest
    ordered_posts = collections.OrderedDict(sorted(posts.items()))

    # Generate the target file
    epub = pypub.Epub(name)
    for date_en, post in ordered_posts.iteritems():
        c = pypub.create_chapter_from_string(post["content"], title=post["title"])
        epub.add_chapter(c)
    epub.create_epub(os.getcwd())


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Convert The Morning Paper to Epub.')
    parser.add_argument('--start', dest='start', default=None,
                        help='filter posts published after the start date')
    parser.add_argument('--end', dest='end', default=None,
                        help='filter posts published before the end date')
    parser.add_argument('--filename', dest='filename', default="The-Morning-Paper",
                        help='name of the output file without the extension')
    args = parser.parse_args()

    generate_epub(args.filename, start=args.start, end=args.end)
