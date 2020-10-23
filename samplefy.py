from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/")
def home():
	return "<h1>Samplefy, the web application that combines Spotify and WhoSampled</h1>"

@app.route("/<title>")
def song(title):
	return f"Now playing {title}"

@app.route("/admin")
def admin():
		return redirect(url_for("home"))

if __name__ == "__main__":
	app.run(debug=True) #Auto saves upon change in file