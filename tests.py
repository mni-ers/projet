from flask import Flask, render_template, redirect, url_for, flash, request, session,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

@app.route('/')
def index():
    if 'user' in session:
        return render_template('home.html', user=session['user'])
    else:
        return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # c'est ici qu'on verifie si l'user existe deja 
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Cet utilisateur existe déjà.', 'danger')
            return render_template('login.html',message=["User already exist . Please Login "])

        # on creer un nouvel utilisateur ici en se servant de la class User codée un peu plus au 
        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )
        #on l'ajoute a la db et on sauvegarde 
        db.session.add(new_user)
        db.session.commit()
        flash('Vous vous êtes inscrit avec succès. Vous pouvez maintenant vous connecter.', 'success')
        #on retourne le chemin par defaut du site
        
        return redirect(url_for('login')) , 201

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    #on veut bien verifier qu'il s'agit d'une methode POST pour effectuer le reste des actions 
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Vérifier si l'utilisateur existe
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user'] = user
            flash('Vous êtes connecté.', 'success')
            #on retourne le chemin par defaut du site si jamais la connexion réussie (home)
            return redirect(url_for('index')),201
        else:
            flash('Identifiants invalides.', 'danger')
            #dans le cas contraire on retourne la mm page (login)
            return render_template('login.html'), 400

    return render_template('login.html')

#chemin pour deconnecter l'user
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Vous vous êtes déconnecté.', 'success')
    return redirect(url_for('index'))

#code pour run l'application et lancer la db
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    
#utilisant l'ia d'Anthropic pour formatter le code pour gagner en temps