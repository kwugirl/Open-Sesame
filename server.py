from flask import Flask, flash, render_template, redirect, request, session, url_for, jsonify
import model
import urllib # used for URL encoding
import dtw_algorithm
import json

app = Flask(__name__)
app.secret_key = 'some_secret'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create_user")
def create_user():
    return render_template("create_user.html")

@app.route("/save_user", methods=["POST"])
def save_user():

    form_email = urllib.quote(request.form['email'])
    form_password = json.loads(request.form['password']) # takes unicode string from form and because it's already in JSON-acceptable format, gets it back out as a list data type instead of unicode string

    # TO DO: add check that email doesn't already exist in DB
    if form_email and form_password: # checking that both email and pw have been entered

        vector_objects = []
        for vector in form_password: # convert vectors into objects
            new_vector = dtw_algorithm.Vector(vector[0], vector[1], vector[2])
            vector_objects.append(new_vector)

        gesture = dtw_algorithm.Gesture(vector_objects)

        new_user = model.User(email=form_email, password=vector_objects)
        model.session.add(new_user)
        model.session.commit()
        flash('New user ' + request.form['email'] + ' created!')
        return redirect(url_for('index'))
    else:
        flash('Please enter a valid email address and password.')
        return redirect(url_for('create_user'))

@app.route("/login", methods=['GET'])
def login():
    return render_template("login.html")

@app.route("/validate_login", methods=["POST"])
def validate_login():
    form_email = urllib.quote(request.form['email'])
    form_password = urllib.quote(request.form['password'])

    #form_email and form_password must both exist and match in db for row to be an object. Row is the entire row from the users table, including the id
    row = model.session.query(model.User).filter_by(email=form_email, password=form_password).first()

    if row:
        session['email'] = request.form['email']
        session['user_id'] = row.id
        flash('Login successful!')
        return redirect(url_for('index'))
    else:
        flash('Please enter a valid email address and password.')
        return redirect(url_for('login'))

@app.route("/logout")
def logout():
    session.pop('email', None)
    session.pop('user_id', None)
    flash('You have logged out.')
    return redirect(url_for('index'))



if __name__ == "__main__":
    app.run(debug = True)
