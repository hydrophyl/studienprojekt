from flask import Blueprint, render_template, request, jsonify, redirect, url_for

views = Blueprint(__name__, "views")

@views.route("/")
def home():
  return render_template("index.html", name="Duy")

@views.route("/graphics")
def graphics():
  args = request.args
  time = args.get('time')
  return render_template("graphics.html", time=time)

@views.route("/json")
def get_json():
  return jsonify({'name':'duy', 'age':25})

@views.route("/data")
def get_date():
  data = request.json
  return jsonify(data)

@views.route("/go-to-home")
def go_to_home():
  return redirect(url_for("views.home"))