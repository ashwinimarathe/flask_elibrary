from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,session
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('dashboard', __name__)


@bp.route('/')
def index():
    return "Hello"
    # db = get_db()
    # user_id = session.get('user_id')
    # books = db.execute(
    #     'SELECT b.id, b.name, b.author, b.publisher,b.yera_of_publication, ub.possessedid, u.name FROM books b, users u,users_books ub where  u.id = ub.ownerid AND b.id = ub.bookid AND  u.id=?',(user_id,)
    # ).fetchall()
    # rentedbooks = db.execute(
    #     'SELECT b.id, b.name, b.author, b.publisher,b.yera_of_publication, ub.possessedid, u.name FROM books b, users u,users_books ub where  u.id = ub.ownerid AND b.id = ub.bookid AND ub.possessedid<>ub.ownerid AND ub.ownerid != ? AND ub.possessedid=?',(user_id,user_id)
    # )
    # return render_template('dashboard/index.html', books=books, rentedbooks = rentedbooks)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        publisher = request.form['publisher']
        publishyear = request.form['publishyear']
        error = None

        if not title:
            error = 'Title is required.'
        if not author:
            error = 'Author is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            user_id = str(session.get('user_id'))
            #title = title.replace(" ","")
            db.execute(
                'insert into books values'
                '(?,?,?,?,?);', ((title.replace(" ",""))+"_"+str(user_id), title, author, publisher, publishyear)
            )
            db.execute(
            	'insert into users_books values (?,?,?)', (str(user_id), title.replace(" ","")+"_"+str(user_id), str(user_id))
            	)
            db.commit()
            return redirect(url_for('dashboard.index'))

    return render_template('dashboard/create.html')


@bp.route('/findbook', methods=('GET', 'POST'))
@login_required
def findbook():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        db = get_db()
        user_id = session.get('user_id')
        if title is not None:
            return redirect(url_for('dashboard.rent', title=title))
        elif author is not None:
            return redirect(url_for('dashboard.rent', title=author))     
        db.commit()
        return redirect(url_for('dashboard.rent', title=rentedbooks))
        #return redirect('dashboard/rent.html', books=books)
    return render_template('dashboard/find.html')


@bp.route('/rent/<title>', methods=('GET', 'POST'))
@login_required
def rent(title):
    if request.method == 'GET':
        user_id = session.get('user_id')
        db = get_db()
#       title = title.replace(" ","")
        rentedbooks=db.execute(
                'SELECT b.id, b.name, b.author, b.publisher, b.yera_of_publication, ub.ownerid FROM books as b, users_books as ub WHERE ub.bookid=b.id AND ub.ownerid=ub.possessedid AND ub.ownerid<> ? AND b.name=?',(user_id, title,)
            ).fetchall()
        db.commit()
        return render_template('dashboard/rent.html', books=rentedbooks)
    elif request.method == 'POST':
        bookid = request.form['submit_button']
        print("debug: bookid: "+bookid)
        user_id = session.get('user_id')
        db = get_db()
        ownerid = bookid.split("_")[1]
        db.execute(f'update users_books set possessedid="{user_id}" where bookid="{bookid}" AND ownerid="{ownerid}"')
        db.commit()
        return redirect(url_for('dashboard.index'))



