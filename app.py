import os
import subprocess
import urllib

from flask import Flask
from flask import send_file

app = Flask(__name__)

urls = [
    "https://cf-st.sc-cdn.net/d/OCX13TlDEXbS0A8PUQf7P.111?bo=EhgaABoAMgEEOgF9QgYIy7OTngZIAlAFYAE%3D&uc=5",
    "https://cf-st.sc-cdn.net/d/9SS6eVdk3S4lmtQUN5suM.111?bo=EhgaABoAMgEEOgF9QgYIqrOTngZIAlAFYAE%3D&uc=5",
    "https://cf-st.sc-cdn.net/d/0CKxw2b9MTUSBivttCeEd.111?bo=EhgaABoAMgEEOgF9QgYI0LOTngZIAlAFYAE%3D&uc=5",
]


@app.route('/')
def hello_world():
    for i, url in enumerate(urls):
        filename = os.path.join('./', 'image' + str(i) + ".mp4")
    if not os.path.isfile(filename):
        urllib.request.urlretrieve(url, filename)

    command = "ffmpeg -i image0.mp4 output.avi"
    x = subprocess.run(command, shell=True)
    return 'Hello, World!'


@app.route('/download')
def downloadFile():
    name = "video.mp4"
    urllib.request.urlretrieve(urls[0], name)
    path = "./" + name
    return send_file(path, as_attachment=True)
