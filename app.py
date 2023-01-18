from flask import Flask
import subprocess


app = Flask(__name__)

@app.route('/')
def hello_world():
    import time
    print("something")
    time.sleep(3.5)    # Pause 5.5 seconds
    print("something")
    command = "ffmpeg -i input.mp4 output.avi"
    x = subprocess.run(command, shell=True)
    return 'Hello, World!' +x
