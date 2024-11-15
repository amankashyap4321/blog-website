from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory
import sqlite3

app = Flask(__name__, static_folder='static', static_url_path='/static')

DATABASE = r'C://Users//asus//Desktop//blog website//src//db//blog.db'
#make sure this path is correct according to your system


@app.route('/assets/<path:filename>')
def custom_static(filename):
    return send_from_directory('assets', filename)

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, content FROM posts")
    posts = cursor.fetchall()
    conn.close()
    posts_list = [{'id': post[0], 'title': post[1], 'content': post[2]} for post in posts]
    return render_template('index.html', posts=posts_list)

@app.route('/post/<int:id>', methods=['GET'])
def view_post(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, content FROM posts WHERE id = ?", (id,))
    post = cursor.fetchone()
    conn.close()
    if post:
        post_dict = {'id': post[0], 'title': post[1], 'content': post[2]}
        return render_template('view_post.html', post=post_dict)
    else:
        return "Post not found", 404

@app.route('/post/<int:id>/edit', methods=['GET', 'POST'])
def edit_post(id):
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        cursor.execute("UPDATE posts SET title = ?, content = ? WHERE id = ?", (title, content, id))
        conn.commit()
        conn.close()
        return redirect(url_for('view_post', id=id))
    else:
        cursor.execute("SELECT id, title, content FROM posts WHERE id = ?", (id,))
        post = cursor.fetchone()
        conn.close()
        if post:
            post_dict = {'id': post[0], 'title': post[1], 'content': post[2]}
            return render_template('edit_post.html', post=post_dict)
        else:
            return "Post not found", 404

@app.route('/post/<int:id>/delete', methods=['POST'])
def delete_post(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posts WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/new-post', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('new_post.html')

if __name__ == '__main__':
    app.run(debug=True)
