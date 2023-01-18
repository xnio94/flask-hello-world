import os
import subprocess
import urllib

from flask import Flask
from flask import send_file
from flask import request

app = Flask(__name__)


urls = [
    "https://cf-st.sc-cdn.net/d/OCX13TlDEXbS0A8PUQf7P.111?bo=EhgaABoAMgEEOgF9QgYIy7OTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/9SS6eVdk3S4lmtQUN5suM.111?bo=EhgaABoAMgEEOgF9QgYIqrOTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/0CKxw2b9MTUSBivttCeEd.111?bo=EhgaABoAMgEEOgF9QgYI0LOTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/Qk5Eb303BUmZkP0yzMDhk.111?bo=EhgaABoAMgEEOgF9QgYIrLOTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/XxfkYhUNOmtzTgSKZfFbh.111?bo=EhgaABoAMgEEOgF9QgYIqLOTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/JbDiymCBRuaJJYlVNbQHl.111?bo=EhgaABoAMgEEOgF9QgYIorOTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/ea0A0iKlqcfy1b034ITvW.111?bo=EhgaABoAMgEEOgF9QgYIqrOTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/LYxKChgD8eTUqRF3KOfmf.111?bo=EhgaABoAMgEEOgF9QgYIybOTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/5YvibHLNmzUcBTaZaC5JY.111?bo=EhgaABoAMgEEOgF9QgYIqLOTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/vFI9M5MzSb9UO93Pi0CAg.111?bo=EhgaABoAMgEEOgF9QgYIpbOTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/og6EBbbF9GBRgZwu8YmZV.111?bo=EhgaABoAMgEEOgF9QgYIr7OTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/bjuZcUK5sBw1pFdt2X4JH.111?bo=EhgaABoAMgEEOgF9QgYIp7OTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/7RYuoSElWWWmRE5x8gSHP.111?bo=EhgaABoAMgEEOgF9QgYIqLOTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/BPQFE47Bfe4WoW94r5ST9.111?bo=EhgaABoAMgEEOgF9QgYIpbOTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/EPzRFGc8E2zAz7dP4A7Ko.111?bo=EhgaABoAMgEEOgF9QgYIp7OTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/dPPN1JomWHEn5X7Fm5KEw.111?bo=EhgaABoAMgEEOgF9QgYIy7OTngZIAlAFYAE%3D&uc=5"
    # "https://cf-st.sc-cdn.net/d/63SgUh13qVkBUrFX0oXZP.111?bo=EhgaABoAMgEEOgF9QgYIqbOTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/6iP7qtfspiWVH5udL9FvO.111?bo=EhgaABoAMgEEOgF9QgYIqbOTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/synzSlfknEEPHq3K0RYCd.111?bo=EhgaABoAMgEEOgF9QgYIq7OTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/5XrHrbQY87CbDv588UM3D.111?bo=EhgaABoAMgEEOgF9QgYIyrOTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/LHV7WYLZMJLo1z3RJIZCe.111?bo=EhgaABoAMgEEOgF9QgYIpbOTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/8psTu4I3JYBvAxBSEqRYm.111?bo=EhgaABoAMgEEOgF9QgYIsbOTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/U4lIpkE23M3px76iXCPfW.111?bo=EhgaABoAMgEEOgF9QgYIq7OTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/VDA0CQUvibYKlu4G8c7Ig.111?bo=EhgaABoAMgEEOgF9QgYIsLOTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/nzLMiDDphwOcjmGVGmI2b.111?bo=EhgaABoAMgEEOgF9QgYIqbOTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/3ns88iNnQyeVYrKyexS1s.111?bo=EhgaABoAMgEEOgF9QgYIprOTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/8ymtw5wpXMNGnsiQB6bt8.111?bo=EhgaABoAMgEEOgF9QgYItbOTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/su89SKKfkLOMceUPxfQtY.111?bo=EhgaABoAMgEEOgF9QgYIp7OTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/057CvZYpqLRAeqF8jJd5k.111?bo=EhgaABoAMgEEOgF9QgYIqLOTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/gEA0adjUultSMSIHypiOX.111?bo=EhgaABoAMgEEOgF9QgYIybOTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/SqcIR6ggFC5VryX3SAA7l.111?bo=EhgaABoAMgEEOgF9QgYIqrOTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/gvvA2DomSwyhnrTCpTYm3.111?bo=EhgaABoAMgEEOgF9QgYIx7OTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/E4UoVVVG1WchSeMNDBd3C.111?bo=EhgaABoAMgEEOgF9QgYIqrOTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/CMswxHDJwDWOdk3gptdJc.111?bo=EhgaABoAMgEEOgF9QgYIx7OTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/dRtJE4yqSshLnyQgy91Ri.111?bo=EhgaABoAMgEEOgF9QgYIo7OTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/MXiOsh4M5BVJxc3mEJiXn.111?bo=EhgaABoAMgEEOgF9QgYIsLOTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/bZ5e43DE2O9MCdEyX13ot.111?bo=EhgaABoAMgEEOgF9QgYIy7OTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/ShKRH2R1BKpNNIz5tQefm.111?bo=EhgaABoAMgEEOgF9QgYIuLOTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/uDdNDKCKZiHHoyrqxk9F8.111?bo=EhgaABoAMgEEOgF9QgYIyrOTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/nNYRxDu8TfsYLWBhBonxz.111?bo=EhgaABoAMgEEOgF9QgYIq7OTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/0kcL09k04GJa3H8kRGQJS.111?bo=EhgaABoAMgEEOgF9QgYIsrOTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/gpgRKkXxQ503jn24wvcFB.111?bo=EhgaABoAMgEEOgF9QgYIp7OTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/Pdfzn39Bw6ypTfsUKKIvt.111?bo=EhgaABoAMgEEOgF9QgYIrLOTngZIAlAFYAE%3D&uc=5",
    # "https://cf-st.sc-cdn.net/d/KZeG3ueSP9mOFRADffWZD.111?bo=EhgaABoAMgEEOgF9QgYIrbOTngZIAlAFYAE%3D&uc=5",
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

    # command = "ffmpeg -f concat -i list.txt -c copy output.mp4"
    # x = subprocess.run(command, shell=True)

    # command = "ffmpeg -i output.mp4 -vf scale=1080:1920 -preset ultrafast -threads 4 -c:a copy output2.mp4"
    # x = subprocess.run(command, shell=True)

    command = "ffmpeg -i 0.mp4 -vf scale=1080:1920 -preset ultrafast -threads 4 -c:a copy output2.mp4"
    x = subprocess.run(command, shell=True)

    path = "output.mp4"
    return send_file(path, as_attachment=True)