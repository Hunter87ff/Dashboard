import os
from flask import Flask, render_template, render_template_string, url_for, jsonify, request, redirect
import json
import secrets
import pymongo
from pymongo import MongoClient



sdb = MongoClient(os.environ["spdb"])
sdbc = sdb["qna"]["query"]
value = os.environ["token"]
docs = sdbc.find()



app = Flask('app')

@app.route('/')
def hello_world():
  return 'Hello, World!'

@app.route("/login")
def login():
	return render_template("login.html", token=value)


@app.route("/oauth", methods=["POST"])
def oauth():
	data = request.form.to_dict()
	print(data)
	token = secrets.token_hex(16)
	if data["email"] != os.environ["amail"]:
		return "You've Entered Wrong Email"
	if data["pass"] != os.environ["apass"]:
		return "You've Entered Wrong Password"
	script = f"""<!DOCTYPE html><script>localStorage.setItem('token', '{value}');
 window.location.href='https://dbm.sourav87.repl.co/dashboard';
    </script>
    """
	return render_template_string(script)



@app.route("/v2", methods=["POST"])
def verify():
	data = request.form.to_dict()
	print(data)
	if "key" not in data:
		return "<script>window.location.href='https://dbm.sourav87.repl.co/login'</script>"
	if {data['key']} == value:
		return "<script>window.location.href='https://dbm.sourav87.repl.co/dashboard'</script>"
	return "<script>window.location.href='https://dbm.sourav87.repl.co/login'</script>"
		

	
@app.route("/dashboard")
def dash():
	data =  {"docs":len(list(docs))}
	return render_template("index.html", token=value, list=docs, data=data)
	

app.run(host='0.0.0.0', port=8080)
