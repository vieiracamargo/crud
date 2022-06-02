import jwt
from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_login import LoginManager



login_manager = LoginManager()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

@login_manager.user_loader
def get_user(user_id):
    return Pessoa.query.filter_by(id=user_id)

db = SQLAlchemy(app)
class Pessoa(db.Model, UserMixin):
    __tablename__ ='usuarios'
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String)
    senha = db.Column(db.String)
    email = db.Column(db.String)
    telefone = db.Column(db.String)
    cpf = db.Column(db.String)
    data_nascimento = db.Column(db.String) #Verificar o Problema do Date

    def __init__(self, nome, senha, email, telefone, cpf, data_nascimento):
        self.nome = nome
        self.senha = senha
        self.email = email
        self.telefone = telefone
        self.cpf = cpf
        self.data_nascimento = data_nascimento

db.create_all()

@app.route('/')
def index():
    return render_template('login_page.html')

@app.route('/cadastrar')
def cadastrar():
    return render_template('cadastro.html')

@app.route('/user/create', methods=["POST", "GET"])
def create():
    if request.method == "POST":
        nome = request.form['usuario']
        senha = request.form['senha']
        email = request.form['email']
        telefone = request.form['telefone']
        cpf = request.form['cpf']
        data_nascimento = request.form['data-nascimento']

        if nome and senha and email and telefone and cpf and data_nascimento:
            p = Pessoa(nome, senha, email, telefone, cpf, data_nascimento)
            db.session.add(p)
            db.session.commit()

    return redirect('/')

@app.route('/user/read')
def read():
    pessoas = Pessoa.query.all()
    return render_template('user.html', pessoas=pessoas)


@app.route('/user/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    pessoa = Pessoa.query.filter_by(_id=id).first()

    if request.method == "POST":
        nome = request.form['usuario']
        senha = request.form['senha']
        email = request.form['email']
        telefone = request.form['telefone']
        cpf = request.form['cpf']
        data_nascimento = request.form['data-nascimento']

        if nome and senha and email and telefone and cpf and data_nascimento:
            pessoa.nome = nome
            pessoa.senha = senha
            pessoa.email = email
            pessoa.telefone = telefone
            pessoa.cpf = cpf
            pessoa.data_nascimento = data_nascimento

            db.session.commit()

            return redirect('/user/read')

    return render_template('atualizar.html', pessoa=pessoa)

@app.route('/user/delete/<int:id>')
def delete(id):
    pessoa = Pessoa.query.filter_by(_id=id).first()
    db.session.delete(pessoa)
    db.session.commit()

    pessoas = Pessoa.query.all()
    return render_template('user.html', pessoas=pessoas)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        nome = request.form['usuario']
        senha = request.form['senha']

        user = Pessoa.query.filter_by(nome=nome).first()
        password = Pessoa.query.filter_by(senha=senha).first()
        encoded_jwt = jwt.encode({"some": "payload"}, "secret", algorithm="HS256")

        if not user or not password:
            return redirect('/')

    return jsonify({"token": encoded_jwt})

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)
