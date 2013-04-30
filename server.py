from flask import Flask, flash, render_template, redirect, request, session, url_for
import urllib # used for URL encoding
import json
import model
import dtw_algorithm

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
    # TO DO: add check for password not being in JSON format
    form_password = json.loads(request.form['password']) # takes unicode string from form and because it's already in JSON-acceptable format, gets it back out as a list data type instead of unicode string

    # TO DO: add check that email doesn't already exist in DB
    if form_email and form_password: # checking that both email and pw have been entered
        gesture = dtw_algorithm.create_gesture(form_password)

        new_user = model.User(email=form_email, password=gesture)
        model.session.add(new_user)
        model.session.commit()
        flash('New user ' + request.form['email'] + ' created!')
        return redirect(url_for('index'))
    else:
        flash('Please enter a valid email address and password.')
        return redirect(url_for('create_user'))

@app.route("/validate_login", methods=["POST"])
def validate_login():
    form_email = urllib.quote(request.form['email'])
    form_password = json.loads(request.form['password'])

    gesture = dtw_algorithm.create_gesture(form_password)

    user = model.session.query(model.User).filter_by(email=form_email).first()

    difference = gesture - user.password

    if difference < 1000: # TO DO: figure out what difference threshold should be
        session['email'] = request.form['email']
        session['user_id'] = user.id
        flash('Login successful!')

    else:
        flash('Please enter a valid email address and password.')

    return redirect(url_for('index'))

@app.route("/logout")
def logout():
    session.pop('email', None)
    session.pop('user_id', None)
    flash('You have logged out.')

    return redirect(url_for('index'))



if __name__ == "__main__":
    app.run(debug = True)
