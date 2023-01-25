import os
import subprocess
import urllib
import re

from flask import Flask
from flask import send_file
from flask import request
from flask_cors import CORS

import requests
from bs4 import BeautifulSoup
import json
from munch import DefaultMunch
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/download')
def downloadFile():
    # action = request.args.get('action')
    # if action == 'download':
    #

    link = request.args.get('link')
    count = request.args.get('count')
    count = int(count)

    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find('script', id= '__NEXT_DATA__')
    tree = y = json.loads(s.text)
    tree = DefaultMunch.fromDict(tree)
    pageProps = tree.props.pageProps

    urls = pageProps.preselectedStory.premiumStory.playerStory.snapList
    urls = [e.snapUrls.mediaUrl for e in urls]
    urls = urls[0:count]
    urls = [a.split('.111?')[0] for a in urls]
    episode = pageProps.preselectedStory.premiumStory.playerStory.storyTitle.value
    show = pageProps.publicProfileInfo.title
    episode_num = pageProps.preselectedStory.premiumStory.episodeNumber
    season_num = pageProps.preselectedStory.premiumStory.seasonNumber
    date = pageProps.preselectedStory.premiumStory.timestampInSec.value
    date = datetime.fromtimestamp(int(date))
    date = str(date.date())
    title = str(episode) + '_' + str(show) + '_S' + str(season_num) + '_EP' + str(episode_num) + '_' + date
    title = re.sub(r'[^\w\d-]','_',title)
    title = title + ".mp4"

    with open("list.txt", "w") as f:
        for i in range(0, len(urls)):
            f.write(f"file {i}.mp4\n")

    for i, url in enumerate(urls):
        filename = os.path.join('./', str(i) + ".mp4")
        if os.path.exists(filename):
            os.remove(filename)
        if not os.path.isfile(filename):
            urllib.request.urlretrieve(url, filename)

    if os.path.exists("output.mp4"):
        os.remove("output.mp4")

    command = "ffmpeg -f concat -i list.txt -c copy " + title
    x = subprocess.run(command, shell=True)

    return send_file(title, as_attachment=True)


@app.route('/downloadv1')
def downloadFilev1():
    urls = []
    for i in range(50):
        url = request.args.get('video'+str(i))
        print(url)
        if (url is not None):
            urls = urls + [url]
    urls = urls[0:-1]

    with open("list.txt", "w") as f:
        for i in range(0, len(urls)):
            f.write(f"file {i}.mp4\n")

    for i, url in enumerate(urls):
        filename = os.path.join('./', str(i) + ".mp4")
        if os.path.exists(filename):
            os.remove(filename)
        if not os.path.isfile(filename):
            urllib.request.urlretrieve(url, filename)

    if os.path.exists("output.mp4"):
        os.remove("output.mp4")

    title = request.args.get('title')
    title = re.sub(r'[^\w\d-]','_',title)
    title = title + ".mp4"

    command = "ffmpeg -f concat -i list.txt -c copy " + title
    x = subprocess.run(command, shell=True)

    return send_file(title, as_attachment=True)