"""Blogly application."""

from flask import Flask, render_template, redirect, flash, session, abort
from forms import FeedbackForm, RegisterUserForm, LoginUserForm
from models import Feedback, db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'supersecretdefinitelynotabletobeguessed'

connect_db(app)
db.create_all()

@app.route('/')
def redirect_to_register():
    return redirect('/register')

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")

@app.errorhandler(401)
def not_authenticated(e):
    return render_template("401.html")

def redirect_to_register():
    return redirect('/register')

""" USER ROUTES """
@app.route('/register', methods=["GET", "POST"])
def create_user():
    """ Register a New User """
    form = RegisterUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        user = User.register(username, password, email, first_name, last_name)

        db.session.add(user)
        db.session.commit()
        return redirect(f"/user/{user.username}")

    else:
        return render_template("register_user.html", form=form)

@app.route('/login', methods=["GET", "POST"])
def login_user():
    """authenticate a user"""
    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if User.authenticate(username, password):
            session["username"] = username
            return redirect(f"/users/{username}")
        else:
            flash("Incorrect username or password")
            return redirect('/login')
    else:
        return render_template("login_user.html", form=form)

@app.route('/logout')
def logout_user():
    """logout user"""
    session.pop('username')
    return redirect('/')

@app.route('/users/<username>')
def user_detail(username):
    if "username" not in session:
        abort(401)

    user = User.query.get_or_404(username)
    feedbacks = Feedback.query.filter_by(username=user.username).all()
    return render_template("user_info.html", user=user, feedbacks=feedbacks)

@app.route('/users/<username>/delete')
def delete_user(username):
    if username == session["username"]:
        user = User.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()
        flash(f'Deleted {username} successfully!')
        return redirect('/logout')
    else:
        abort(401)

@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def add_feedback(username):
    """give feedback"""
    if "username" not in session:
        abort(401)

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        feedback = Feedback(title=title, content=content, username=username)
        db.session.add(feedback)
        db.session.commit()
        return redirect(f'/users/{username}')
    else:
        return render_template("feedback.html", form=form)


@app.route('/feedback/<id>/update', methods=["GET", "POST"])
def edit_feedback(id):
    """edit feedback"""
    if "username" not in session:
        abort(401)

    feedback = Feedback.query.get_or_404(id)

    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit():
        feedback.title = form.title.data 
        feedback.content = form.content.data
        
        db.session.add(feedback)
        db.session.commit()
        return redirect(f'/users/{feedback.username}')
    else:
        return render_template("feedback.html", form=form, feedback=feedback)

@app.route('/feedback/<id>/delete', methods=["POST"])
def delete_feedback(id):
    """delete feedback"""
    feedback = Feedback.query.get_or_404(id)

    if feedback.username == session["username"]:
        db.session.delete(feedback)
        db.session.commit()
        flash(f'Deleted feedback successfully!')
        return redirect(f'/users/{feedback.username}')
    else:
        abort(401)