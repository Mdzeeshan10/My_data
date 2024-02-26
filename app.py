import os
import urllib.parse 
from flask import Flask, render_template, request, g, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash


import yaml

with open('secrete_key/azureopenaikeys.yaml', 'r') as file:
    azurecred = yaml.safe_load(file)

# from Models.agentchatmemory import chatconversationagent

GPT_35_TURBO= azurecred["azureopenai"]["Azure_openai_deployment_35T_name"]                       #os.getenv("Azure_openai_deployment_35T_name")                       #secret["Azure_openai_deployment_35T_name"]
GPT_4_TURBO= azurecred["azureopenai"]["Azure_openai_deployment_4T_name"]             # os.getenv("Azure_openai_deployment_4T_name")                               #secret["Azure_openai_deployment_4T_name"]
GPT_35_TURBO_16K= azurecred["azureopenai"]["Azure_openai_deployment_35T_16k_name"]         #os.getenv("Azure_openai_deployment_35T_16k_name")                      #secret["Azure_openai_deployment_35T_16k_name"]
GPT_4_TURBO_32k=azurecred["azureopenai"]["Azure_openai_deployment_4T_32k_name"]                #os.getenv("Azure_openai_deployment_4T_32k_name")           #secret["Azure_openai_deployment_4T_32k_name"]

AzureDBusername= azurecred["azureopenai"]["username"]
AzureDBpassword= azurecred["azureopenai"]["password"]
AzureDBserver= azurecred["azureopenai"]["server"]
AzureDBdatabasename= azurecred["azureopenai"]["database"]

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret'

# Configure Database URI:
params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};SERVER=stream-data.database.windows.net;DATABASE=stream-data-db;UID=zee;PWD=P@ssw0rd")
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# Initialize SQLAlchemy
db = SQLAlchemy(app)





# Define User model
# Define User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(2000), nullable=False)  # Increased length to 2000
    normal_password = db.Column(db.String(200), nullable=False)

    @property
    def password(self):
        raise AttributeError('Password is not readable.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        self.normal_password=password

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        
        if user and user.verify_password(password):
            login_user(user)
            name = user.name
            # models = ["model1", "model2"]  # Example models list
            models = {
                            "GPT_35_TURBO": GPT_35_TURBO,
                            "GPT_35_TURBO_16K": GPT_35_TURBO_16K,
                            "GPT_4_TURBO": GPT_4_TURBO,
                            "GPT_4_TURBO_32K": GPT_4_TURBO_32k
                        }
        
            return render_template("gpt.html", models=models, username=name)
        else:
            flash("Login Faild. Please Check Your email and password")
            return redirect(url_for("login"))
    return render_template('login.html')

from Models.clasmodel import chat_gen
myllm = chat_gen()

@app.route('/process_message', methods=['POST'])
def process_message():
    # from Models.clasmodel import chat_gen
    # myllm = chat_gen()
    
    data = request.get_json()
    
    user_input = data['message']
    model = data['model']
    response = myllm.ask_pdf(model, user_input)
    # Your processing logic here, for example, using GPT to generate a response
    # For demonstration purposes, let's just echo back the user input
    gpt_response = response
    
    return jsonify(gpt_response)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address already exists', 'error')
        else:
            new_user = User(name=name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. Please login.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
