import os
from flask import Flask, render_template, render_template_string, url_for, jsonify, request, redirect
#import json
from pymongo import MongoClient
import requests as req
import bs4
from bs4 import BeautifulSoup
print(os.environ)

rl = "https://dbm.sourav87.repl.co/dashboard"
def gkel(url=rl):
	data = req.get(url).content
	soup = BeautifulSoup(data, features="html5lib")
	images = soup.findAll('button')
	for image in images:
		img_url = image.get('kel')
		print(img_url)
		return img_url



sdb = MongoClient(os.environ["SPDB"])
sdbc = sdb["qna"]["query"]
value = os.environ["TOKEN"]
#sdbc.update_many({},{"$set":{"rating":0}})



docs = []
for i in sdbc.find():
	#print(i)
	docs.append(i)

app = Flask('app')

@app.route('/')
def hello_world():
  return '<script>window.location.href="/login"</script>'

@app.route("/login")
def login():
	return render_template("login.html", token=value)


@app.route("/oauth", methods=["POST"])
def oauth():
	data = request.form.to_dict()
	print(data)
	#token = secrets.token_hex(16)
	if data["email"] != os.environ["AMAIL"]:
		return "You've Entered Wrong Email"
	if data["pass"] != os.environ["APASS"]:
		return "You've Entered Wrong Password"
	script = f"""<!DOCTYPE html><script>localStorage.setItem('token', '{value}');
 window.location.href='https://dbm.sourav87.repl.co/dashboard';
    </script>
    """
	return render_template_string(script)



@app.route("/v2", methods=["POST"])
def verify():
	data = request.form.to_dict()
	key = request.args.get('token')
	print(data['key'], key)
	#print(data)
	if "key" not in data:
		return "<script>window.location.href='https://dbm.sourav87.repl.co/login'</script>"
	if {data['key']} == value:
		return "<script>window.location.href='https://dbm.sourav87.repl.co/dashboard'</script>"
	return "<script>window.location.href='https://dbm.sourav87.repl.co/login'</script>"



@app.route("/add", methods=["POST"])
def add():
	data = request.form.to_dict()
	db = sdbc.find_one({"q":data["q"]})
	if db is not None:
		sdbc.update_one({"q":data["q"]},{"$set":data})
	if db is None:
		sdbc.insert_one(data)
		docs.append(data)
	return "<script>window.location.href=window.location.href + '#doc'</script>"


@app.route("/del", methods=["POST"])
def dell():
	data = request.form.to_dict()
	db = sdbc.find_one({"q":data["q"]})
	if db is not None:
		sdbc.delete_one({"q":data["q"]})
		#docs.remove(data)
	return "<script>window.location.href=window.location.href + '#del'</script>"



@app.route("/docs")
def doc():
	return render_template("docs.html", list=docs, token=value)



@app.route("/dashboard")
def dash():
	data =  {"docs":len(docs)}
	return render_template("index.html", token=value, tkl=len(value), list=docs, data=data)
	

app.run(host='0.0.0.0', port=8080)
