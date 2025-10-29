---
draft: true
title: "23. 웹 개발"
description: "Flask, Django 등 웹 프레임워크를 활용한 웹 애플리케이션 개발"
collection_order: 23
---

# 챕터 23: 웹 개발

> "웹으로 세상과 연결하라" - Flask와 Django를 활용하여 현대적인 웹 애플리케이션을 개발해봅시다.

## 학습 목표
- 웹 개발의 기본 개념과 구조를 이해할 수 있다
- Flask와 Django 프레임워크를 활용할 수 있다
- RESTful API를 설계하고 구현할 수 있다
- 웹 애플리케이션의 보안과 배포를 관리할 수 있다

## Flask 웹 프레임워크

### Flask 기본 구조

```python
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask import session, flash
import os

# Flask 애플리케이션 생성
app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # 세션을 위한 비밀키

# 기본 라우트
@app.route('/')
def home():
    """홈페이지"""
    return render_template('index.html')

@app.route('/about')
def about():
    """소개 페이지"""
    return '<h1>About Page</h1><p>This is a Flask web application.</p>'

# 동적 라우트
@app.route('/user/<string:username>')
def user_profile(username):
    """사용자 프로필 페이지"""
    return f'<h1>User Profile</h1><p>Welcome, {username}!</p>'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    """포스트 상세 페이지"""
    return f'<h1>Post #{post_id}</h1>'

# HTTP 메서드 처리
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """연락처 페이지"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # 여기서 이메일 발송 등 처리
        flash(f'Thank you, {name}! Your message has been sent.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

# JSON API 엔드포인트
@app.route('/api/users')
def api_users():
    """사용자 목록 API"""
    users = [
        {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
        {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'},
        {'id': 3, 'name': 'Charlie', 'email': 'charlie@example.com'}
    ]
    return jsonify(users)

@app.route('/api/users/<int:user_id>')
def api_user_detail(user_id):
    """사용자 상세 정보 API"""
    # 실제로는 데이터베이스에서 조회
    user = {'id': user_id, 'name': f'User {user_id}', 'email': f'user{user_id}@example.com'}
    return jsonify(user)

# 에러 핸들러
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### 템플릿과 정적 파일

```python
# templates/base.html
"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Flask App{% endblock %}</title>
    <link href="{{ url_for('static', filename='css/style.css') }}" rel="stylesheet">
</head>
<body>
    <nav>
        <ul>
            <li><a href="{{ url_for('home') }}">Home</a></li>
            <li><a href="{{ url_for('about') }}">About</a></li>
            <li><a href="{{ url_for('contact') }}">Contact</a></li>
        </ul>
    </nav>
    
    <main>
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        {% block content %}{% endblock %}
    </main>
    
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
</body>
</html>
"""

# templates/index.html
"""
{% extends "base.html" %}

{% block title %}Home - Flask App{% endblock %}

{% block content %}
<h1>Welcome to Flask App</h1>
<p>This is the home page of our Flask application.</p>

<div id="user-list">
    <h2>Users</h2>
    <div id="users"></div>
    <button onclick="loadUsers()">Load Users</button>
</div>

<script>
async function loadUsers() {
    try {
        const response = await fetch('/api/users');
        const users = await response.json();
        
        const usersDiv = document.getElementById('users');
        usersDiv.innerHTML = users.map(user => 
            `<div>
                <strong>${user.name}</strong> - ${user.email}
             </div>`
        ).join('');
    } catch (error) {
        console.error('Error loading users:', error);
    }
}
</script>
{% endblock %}
"""

# 템플릿 활용 예제
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/dashboard')
def dashboard():
    """대시보드 페이지"""
    user_data = {
        'name': 'Alice',
        'email': 'alice@example.com',
        'posts_count': 15,
        'followers': 142
    }
    
    recent_posts = [
        {'title': 'Flask 입문', 'date': '2024-01-15'},
        {'title': 'Python 웹 개발', 'date': '2024-01-10'},
        {'title': 'REST API 설계', 'date': '2024-01-05'}
    ]
    
    return render_template('dashboard.html', 
                         user=user_data, 
                         posts=recent_posts)
```

### 데이터베이스 연동 (Flask-SQLAlchemy)

```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# 데이터베이스 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 모델 정의
class User(db.Model):
    """사용자 모델"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 관계 설정
    posts = db.relationship('Post', backref='author', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'posts_count': len(self.posts)
        }

