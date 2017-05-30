#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pypub
import re, unicodedata
import requests
from bs4 import BeautifulSoup
import time
import os
import argparse



def slugify(value):
    """
    Converts to lowercase, removes non-word characters (alphanumerics and
    underscores) and converts spaces to hyphens. Also strips leading and
    trailing whitespace.
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    return re.sub('[-\s]+', '-', value)



def generate_epub(name, start=None, end=None):
    """
    Main method.
    """

    epub = pypub.Epub('The Morning Paper')

    # We test with a downloaded page to avoid excessive connections
    with open("resources/page_15.html") as f:
        html_doc = f.read()
        soup = BeautifulSoup(html_doc, 'html.parser')
        for post in soup.select(".post"):
            #print(post)

            post_link = post.select(".post-header h2 a")[0]
            post_date = post.select(".post-header .date")[0]

            # Collect the HREF
            # Note: the link is useless because the list page contains the full post text.
            href = post_link.attrs['href']

            # Collect and process the title
            title = post_link.get_text()
            slug_title = slugify(title)
            short_slug_title = slug_title  # Will be use to create a folder for each post containing pictures
            if len(short_slug_title) > 20:
                short_slug_title = short_slug_title[:short_slug_title.index("-", 15)]

            # Collect and parse the data
            date_text = post_date.get_text()  # Ex: December 16, 2016
            conv = time.strptime(date_text, "%B %d, %Y")
            date_en = time.strftime("%Y-%m-%d", conv) # Ex: 2016-12-16

            # Collect the content
            content = post.select(".entry")[0]
            content_text = str(content)

            c = pypub.create_chapter_from_string(content_text, title=title)
            epub.add_chapter(c)

    epub.create_epub(os.getcwd())



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Convert The Morning Paper to Epub.')
    parser.add_argument('--start', dest='start', default=None,
                        help='filter posts published after the start date')
    parser.add_argument('--end', dest='end', default=None,
                        help='filter posts published before the end date')
    parser.add_argument('--filename', dest='filename', default="The-Morning-Paper.epub",
                        help='name of the output file')
    args = parser.parse_args()

    generate_epub(args.filename, start=args.start, end=args.end)
