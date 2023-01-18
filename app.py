import os
import subprocess
import urllib

from flask import Flask
from flask import send_file
from flask import request

app = Flask(__name__)

urls = [
    "https://cf-st.sc-cdn.net/d/OCX13TlDEXbS0A8PUQf7P.111?bo=EhgaABoAMgEEOgF9QgYIy7OTngZIAlAFYAE%3D&uc=5",
    "https://cf-st.sc-cdn.net/d/9SS6eVdk3S4lmtQUN5suM.111?bo=EhgaABoAMgEEOgF9QgYIqrOTngZIAlAFYAE%3D&uc=5",
    "https://cf-st.sc-cdn.net/d/0CKxw2b9MTUSBivttCeEd.111?bo=EhgaABoAMgEEOgF9QgYI0LOTngZIAlAFYAE%3D&uc=5",
    "https://cf-st.sc-cdn.net/d/OCX13TlDEXbS0A8PUQf7P.111?bo=EhgaABoAMgEEOgF9QgYIy7OTngZIAlAFYAE%3D&uc=5",
    "https://cf-st.sc-cdn.net/d/9SS6eVdk3S4lmtQUN5suM.111?bo=EhgaABoAMgEEOgF9QgYIqrOTngZIAlAFYAE%3D&uc=5",
    "https://cf-st.sc-cdn.net/d/0CKxw2b9MTUSBivttCeEd.111?bo=EhgaABoAMgEEOgF9QgYI0LOTngZIAlAFYAE%3D&uc=5",
]


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/download')
def downloadFile():
    # username = request.args.get('username')
    # password = request.args.get('password')
    #
    with open("list.txt", "w") as f:
        for i in range(0, len(urls)):
            f.write(f"file {i}.mp4\n")
    for i, url in enumerate(urls):
        filename = os.path.join('./', str(i) + ".mp4")
        if not os.path.isfile(filename):
            urllib.request.urlretrieve(url, filename)

    command = "ffmpeg -f concat -i list.txt -c copy output.mp4"
    x = subprocess.run(command, shell=True)

    command = "ffmpeg -i output.mp4 -vf scale=1080:1920 -preset ultrafast -threads 4 -c:a copy output2.mp4"
    x = subprocess.run(command, shell=True)

    path = "output2.mp4"
    return send_file(path, as_attachment=True)
