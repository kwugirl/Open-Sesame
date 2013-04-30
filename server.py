from flask import Flask, flash, render_template, redirect, request, session, url_for
import urllib  # used for URL encoding
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
    form_password1 = json.loads(request.form['password1'])  # takes unicode string from form and because it's already in JSON-acceptable format, gets it back out as a list data type instead of unicode string
    form_password2 = json.loads(request.form['password2'])
    form_password3 = json.loads(request.form['password3'])

    # TO DO: add check that email doesn't already exist in DB
    # TO DO: clean up whether 3 samples should be required
    if form_email and form_password1:  # checking that both email and pw have been entered
        gesture1 = dtw_algorithm.create_gesture(form_password1)
        gesture2 = dtw_algorithm.create_gesture(form_password2)
        gesture3 = dtw_algorithm.create_gesture(form_password3)

        gestures = [gesture1, gesture2, gesture3]

        # TO DO: better way to do this combinatorics?
        # run DTW on all pairs of samples, store greatest difference as user's personal threshold
        threshold = max(gesture1 - gesture2, gesture1 - gesture3, gesture2 - gesture3)

        new_user = model.User(email=form_email, password=gestures, threshold=threshold)
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

    authentication = False

    for password in user.password:
        if gesture - password <= user.threshold:
            authentication = True
            break

    if authentication is True:
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
    app.run(debug=True)
