from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Post  
from . import db

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def posts_list():
    if request.method == 'POST':
        query = request.form.get('searchQuery')
        posts = Post.query.filter(Post.title.contains(query)).order_by(Post.timestamp.desc()).all()
    else:
        posts = Post.query.order_by(Post.timestamp.desc()).all()

    return render_template('main.html', posts=posts)


@main.route('/post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'GET':
        return render_template('create.html')
    elif request.method == 'POST':
        name = current_user.name
        title = request.form['title']
        description = request.form['description']
        image_url = request.form.get('image_url')  # 画像URLは任意
        code = request.form.get('code')  # コードも任意
        new_post = Post(name=name, title=title, description=description, image_url=image_url, code=code, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        flash('Post created')
        return redirect(url_for('main.posts_list'))

@main.route('/detail/<int:id>')
def detail_post(id):
    post = Post.query.filter_by(id=id).first()

    # ユーザーがログインしているかどうかをチェック
    if current_user.is_authenticated:
        user_id = current_user.id
    else:
        user_id = None

    return render_template('detail.html', post=post, user_id=user_id)

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.filter_by(id=id).first()

    if post.user_id != current_user.id:
        flash('You do not have permission to edit this post.')
        return redirect(url_for('main.posts_list'))

    if request.method == 'POST':
        post.title = request.form['title']
        post.description = request.form['description']
        post.image_url = request.form.get('image_url')  # ここを修正
        post.code = request.form.get('code')            # 念のためここも確認
        db.session.commit()
        flash('Post updated')
        return redirect(url_for('main.posts_list', id=id))

    return render_template('edit.html', post=post)

@main.route('/delete/<int:id>')
@login_required
def delete_post(id):
    post_to_delete = Post.query.filter_by(id=id).first()
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('main.posts_list'))
