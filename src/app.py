from src.common.database import Database

from flask import Flask, render_template, request, session, make_response

from src.models.blog import Blog
from src.models.post import Post
from src.models.user import User

app = Flask(__name__)  # __main__
app.secret_key = 'yogi'


@app.route('/')
def hello_world():
    return render_template('home.html')


@app.route('/login')
def login_tempate():
    return render_template('login.html')


@app.route('/register')
def register_template():
    return render_template('register.html')


@app.before_request
def initialize_database():
    Database.initialize()


@app.route('/auth/login', methods=['POST'])  # get sends parameters in urls and post sents them hidden
def login_user():
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email, password):
        User.login(email)
    else:
        session['email'] = None

    return render_template("profile.html", email=session['email'])


@app.route('/auth/register', methods=['POST'])  # get sends parameters in urls and post sents them hidden
def register_user():
    email = request.form['email']
    password = request.form['password']

    a = User.register(email, password)

    return render_template("profile.html", email=session['email'])


@app.route('/blogs/<string:user_id>')  # if provided user will send user blogs
@app.route('/blogs')
def user_blog(user_id=None):
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session['email'])

    blogs = user.get_blogs()

    return render_template("user_blogs.html", blogs=blogs, email=user.email)


@app.route('/blogs/new', methods=['POST', 'GET'])
def new_blog():
    if request.method == 'GET':
        return render_template('new_blog.html')
    else:
        title = request.form['title']
        description = request.form['description']
        user = User.get_by_email(session['email'])
        new_blog = Blog(user.email, title, description, user._id)
        new_blog.save_to_mongo()

    return make_response(user_blog())  # return a funtion user_blog


@app.route('/posts/<string:blog_id>')
def user_posts(blog_id):
    blog = Blog.from_mongo(blog_id)
    posts = blog.get_post()

    return render_template("posts.html", posts=posts, blog_name=blog.title, blog_id=blog_id)


@app.route('/posts/new/<string:blog_id>', methods=['POST', 'GET'])
def new_post(blog_id):
    if request.method == 'GET':
        return render_template('new_post.html', blog_id=blog_id)
    else:
        title = request.form['title']
        content = request.form['content']
        user = User.get_by_email(session['email'])

        new_post = Post(blog_id, title, content, user.email)
        new_post.save_to_mongo()

    return make_response(user_posts(blog_id))  # return a funtion user_blog


if __name__ == "__main__":
    app.run(debug=True)
