from flask import Blueprint, render_template, url_for, request, current_app, flash, redirect, g
from flask_login import (current_user, login_user,
                         login_required, logout_user, confirm_login, login_fresh)
from .form import (LoginForm, RegisterForm,
                           EditProfileForm, ChangePasswordForm, UploadForm)
from datetime import datetime
from werkzeug import secure_filename
from .model import User
from ..topics.model import Topic
from ..models.user_meta import User_Meta
from ..ext import cache
import os

user = Blueprint("user", __name__)


@user.route("/user/<username>")
def profile(username):
    user = User.query.filter_by(name=username).first_or_404()
    posts = Topic.query.filter_by(user_id= user.id).all()
    return render_template("user/profile.html", user=user,posts=posts)


@user.route("/login", methods=['GET', 'POST'])
def login():
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for("user.profile", username=current_user.name))
    form = LoginForm()
    if form.validate_on_submit():
        authenticated, user = User.authenticate(
            form.name.data, form.password.data)
        if user and authenticated:
            meta=User_Meta()
            meta.set(user.id,'k','v')
            login_user(user, form.remember_me.data)
            #user.last_seen = datetime.utcnow()
            #user.save()
            return redirect(request.args.get("next") or url_for('user.profile', username=current_user.name))
        flash(authenticated, 'warning')
    return render_template("user/login.html", form=form)


@user.route("/register", methods=['GET', 'POST'])
def register():
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for("user.profile", username=current_user.name))
    # if current_app.config["ENABLE_REGISTER"]:
    form = RegisterForm()
    if form.validate_on_submit():
        user = form.save()

        login_user(user)
        flash("thanks for regisering", "success")
        return redirect(url_for("user.profile", username=current_user.name))
    return render_template("user/register.html", form=form)


@user.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index.indexs'))
# @user.route("/<username>/topics")
# def view_all_topics(username):


# @user.route("/<username>/posts")
# def view_all_posts(username):


# @user.route("/settings/general", methods=["POST", "GET"])
# @login_required
# def settings():


# @user.route("/settings/password", methods=["POST", "GET"])
# @login_required
# def change_password():


# @user.route("/settings/email", methods=["POST", "GET"])
# @login_required
# def change_email():


@user.route("/settings/edit_profile", methods=["POST", "GET"])
@login_required
def edit_user_profile():
    form = EditProfileForm(obj=current_user)
    change_pw_form = ChangePasswordForm(prefix='pwd')
    if form.has_been_submitted(request):
        if form.validate_on_submit():
            current_user.website = form.website.data
            current_user.avater = form.avater.data
            current_user.signature = form.signature.data
            saved = current_user.save()
            if saved:
                flash("saved your settings")
            else:
                flash("something went wrong")
    elif change_pw_form.has_been_submitted(request):
        if change_pw_form.validate_on_submit():
            if current_user.verify_password(change_pw_form.password.data):
                current_user.password = change_pw_form.new_password.data
                current_user.save()
                flash("You have changed password")
                form = EditProfileForm(obj=current_user)
            else:
                flash("wrong password")

    return render_template("user/profile_edit.html", form=form, change_pw_form=change_pw_form)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in current_app.config[
               'ALLOWED_EXTENSIONS']


@user.route('/uploads', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the name of the uploaded files
        uploaded_files = request.files.getlist("file[]")
        filenames = []
        for file in uploaded_files:
            # Check if the file is one of the allowed types/extensions
            if file and allowed_file(file.filename):
                # Make the filename safe, remove unsupported chars
                filename = secure_filename(file.filename)
                # Move the file form the temporal folder to the upload
                # folder we setup
                file.save(os.path.join(current_app.config[
                          'UPLOAD_FOLDER'], filename))

                url = os.path.join(current_app.config[
                                   'UPLOAD_FOLDER'], filename)
                # Save the filename into a list, we'll use it later
                filenames.append(url)
                # Redirect the user to the uploaded_file route, which
                # will basicaly show on the browser the uploaded file
        # Load an html page with a link to each uploaded file
        return render_template('upload.html', filenames=filenames)
    elif request.method == 'GET':
        return render_template('upload.html')
