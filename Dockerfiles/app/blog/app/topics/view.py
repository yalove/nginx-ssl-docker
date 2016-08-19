from flask import Blueprint, render_template, url_for, request, current_app, flash, redirect, g
from flask_login import (current_user, login_user,
                         login_required, logout_user, confirm_login, login_fresh)
from ..users.model import User
from .model import Topic
from ..models.comment import Comment
from .form import TopicForm
from ..models.comment_form import Comment_Form, Comment_User_Form

topic = Blueprint("topic", __name__)


@topic.route("/newpost", methods=['GET', 'POST'])
@login_required
def newpost():
    form = TopicForm(request.form, prefix="post")
    if form.has_been_submitted(request):
        if form.validate_on_submit():
            topic = Topic()
            new_post = topic.create_topic(user=current_user,
                                          title=form.title.data,
                                          markdown=form.content.data)
            new_post.to_ping = u'www.baidu.com'
            if request.form['test-editormd-html-code']:
                new_post.html = request.form['test-editormd-html-code']
            status = new_post.save()
            if status:
                flash("Successfully posted")
                return redirect(url_for('topic.topic_single', topic_name=topic.name))
            else:
                flash("something is wrong")
    return render_template("topic/newpost.html", form=form)


@topic.route("/topic/<topic_name>", methods=["POST", "GET"])
def topic_single(topic_name):
    topic = Topic.query.filter_by(name=topic_name).first_or_404()
    user = User.query.filter_by(id=topic.user_id).first_or_404()
    comments = Comment.query.filter_by(topic_id=topic.id)
    if current_user.is_anonymous():
        comment_form = Comment_Form()
    else:
        comment_form = Comment_User_Form()
    if comment_form.has_been_submitted(request):
        if comment_form.validate_on_submit():
            comment_form.save(topic, user)
            flash("thanks for comment", "success")
    return render_template("topic/single.html", topic=topic, current_user=current_user, user=user, comments=comments, comment_form=comment_form)
