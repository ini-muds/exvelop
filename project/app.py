from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    title = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    image_url = db.Column(db.String(200), nullable=True)
    code = db.Column(db.String(1000), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)

@app.route('/post', methods=['POST'])
def create_post():
    data = request.json
    new_post = Post(name=data['name'], title=data['title'], description=data['description'], image_url=data['image_url'], code=data['code'])
    db.session.add(new_post)
    db.session.commit()
    return jsonify({"message": "Post created"}), 201

@app.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return jsonify([{"name": post.name, "title": post.title, "description": post.description, "image_url": post.image_url, "code": post.code} for post in posts])

@app.route('/search', methods=['GET'])
def search_posts():
    query = request.args.get('query')
    posts = Post.query.filter(Post.title.contains(query) | Post.description.contains(query)).all()
    return jsonify([{"name": post.name, "title": post.title, "description": post.description, "image_url": post.image_url, "code": post.code} for post in posts])

if __name__ == '__main__':
    app.run(debug=True)
