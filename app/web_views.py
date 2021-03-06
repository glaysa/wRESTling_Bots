from flask_login import login_user, login_required, logout_user, current_user
from flask import render_template, request, redirect, url_for, session, flash

from app.login import get_user
from app import app
from api_views import room_list
from data.dict2obj import dict2User


@app.route("/register")
def get_register():
    if 'user' in session:
        return redirect(url_for("get_home"))

    return render_template("register.html")


@app.route("/home")
@login_required
def get_home():
    user = session['user']
    user = dict2User(user)
    if 'user' not in session:
        user = request.args.get('user')

    return render_template("home.html", rooms=room_list, user=user)


@app.route("/profile")
@login_required
def get_profile_page():
    user = current_user
    if 'user' not in session:
        return redirect(url_for('get_login'))

    return render_template("profile.html", user=user)


@app.route("/chatroom/<room_id>")
@login_required
def get_room(room_id):
    active_room = None
    active_user = session['user']
    for room in room_list:
        if room.room_id == room_id:
            active_room = room
    return render_template(f"chatroom.html", room=active_room, user=active_user)


@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def get_login():
    if 'user' in session:
        the_current_user = dict2User(session['user'])
        return render_template('home.html', user=the_current_user, rooms=room_list)

    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user = get_user(username)
        if user and user.check_password(password):
            login_user(user)
            session['user'] = user
            return redirect(url_for('get_home'))
        flash(message="Wrong username or password, please try again or create a new user", category="warning")
    return render_template('login.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop('user', None)
    return redirect(url_for('get_login'))