class Post(db.Model):
    """포스트 모델"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 외래키
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'author': self.author.username
        }

# API 엔드포인트들
@app.route('/api/users', methods=['GET', 'POST'])
def handle_users():
    """사용자 목록 조회 및 생성"""
    if request.method == 'GET':
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])
    
    elif request.method == 'POST':
        data = request.get_json()
        
        # 검증
        if not data.get('username') or not data.get('email'):
            return jsonify({'error': 'Username and email are required'}), 400
        
        # 중복 체크
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        # 사용자 생성
        user = User(
            username=data['username'],
            email=data['email']
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify(user.to_dict()), 201

@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    """사용자 상세 조회"""
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@app.route('/api/posts', methods=['GET', 'POST'])
def handle_posts():
    """포스트 목록 조회 및 생성"""
    if request.method == 'GET':
        posts = Post.query.order_by(Post.created_at.desc()).all()
        return jsonify([post.to_dict() for post in posts])
    
    elif request.method == 'POST':
        data = request.get_json()
        
        # 검증
        if not data.get('title') or not data.get('content') or not data.get('user_id'):
            return jsonify({'error': 'Title, content, and user_id are required'}), 400
        
        # 사용자 존재 확인
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # 포스트 생성
        post = Post(
            title=data['title'],
            content=data['content'],
            user_id=data['user_id']
        )
        
        db.session.add(post)
        db.session.commit()
        
        return jsonify(post.to_dict()), 201

@app.route('/api/posts/<int:post_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_post(post_id):
    """포스트 조회, 수정, 삭제"""
    post = Post.query.get_or_404(post_id)
    
    if request.method == 'GET':
        return jsonify(post.to_dict())
    
    elif request.method == 'PUT':
        data = request.get_json()
        
        if 'title' in data:
            post.title = data['title']
        if 'content' in data:
            post.content = data['content']
        
        post.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(post.to_dict())
    
    elif request.method == 'DELETE':
        db.session.delete(post)
        db.session.commit()
        
        return '', 204

# 데이터베이스 초기화
@app.before_first_request
def create_tables():
    db.create_all()
    
    # 샘플 데이터 생성
    if User.query.count() == 0:
        sample_user = User(username='admin', email='admin@example.com')
        db.session.add(sample_user)
        db.session.commit()
        
        sample_post = Post(
            title='Welcome to Flask Blog',
            content='This is the first post on our Flask blog!',
            user_id=sample_user.id
        )
        db.session.add(sample_post)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
```

## 실습 프로젝트

###️ 프로젝트 1: 완전한 블로그 시스템

```python
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 모델들
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text)
    
    posts = db.relationship('Post', backref='category', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.String(300))
    published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan')
    
    @property
    def comment_count(self):
        return len(self.comments)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

# 인증 데코레이터
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('로그인이 필요합니다.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('로그인이 필요합니다.', 'warning')
            return redirect(url_for('login'))
        
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin:
            flash('관리자 권한이 필요합니다.', 'error')
            return redirect(url_for('home'))
        
        return f(*args, **kwargs)
    return decorated_function

# 라우트들
@app.route('/')
def home():
    """홈페이지 - 최근 포스트들"""
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(published=True)\
                .order_by(Post.created_at.desc())\
                .paginate(page=page, per_page=5, error_out=False)
    
    categories = Category.query.all()
    
    return render_template('home.html', posts=posts, categories=categories)

@app.route('/post/<int:post_id>')
def post_detail(post_id):
    """포스트 상세 페이지"""
    post = Post.query.get_or_404(post_id)
    
    if not post.published and (
        'user_id' not in session or 
        session['user_id'] != post.user_id
    ):
        flash('접근할 수 없는 포스트입니다.', 'error')
        return redirect(url_for('home'))
    
    comments = Comment.query.filter_by(post_id=post_id)\
                          .order_by(Comment.created_at.desc()).all()
    
    return render_template('post_detail.html', post=post, comments=comments)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """로그인"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            
            flash(f'환영합니다, {user.username}님!', 'success')
            return redirect(url_for('home'))
        else:
            flash('잘못된 사용자명 또는 비밀번호입니다.', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """회원가입"""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # 검증
        if User.query.filter_by(username=username).first():
            flash('이미 사용 중인 사용자명입니다.', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('이미 사용 중인 이메일입니다.', 'error')
            return render_template('register.html')
        
        # 사용자 생성
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('회원가입이 완료되었습니다. 로그인해주세요.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """로그아웃"""
    session.clear()
    flash('로그아웃되었습니다.', 'info')
    return redirect(url_for('home'))

@app.route('/write', methods=['GET', 'POST'])
@login_required
def write_post():
    """포스트 작성"""
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        summary = request.form.get('summary', '')
        category_id = request.form.get('category_id')
        published = 'published' in request.form
        
        post = Post(
            title=title,
            content=content,
            summary=summary,
            published=published,
            user_id=session['user_id'],
            category_id=category_id if category_id else None
        )
        
        db.session.add(post)
        db.session.commit()
        
        flash('포스트가 작성되었습니다.', 'success')
        return redirect(url_for('post_detail', post_id=post.id))
    
    categories = Category.query.all()
    return render_template('write_post.html', categories=categories)

@app.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    """댓글 추가"""
    post = Post.query.get_or_404(post_id)
    content = request.form['content']
    
    comment = Comment(
        content=content,
        user_id=session['user_id'],
        post_id=post_id
    )
    
    db.session.add(comment)
    db.session.commit()
    
    flash('댓글이 추가되었습니다.', 'success')
    return redirect(url_for('post_detail', post_id=post_id))

@app.route('/admin')
@admin_required
def admin_dashboard():
    """관리자 대시보드"""
    users_count = User.query.count()
    posts_count = Post.query.count()
    comments_count = Comment.query.count()
    categories_count = Category.query.count()
    
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    recent_comments = Comment.query.order_by(Comment.created_at.desc()).limit(5).all()
    
    stats = {
        'users': users_count,
        'posts': posts_count,
        'comments': comments_count,
        'categories': categories_count
    }
    
    return render_template('admin_dashboard.html', 
                         stats=stats, 
                         recent_posts=recent_posts,
                         recent_comments=recent_comments)

# 데이터베이스 초기화
@app.before_first_request
def create_tables():
    db.create_all()
    
    # 관리자 계정 생성
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@example.com', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)
        
        # 기본 카테고리 생성
        categories = [
            Category(name='일반', description='일반적인 주제'),
            Category(name='기술', description='기술 관련 포스트'),
            Category(name='일상', description='일상 이야기')
        ]
        
        for category in categories:
            db.session.add(category)
        
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
```

## 체크리스트

### Flask 기초
- [ ] Flask 애플리케이션 구조 이해
- [ ] 라우팅과 뷰 함수 작성
- [ ] 템플릿과 정적 파일 활용
- [ ] HTTP 메서드 처리

### 데이터베이스 연동
- [ ] SQLAlchemy ORM 활용
- [ ] 모델 정의와 관계 설정
- [ ] 마이그레이션 관리
- [ ] 쿼리 최적화

### API 개발
- [ ] RESTful API 설계
- [ ] JSON 응답 처리
- [ ] 에러 처리와 상태 코드
- [ ] API 문서화

### 인증과 보안
- [ ] 사용자 인증 구현
- [ ] 세션 관리
- [ ] 비밀번호 해싱
- [ ] 권한 기반 접근 제어

### 실무 기능
- [ ] 페이지네이션 구현
- [ ] 파일 업로드 처리
- [ ] 폼 검증
- [ ] 에러 핸들링

## 다음 단계

🎉 **축하합니다!** 웹 개발을 마스터했습니다.

Flask를 통해 웹 개발의 기초를 익혔습니다. 이제 [24. 테스팅과 디버깅](../24_testing_debugging/)으로 넘어가서 코드 품질을 보장하는 방법을 학습해봅시다.

---

💡 **웹 개발 가이드:**
- **Flask는 간단한 API와 프로토타입**에 적합
- **보안**을 항상 최우선으로 고려
- **데이터베이스 설계**를 신중하게 계획
- **API 문서화**로 협업 효율성 향상
- **테스트 코드** 작성으로 품질 보장 