import urllib
import json
from flask import *
from firebase import Firebase
from werkzeug.utils import secure_filename
from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
import re
import requests
import os
import moviepy.editor as mp
from sumy.parsers.plaintext import PlaintextParser #We're choosing a plaintext parser here, other parsers available for HTML etc.
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import speech_recognition as sr
import glob
from pydub import AudioSegment

r = sr.Recognizer()
summarizer_lsa = LsaSummarizer()
headers = {'user-agent': 'Wget/1.16 (linux-gnu)'}

firebaseConfig = {
    "apiKey": "AIzaSyDw65BvUcaILJoXX8Mws5QOTRLjyXCGlf0",
    "authDomain": "webschool-7e9db.firebaseapp.com",
    "projectId": "webschool-7e9db",
    "storageBucket": "webschool-7e9db.appspot.com",
    "messagingSenderId": "396594842645",
    "appId": "1:396594842645:web:df2c845b47405bacb9521c",
    "databaseURL" : " "
  }

app = Flask(__name__, static_folder='./static')
fire = Firebase(firebaseConfig)
auth = fire.auth()

@app.route('/', methods=['GET', 'POST'])
def login_page():
	return render_template('Intro_page.html')

# Replace with this in main.py
@app.route('/login', methods=['GET', 'POST'])
def basic():
    if request.method == 'POST':
      if request.form["submit"] == "register":
        email = request.form.get("sup")
        password = request.form.get("pwd")
        try:
          register = auth.create_user_with_email_and_password(email, password)
          return render_template('login.html')
        except:
          return "Invalid email and password. "

      elif request.form["submit"] == "login":
        email = request.form.get("sup")
        password = request.form.get("pwd")
        try:
          login = auth.sign_in_with_email_and_password(email, password)
          return render_template('HomePage.html')
        except:
          return "Wrong email and password."


@app.route("/upload", methods=["GET", "POST"])
def upload():
  if request.method == 'POST':
    f = request.files.get('file')
    f.save(secure_filename("./static/f.txt"))
    output_string = StringIO()
    with open(secure_filename("./static/f.txt"), 'rb') as in_file:
      parser = PDFParser(in_file)
      doc = PDFDocument(parser)
      rsrcmgr = PDFResourceManager()
      device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
      interpreter = PDFPageInterpreter(rsrcmgr, device)
      for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)
      document = output_string.getvalue()
      document = document.replace("/n", "")
      count = document.count(".")
      noofsent = round(30/100 * count)
      parser = PlaintextParser.from_string(document,Tokenizer("english"))
      summary_2 =summarizer_lsa(parser.document,noofsent)
      summary = ""
      for sentence in summary_2:
          summary += str(sentence)
      return render_template("Summary.html", chapter_summary=summary)

@app.route("/classnotesmaker", methods = ["GET", "POST"])
def classnotes():
  if request.form.get("dropbox") == "" or request.form.get("dropbox") == " ":
    return "Invalid link. Please enter the correct link and try again."
  req = requests.get(request.form.get("dropbox"), stream=True, headers=headers, allow_redirects=True)
  open('./static/video.mp4', 'wb').write(req.content)
  if not "chunks" in os.listdir():
      os.mkdir("./chunks")
  files = glob.glob('./chunks/*')
  for f in files:
      os.remove(f)
  my_clip = mp.VideoFileClip("./static/video.mp4")
  my_clip.audio.write_audiofile("./static/audio_from_video.wav")
  audio = AudioSegment.from_wav("./static/audio_from_video.wav")
  duration = audio.duration_seconds
  t1 = 0 * 1000
  t2 = 59 * 1000
  while duration > 5:
      newAudio = audio[t1:t2]
      newAudio.export('./chunks/newSong' + str(t1/1000) + '.wav', format="wav")
      t1 += 60 * 1000
      t2 += 60 * 1000
      duration -= 60
  full_text = ""
  for filename in os.listdir('./chunks'):
      with sr.AudioFile('./chunks/'+filename) as source:
          audio = r.record(source)
          try:
              text = r.recognize_google(audio)
              full_text += " " + text
          except sr.UnknownValueError:
              print("Google Speech Recognition could not understand audio")
              break
          except sr.RequestError as e:
              print("Could not request results from Google Speech Recognition service; {0}".format(e))
              break
  print(full_text)
  return render_template("Summary.html", class_summary=full_text)

@app.route("/summarizer", methods = ["GET", "POST"])
def summarizer():
  return render_template("Summary.html")

@app.route("/homepage", methods=["GET", "POST"])
def home():
  return render_template('HomePage.html')

@app.route("/loginpage", methods=["GET", "POST"])
def login():
  return render_template('login.html')

@app.route("/classpage", methods=["GET", "POST"])
def classpage():
  return render_template('Class.html')

@app.route("/arpage", methods=["GET", "POST"])
def ar():
  return render_template('Gallery.html')

@app.route("/aboutpage", methods=["GET", "POST"])
def about():
  return render_template('About.html')

@app.route("/intropage", methods=["GET", "POST"])
def intro():
  return render_template('Intro_page.html')

if __name__ == '__main__':
  port = int(os.environ.get("PORT", 5000))
  print(f"Running on: 127.0.0.1:{port}")
  app.run(host='127.0.0.1', port=port, threaded=True)
