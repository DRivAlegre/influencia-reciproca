import os, sys, threading

from flask import Flask, render_template

from track_images.exportimage import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

def begin_thread(worker):
	threads = list()
	t = threading.Thread(target=worker)
	threads.append(t)
	t.start()
	return threads,t

if __name__ == '__main__':
	limg, path, operations = init()
	observerimg_instance = ObserverImgFolder(limg, path, operations)
	begin_thread(observerimg_instance.observe_img)
	port = int(os.environ.get('PORT', 5205))
	app.run(host='0.0.0.0', port=port)


