import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
from werkzeug.exceptions import abort
import os
import requests, json, flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'codebinpy'

#connect db
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

#get post
def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

#index
@app.route("/", methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

#admin
@app.route("/admin/pass", methods=['GET', 'POST'])
def admin():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('admin.html', posts=posts)

#code
@app.route("/<int:post_id>")
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

#raw
@app.route("/raw/<int:post_id>")
def raw(post_id):
    post = get_post(post_id)
    return render_template('raw.html', post=post)

#print
@app.route("/print/<int:post_id>")
def print(post_id):
    post = get_post(post_id)
    return render_template('print.html', post=post)

#docs
@app.route("/docs")
def doc():
    return render_template('doc.html', post=post)

#v
@app.route("/v")
def v():
    return render_template('v.html')

#sourse code
@app.route("/sc")
def sc():
    return render_template('sourse.html')

#create
@app.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Нету заголовка!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect('/')

    return render_template('create.html')

#edit code
@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Нету заголовка!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect('/')

    return render_template('edit.html', post=post)

#delete
@app.route("/delete/<int:id>", methods=['GET', 'POST'])
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" удачно удалён!'.format(post['title']))
    return redirect('/')

####API####
@app.route('/api', methods=['POST', 'GET'])
def postapi():
    global post
    if request.method == 'POST':
        code = request.get_json()
        title = 'api_code'
        content = str(code)
        conn = get_db_connection()
        conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                     (title, content))
        conn.commit()
        conn.close()
        return jsonify({'url': "https://codebinpy.herokuapp.com/" + post}), 201
    else:
        return "API в разработке"

#404
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

#RUN
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
