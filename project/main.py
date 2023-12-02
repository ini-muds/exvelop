from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Post  
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def posts_list():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('main.html', posts=posts)

@main.route('/search', methods=['GET'])
def search_posts():
    query = request.args.get('query')
    posts = Post.query.filter(Post.title.contains(query) | Post.description.contains(query)).all()
    return jsonify([{"name": post.name, "title": post.title, "description": post.description, "image_url": post.image_url, "code": post.code} for post in posts])

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

    # 現在のユーザーが投稿の作成者であるか確認
    if post.user_id != current_user.id:
        flash('You do not have permission to edit this post.')
        return redirect(url_for('main.posts_list'))

    # 投稿の編集
    if request.method == 'POST':
        post.title = request.form['title']
        post.description = request.form['description']
        post.image_url = request.form['image_url']
        post.code = request.form['code']
        db.session.commit()
        flash('Post updated')
        return redirect(url_for('main.detail_post', id=id))

    return render_template('edit.html', post=post, user_id=current_user.id)

@main.route('/delete/<int:id>')
@login_required
def delete_post(id):
    post_to_delete = Post.query.filter_by(id=id).first()
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('main.posts_list'))
