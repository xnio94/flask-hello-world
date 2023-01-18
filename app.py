from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    import time
    print("something")
    time.sleep(3.5)    # Pause 5.5 seconds
    print("something")
    return 'Hello, World!'
