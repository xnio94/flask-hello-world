import os
import subprocess
import urllib
import re

from flask import Flask
from flask import send_file
from flask import request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/download')
def downloadFile():
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

    # command = "ffmpeg -i output.mp4 -vf scale=1080:1920 -preset ultrafast -threads 4 -c:a copy output2.mp4"
    # x = subprocess.run(command, shell=True)
    # command = "ffmpeg -i 0.mp4 -vf scale=1080:1920 -preset ultrafast -threads 4 -c:a copy output2.mp4"
    # x = subprocess.run(command, shell=True)

    return send_file(title, as_attachment=True)