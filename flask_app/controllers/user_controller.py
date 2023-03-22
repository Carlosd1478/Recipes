from flask_app import app
from flask_app.models.user_model import User
from flask import render_template, session, request, redirect, flash
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt( app )

@app.route( '/', methods = ['GET'] )
def display_login_registration_form():
    return render_template( "login_registration.html" )

@app.route( '/user/new', methods = ['POST'])
def create_user():
    if User.validate_registration( request.form):

        encrypted_password = User.encypt_password( request.form["password"], bcrypt )

        if User.get_one_by_email( { "email" : request.form['email'] }, "registration" ) == True:

            data = {
                **request.form,
                "password" : encrypted_password
            }
            user_id = User.create_one( data )
            session['user_id'] = user_id
            session['first_name'] = request.form['first_name']
            return redirect( '/recipes' )
        else:
            return redirect( "/" )
    else:
        return redirect( "/" )
    
@app.route('/login', methods = ['POST'])
def proccess_login():
    current_user = User.get_one_by_email({"email" : request.form['email_login']}, "login")
    if current_user:
        if User.validate_password( request.form["password_login"], current_user.password, bcrypt) == True:
            session['user_id'] = current_user.id
            session['first_name'] = current_user.first_name
            return redirect( '/recipes' )
        else:
            return redirect( "/" )
    else:
        return redirect( "/" )
    
@app.route('/logout', methods = ['POST'])
def process_logout():
    session.clear()
    return redirect('/')
