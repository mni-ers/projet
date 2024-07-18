from flask import Flask, render_template, redirect, url_for, flash, request, session,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'A_A'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    """
    Modèle de données pour les utilisateurs
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.today())

    def __repr__(self):
        return f'<User {self.username} {self.email} {self.password} {self.id}>'
    
    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password_hash': self.password,
            'creaated_at':self.created_at
    }

@app.route('/')
def index():
    #page d'acceuil 
    if 'user' in session:
        return render_template('home.html', user=session['user'],rigth=True)
    else:
         return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # on gere l'inscription ici
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Vérifier si l'utilisateur existe déjà
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Cet utilisateur existe déjà.', 'danger')
            return render_template('login.html', message=["User already exist. Please Login"]),400

        # Créer un nouvel utilisateur
        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Vous vous êtes inscrit avec succès. Vous pouvez maintenant vous connecter.', 'success')
        session['user'] = {new_user.username,new_user.id,new_user.email}
        redirect('home.html'), 201

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Gère la connexion
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user == None:
            return render_template('error.html',message="Not User Found")
        user_json = user.to_json()

        if user and check_password_hash(user_json['password_hash'], password):
                user_sendable = {'username':user.username,'email':user.email,'id':user.id,'created_at':user.created_at}
                session['user'] = user_sendable
                return render_template('home.html'),200
        elif check_password_hash == False: 
                return render_template('login.html',message="Incorrect Informations"), 400
        else:
            render_template('error.html',message="Not User Found")

    return render_template('login.html')

@app.route('/logout')
def logout():
    #Déconnecter l'utilisateur en retirant ses information de la session
 
    session.pop('user', None)
    flash('Vous vous êtes déconnecté.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)