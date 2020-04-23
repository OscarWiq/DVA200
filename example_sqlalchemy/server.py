#!/usr/bin/env python
#Author: Oscar W owt18001

import os
from flask import Flask, abort, request, jsonify, g, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
import cryptography

# init
app = Flask(__name__)
app.config['SECRET_KEY'] = 'cisco var på ett disco men ingen gillade cisco'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# ext
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

# Definierar vad en användare är och vad en användare består av
# varje användare är en instans av detta objekt, detta beror på
# att SQLAlchemy behöver användare som objekt.
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(64))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user

@auth.verify_password
def verify_password(username_or_token, password):
    # försök att autentisera via token först
    user = User.verify_auth_token(username_or_token)
    if not user:
        # försök att autentisera via usr/pw
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

# Registrera ny användare    
# Success: 201 Created
# Failure: 400 Bad Request
@app.route('/api/users', methods=['POST'])
@auth.login_required
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)    # argument saknas
    if User.query.filter_by(username=username).first() is not None:
        abort(400)    # användaren existerar redan
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201, {'Location': url_for('get_user', id=user.id, _external=True)})

# Returnera en användare
# Success: 200 OK
# Failure: 400 Bad Request
@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})

@app.route('/api/users/del/<int:id>', methods=['DELETE'])
@auth.login_required
def del_user(id):
    user = User.query.get(id)
    name = user.username
    if not user:
        abort(400)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'username': name})

# Returnera en autentiserings-token
# Kräver HTTPBasicAuth header
# Success: Json-Objekt returneras med fältet
#           token, satt till en valid token,
#           samt duration till 600 sekunder.
# Failure: 401 Unauthorized
@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})

# Returnera en skyddad resurs, detta är vad vi vill använda
# Kräver HTTPBasicAuth header
# Success: Json-Objekt med data till den autentiserade användaren
# Failure: 401 Unauthorized
@app.route('/api/login')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})

if __name__ == '__main__':
    if not os.path.exists('db.sqlite'):
        db.create_all()
    app.run(debug=True, ssl_context='adhoc') # för https: app.run(debug=True, ssl_context='adhoc')
