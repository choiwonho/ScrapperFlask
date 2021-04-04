from flask import Flask, render_template, request,redirect, send_file
from scrapper import get_jobs
from exporter import save_to_file
app = Flask("Scrapper")

#fake DB
db = {}

@app.route("/")
def home():
  return render_template("potato.html")

@app.route("/report")
def report():
  #arg : /report?args=1&args3=2이런식으로 전달되는것
  word = request.args.get('word')
  if word:
    word = word.lower()
    #검색한 word가 db에 있는지 찾아봄
    existing_jobs = db.get(word)
    if existing_jobs:
     jobs = existing_jobs
    else:
      #scrapping 동작
      jobs = get_jobs(word)
      #scrapping하고 db['word']에 저장.
      db[word] = jobs
  else: 
    return redirect("/")
  return render_template("report.html",
    searchingBy = word,
    #fakeDB에서 긁어온 jobs의 개수
    results_number = len(jobs),
    jobs = jobs
  )

@app.route("/export")
def export():
  try:
    word = request.args.get('word')
    if not word:
      raise Exception()
    word = word.lower()
    jobs = db.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs)
    return send_file("jobs.csv")
  except:
    return redirect("/")

app.run(host="0.0.0.0")