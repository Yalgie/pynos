import soco, time

from gtts import gTTS
from mutagen.mp3 import MP3
from soco.snapshot import Snapshot
from flask import Flask, request, render_template, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play', methods=['POST'])
def play():
	Sonos().play(request.form['text'])
	return redirect("/")

class Sonos():
	def play(self, text):
		tts = gTTS(text=text, lang='en')
		tts.save("sound.mp3")
		audio = MP3("sound.mp3")

		for speaker in soco.discover():
			snap = Snapshot(speaker) 
			snap.snapshot()

			speaker.volume = 50
			speaker.play_uri("http://192.168.0.3:8080/sound.mp3")

			time.sleep(audio.info.length)
			snap.restore()

if __name__ == '__main__':
	app.run(
		host = "0.0.0.0",
		debug = True
	)