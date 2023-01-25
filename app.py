import json
import os
import re
import subprocess
import urllib
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask import jsonify
from flask import request
from flask import send_file
from flask_cors import CORS
from munch import DefaultMunch

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'


def get_title_urls(episode_link):
    r = requests.get(episode_link)
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find('script', id='__NEXT_DATA__')
    tree = y = json.loads(s.text)
    tree = DefaultMunch.fromDict(tree)
    pageProps = tree.props.pageProps

    urls = pageProps.preselectedStory.premiumStory.playerStory.snapList
    urls = [e.snapUrls.mediaUrl for e in urls]
    urls = [a.split('.111?')[0] for a in urls]

    episode = pageProps.preselectedStory.premiumStory.playerStory.storyTitle.value
    show = pageProps.publicProfileInfo.title
    episode_num = pageProps.preselectedStory.premiumStory.episodeNumber
    season_num = pageProps.preselectedStory.premiumStory.seasonNumber
    date = pageProps.preselectedStory.premiumStory.timestampInSec.value
    date = datetime.fromtimestamp(int(date))
    date = str(date.date())
    title = str(episode) + '_' + str(show) + '_S' + str(season_num) + '_EP' + str(
        episode_num) + '_' + date
    title = re.sub(r'[^\w\d-]', '_', title)
    title = title + ".mp4"
    return title, urls


@app.route('/download')
def downloadFile():
    action = request.args.get('action')
    if action == 'download_clips':
        episode_link = request.args.get('episode_link')
        count = request.args.get('count')
        count = int(count)
        title, urls = get_title_urls(episode_link)
        # urls = urls[0:count]
        if count == -1:
            count = len(urls) - 1

        valid_count = 0
        for i in range(count):
            filename = os.path.join('./', str(valid_count) + ".mp4")
            if os.path.exists(filename):
                os.remove(filename)
            try:
                urllib.request.urlretrieve(urls[i], filename)
                valid_count = valid_count + 1
            except:
                print("An exception occurred")

        with open("list.txt", "w") as f:
            for i in range(valid_count):
                f.write(f"file {i}.mp4\n")

        return jsonify({"title": title})

    if action == 'merge':
        title = request.args.get('title')
        if os.path.exists(title):
            os.remove(title)
        command = "ffmpeg -f concat -i list.txt -c copy " + title
        x = subprocess.run(command, shell=True)
        return jsonify({"ready": "Ok"})

    if action == 'download':
        title = request.args.get('title')
        return send_file(title, as_attachment=True)


##############################################
##############################################
##############################################
##############################################
##############################################
##############################################
##############################################
##############################################
##############################################
##############################################
##############################################
##############################################
##############################################
##############################################
##############################################
##############################################
##############################################
##############################################
##############################################
##############################################
##############################################
##############################################
##############################################
##############################################
##############################################
##############################################


@app.route('/downloadv1')
def downloadFilev1():
    urls = []
    for i in range(50):
        url = request.args.get('video' + str(i))
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
    title = re.sub(r'[^\w\d-]', '_', title)
    title = title + ".mp4"

    command = "ffmpeg -f concat -i list.txt -c copy " + title
    x = subprocess.run(command, shell=True)

    return send_file(title, as_attachment=True)
