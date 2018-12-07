from flask import render_template, flash, redirect, session, url_for, request, g
from flask_admin.contrib.sqla import ModelView
from flask_wtf.csrf import CsrfProtect
 

from app import app, db, admin
from .models import Todolist
from .forms import TodolistForm

admin.add_view(ModelView(Todolist, db.session))



@app.route('/create_todolist', methods=['GET','POST'])
def create_todolist():
    form = TodolistForm()
    flash('Errors="%s"' %
          (form.errors))
    if form.validate_on_submit():
        t = Todolist(content=form.content.data, date=form.date.data, title=form.title.data)
        db.session.add(t)
        db.session.commit()
        return redirect('/')

    return render_template('create_todolist.html',
                           title='Create Todolist',
                           form=form)

@app.route('/', methods=['GET'])
def getAllTodolist1():
    todolist = Todolist.query.all()
    return render_template('todolist_list.html',
                           title='All Todolist',
                           todolist=todolist)

@app.route('/todolist_yes', methods=['GET'])
def getAllTodolist2():
    todolist = Todolist.query.filter(Todolist.status==True).all()
    return render_template('todolist_list.html',
                           title='Complete Todolist',
                           todolist=todolist)

@app.route('/todolist_no', methods=['GET'])
def getAllTodolist3():
    todolist = Todolist.query.filter(Todolist.status==False).all()
    return render_template('todolist_list.html',
                           title='Uncomplete Todolist',
                           todolist=todolist)


@app.route('/delete_todolist/<id>', methods=['GET'])
def delete_todolist(id):
    todolist = Todolist.query.get(id)
    db.session.delete(todolist)
    db.session.commit()
    return redirect('/')

@app.route('/todolist_complete/<id>', methods=['GET'])
def todolist_complete(id):
    todolist = Todolist.query.get(id)
    todolist.status=True
    db.session.commit()
    return redirect('/')

CsrfProtect(app)
#csrf保护