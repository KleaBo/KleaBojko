from http import client
from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.client import Client



@app.route('/create/client', methods=['POST'])
def create_client():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Client.validate_client(request.form):
        return redirect('/')
    Client.save(request.form)
    return redirect('/')

@app.route('/client/<int:id>')
def show_client(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'client_id' : id,
        'user_id': session['user_id']
    }
    myClient = Client.get_one(data)
    return render_template('showOneClient.html', client=myClient,  user=User.get_by_id(data),)

@app.route('/client/<int:id>/like', methods=['GET','PUT'])
def like_client(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'client_id': id,
        'user_id': session['user_id'],
        
    }

    Client.addLike(data)
    updatedClient = Client.getUsersWhoLiked(data)
    updatedData = {
        'client_id': id,
        'likes': updatedClient.likes
    }
    Client.update(updatedData)
    return render_template('showOneClient.html', client=updatedClient,  user=User.get_by_id(data))

@app.route('/client/<int:id>/unlike', methods=['GET','PUT'])
def unlike_client(id):
    if 'user_id' not in session:
            return redirect('/logout')
    data={
        'client_id': id,
        'user_id': session['user_id'],
    }
    User.unLike(data)
    updatedClient = Client.getUsersWhoLiked(data)
    
    return render_template('showOneClient.html', client=updatedClient,  user=User.get_by_id(data))
