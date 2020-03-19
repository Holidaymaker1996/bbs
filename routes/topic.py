from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from models.reply import Reply
from routes import *

from models.topic import Topic
from models.board import Board

main = Blueprint('topic', __name__)


@main.route("/")
def index():
    board_id = int(request.args.get('board_id', -1))
    u = current_user()
    if board_id == -1:
        ms = Topic.all()
        b = sorted(ms, key=lambda m: m.created_time, reverse=True)
    else:
        ms = Topic.all(board_id=board_id)
        b = sorted(ms, key=lambda m: m.created_time, reverse=True)
    token = new_csrf_token()
    bs = Board.all()
    return render_template("topic/index.html", user=u, ms=b, token=token, bs=bs, bid=board_id)


@main.route('/<int:id>')
def detail(id):
    m = Topic.get(id)
    b = Board.one(id=m.board_id)
    # 传递 topic 的所有 reply 到 页面中
    return render_template("topic/detail.html", topic=m, b=b)


@main.route("/delete")
@csrf_required
# @author_required
def delete():
    id = int(request.args.get('id'))
    u = current_user()
    print('删除 topic 用户是', u, id)
    Topic.delete(id)
    return redirect(url_for('.index'))


@main.route("/new")
def new():
    board_id = int(request.args.get('board_id'))
    bs = Board.all()
    # return render_template("topic/new.html", bs=bs, bid=board_id)
    token = new_csrf_token()
    return render_template("topic/new.html", bs=bs, token=token, bid=board_id)


@main.route("/add", methods=["POST"])
@csrf_required
def add():
    form = request.form.to_dict()
    u = current_user()
    Topic.new(form, user_id=u.id)
    return redirect(url_for('.index'))


# @main.route('/user/<string:username>')
# def user(username):
#     u = User.one(username=username)
#     topics = Topic.all(user_id=u.id)
#
#     b = sorted(topics, key=lambda m: m.created_time, reverse=True)
#
#     replies = Reply.all(user_id=u.id)
#     replies_topics = []
#     for r in replies:
#         a = Topic.one(id=r.topic_id)
#         replies_topics.append(a)
#     replies_topics = sorted(replies_topics, key=lambda m: m.created_time, reverse=True)
#     return render_template('topic/user.html', u=u, topics=b, ms=replies_topics)
